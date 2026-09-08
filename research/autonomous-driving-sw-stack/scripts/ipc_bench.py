#!/usr/bin/env python3
"""D4 — 동일 호스트 IPC 마이크로벤치: Zenoh vs CycloneDDS (vs 파이프 기준선)

두 프로세스(ping/pong) 사이의 왕복 지연(RTT)과 단방향 처리량을 페이로드 크기별로 잰다.
Python 바인딩 오버헤드가 지배하므로 절대치가 아니라 **같은 조건의 상대 비교**로만 읽는다.

사용:
  python3 -m venv ipcenv && ./ipcenv/bin/pip install eclipse-zenoh cyclonedds
  ./ipcenv/bin/python ipc_bench.py --out d4-ipc-bench.md
옵션:
  --sizes 64,4096,65536,1048576   페이로드 바이트
  --n 1000                        RTT 샘플 수 (1 MB는 자동으로 1/5)
  --transports pipe,zenoh,cyclonedds
"""
import argparse
import json
import multiprocessing as mp
import os
import platform
import statistics
import sys
import time
from dataclasses import dataclass

# ----------------------------------------------------------------------------- 공통

def pct(xs, p):
    xs = sorted(xs)
    k = (len(xs) - 1) * p
    f = int(k)
    c = min(f + 1, len(xs) - 1)
    return xs[f] + (xs[c] - xs[f]) * (k - f)


def summarize(lat_us):
    return {
        "n": len(lat_us),
        "mean_us": statistics.fmean(lat_us),
        "median_us": statistics.median(lat_us),
        "p95_us": pct(lat_us, 0.95),
        "p99_us": pct(lat_us, 0.99),
        "min_us": min(lat_us),
        "max_us": max(lat_us),
    }


def env_info():
    cpu = "unknown"
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("model name"):
                    cpu = line.split(":", 1)[1].strip()
                    break
    except OSError:
        pass
    load = os.getloadavg() if hasattr(os, "getloadavg") else (None,) * 3
    versions = {}
    from importlib.metadata import version as _v
    for dist in ("eclipse-zenoh", "cyclonedds"):
        try:
            versions[dist] = _v(dist)
        except Exception as e:  # pragma: no cover
            versions[dist] = f"미설치: {e}"
    return {
        "date": time.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "cpu": cpu,
        "ncpu": os.cpu_count(),
        "loadavg_1_5_15": load,
        "versions": versions,
    }


# ----------------------------------------------------------------------------- pipe 기준선

def _pipe_pong(conn, n_total):
    for _ in range(n_total):
        data = conn.recv_bytes()
        conn.send_bytes(data)


def bench_pipe(size, n, warmup):
    a, b = mp.Pipe(duplex=True)
    p = mp.Process(target=_pipe_pong, args=(b, n + warmup), daemon=True)
    p.start()
    payload = os.urandom(size)
    lat = []
    for i in range(n + warmup):
        t0 = time.perf_counter_ns()
        a.send_bytes(payload)
        a.recv_bytes()
        t1 = time.perf_counter_ns()
        if i >= warmup:
            lat.append((t1 - t0) / 1000.0)
    p.join(timeout=5)
    return lat


# ----------------------------------------------------------------------------- zenoh

ZENOH_EP = "tcp/127.0.0.1:7447"


def _zenoh_conf(listen: bool):
    """샌드박스에 IPv6가 없어 기본 listen(tcp/[::]:0)이 실패한다 → IPv4 루프백 고정, 멀티캐스트 스카우팅 끔."""
    import zenoh
    c = zenoh.Config()
    c.insert_json5("scouting/multicast/enabled", "false")
    if listen:
        c.insert_json5("listen/endpoints", f'["{ZENOH_EP}"]')
    else:
        c.insert_json5("listen/endpoints", "[]")
        c.insert_json5("connect/endpoints", f'["{ZENOH_EP}"]')
    return c


def _zenoh_pong(ready, n_total):
    import zenoh
    conf = _zenoh_conf(listen=True)
    s = zenoh.open(conf)
    pub = s.declare_publisher("bench/pong")

    def cb(sample):
        pub.put(sample.payload.to_bytes())

    sub = s.declare_subscriber("bench/ping", cb)
    ready.set()
    # 프로세스는 부모가 종료시킨다
    while True:
        time.sleep(1)


def bench_zenoh(size, n, warmup):
    import threading
    import zenoh
    ready = mp.Event()
    p = mp.Process(target=_zenoh_pong, args=(ready, n + warmup), daemon=True)
    p.start()
    ready.wait(20)
    conf = _zenoh_conf(listen=False)
    s = zenoh.open(conf)
    got = threading.Event()

    def cb(sample):
        got.set()

    sub = s.declare_subscriber("bench/pong", cb)
    pub = s.declare_publisher("bench/ping")
    time.sleep(1.0)  # 디스커버리 안정화
    payload = os.urandom(size)
    lat = []
    for i in range(n + warmup):
        got.clear()
        t0 = time.perf_counter_ns()
        pub.put(payload)
        if not got.wait(5):
            raise RuntimeError("zenoh: pong 타임아웃")
        t1 = time.perf_counter_ns()
        if i >= warmup:
            lat.append((t1 - t0) / 1000.0)
    s.close()
    p.terminate()
    p.join(timeout=5)
    return lat


# ----------------------------------------------------------------------------- cyclonedds

def _cdds_types():
    from cyclonedds.idl import IdlStruct
    from cyclonedds.idl.types import sequence, uint8, uint64

    @dataclass
    class BenchMsg(IdlStruct, typename="bench.BenchMsg"):
        seq: uint64
        data: sequence[uint8]

    return BenchMsg


def _cdds_pong(ready, n_total):
    from cyclonedds.domain import DomainParticipant
    from cyclonedds.topic import Topic
    from cyclonedds.pub import DataWriter
    from cyclonedds.sub import DataReader
    from cyclonedds.core import Qos, Policy
    from cyclonedds.util import duration

    BenchMsg = _cdds_types()
    dp = DomainParticipant()
    qos = Qos(Policy.Reliability.Reliable(duration(seconds=10)), Policy.History.KeepLast(16))
    t_ping = Topic(dp, "bench_ping", BenchMsg, qos=qos)
    t_pong = Topic(dp, "bench_pong", BenchMsg, qos=qos)
    dr = DataReader(dp, t_ping, qos=qos)
    dw = DataWriter(dp, t_pong, qos=qos)
    ready.set()
    while True:
        for m in dr.take_iter(timeout=duration(seconds=30)):
            dw.write(m)


def bench_cyclonedds(size, n, warmup):
    from cyclonedds.domain import DomainParticipant
    from cyclonedds.topic import Topic
    from cyclonedds.pub import DataWriter
    from cyclonedds.sub import DataReader
    from cyclonedds.core import Qos, Policy
    from cyclonedds.util import duration

    BenchMsg = _cdds_types()
    ready = mp.Event()
    p = mp.Process(target=_cdds_pong, args=(ready, n + warmup), daemon=True)
    p.start()
    ready.wait(20)
    dp = DomainParticipant()
    qos = Qos(Policy.Reliability.Reliable(duration(seconds=10)), Policy.History.KeepLast(16))
    t_ping = Topic(dp, "bench_ping", BenchMsg, qos=qos)
    t_pong = Topic(dp, "bench_pong", BenchMsg, qos=qos)
    dw = DataWriter(dp, t_ping, qos=qos)
    dr = DataReader(dp, t_pong, qos=qos)
    time.sleep(1.0)  # 디스커버리 안정화
    payload = list(os.urandom(size))
    lat = []
    for i in range(n + warmup):
        msg = BenchMsg(seq=i, data=payload)
        t0 = time.perf_counter_ns()
        dw.write(msg)
        got = False
        for m in dr.take_iter(timeout=duration(seconds=5)):
            if m.seq == i:
                got = True
                break
        if not got:
            raise RuntimeError("cyclonedds: pong 타임아웃")
        t1 = time.perf_counter_ns()
        if i >= warmup:
            lat.append((t1 - t0) / 1000.0)
    p.terminate()
    p.join(timeout=5)
    return lat


# ----------------------------------------------------------------------------- 실행

BENCHES = {"pipe": bench_pipe, "zenoh": bench_zenoh, "cyclonedds": bench_cyclonedds}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", default="64,4096,65536,1048576")
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--warmup", type=int, default=50)
    ap.add_argument("--transports", default="pipe,zenoh,cyclonedds")
    ap.add_argument("--out", default="-")
    args = ap.parse_args()
    sizes = [int(s) for s in args.sizes.split(",")]
    transports = args.transports.split(",")
    info = env_info()
    results = []
    for tr in transports:
        for size in sizes:
            n = args.n if size < 1_000_000 else max(args.n // 5, 50)
            try:
                lat = BENCHES[tr](size, n, args.warmup)
                s = summarize(lat)
                s.update({"transport": tr, "size": size, "ok": True})
                # 왕복 1회당 2번 전송 → 단방향 처리량 근사 (msg/s, MB/s)
                s["oneway_msgs_per_s"] = 2.0 / (s["mean_us"] / 1e6)
                s["oneway_MBps"] = s["oneway_msgs_per_s"] * size / 1e6
            except Exception as e:
                s = {"transport": tr, "size": size, "ok": False, "error": repr(e)}
            results.append(s)
            print(json.dumps(s, ensure_ascii=False), file=sys.stderr)

    lines = []
    lines.append("# D4 — 동일 호스트 IPC 마이크로벤치 (Zenoh vs CycloneDDS vs 파이프 기준선)\n")
    lines.append(f"- 실행일: {info['date']}")
    lines.append(f"- 환경: Python {info['python']} · {info['platform']} · CPU {info['cpu']} × {info['ncpu']} · loadavg {info['loadavg_1_5_15']}")
    lines.append(f"- 버전: {info['versions']}")
    lines.append(f"- 명령: `{' '.join(sys.argv)}`")
    lines.append("- 방법: ping 프로세스가 페이로드를 발행하고 pong 프로세스가 같은 크기로 되돌려 보내는 왕복 지연(RTT). "
                 f"워밍업 {args.warmup}회 제외, 샘플 {args.n}회(1 MB는 1/5). 파이프는 multiprocessing.Pipe(바이트) 기준선. "
                 "Zenoh는 peer 모드 기본 설정, CycloneDDS는 Reliable·KeepLast(16), sequence<uint8> IDL(파이썬 리스트 직렬화 포함). "
                 "**Python 바인딩·GIL 오버헤드가 포함된 수치이므로 절대치가 아닌 상대 비교용.**\n")
    lines.append("| 전송 | 페이로드 | n | 평균 RTT(µs) | 중앙값 | p95 | p99 | 최소 | 단방향 msg/s | 단방향 MB/s |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for s in results:
        if s.get("ok"):
            lines.append(f"| {s['transport']} | {s['size']:,} B | {s['n']} | {s['mean_us']:.0f} | {s['median_us']:.0f} | {s['p95_us']:.0f} | {s['p99_us']:.0f} | {s['min_us']:.0f} | {s['oneway_msgs_per_s']:,.0f} | {s['oneway_MBps']:.1f} |")
        else:
            lines.append(f"| {s['transport']} | {s['size']:,} B | — | 실패: {s['error']} | | | | | | |")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps({"env": info, "results": results}, ensure_ascii=False, indent=1, default=str))
    lines.append("```")
    text = "\n".join(lines)
    if args.out == "-":
        print(text)
    else:
        with open(args.out, "w") as f:
            f.write(text + "\n")
        print(f"saved: {args.out}", file=sys.stderr)


if __name__ == "__main__":
    mp.set_start_method("spawn")
    main()
