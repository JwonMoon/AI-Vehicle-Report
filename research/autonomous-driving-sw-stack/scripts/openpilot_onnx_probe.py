#!/usr/bin/env python3
"""openpilot ONNX 모델 해부 + CPU 추론 지연 측정 (demo D3).

사용법:
  python3 openpilot_onnx_probe.py <model.onnx> [<model2.onnx> ...] \
      [--warmup 20] [--runs 200] [--threads 4,1] [--commit <hash>] [--out <log.md>]

각 ONNX에 대해 다음을 출력한다.
  - opset, IR 버전, producer
  - 입력/출력 이름·shape·dtype
  - 노드 수, 연산자 히스토그램(상위 15)
  - 파라미터(initializer) 수와 바이트 크기
  - onnxruntime CPU EP 지연 (intra_op_num_threads = 4, 1): warmup 후 N회, mean/median/p95/p99 ms
동기 입력(synthetic input)은 dtype을 존중한다 (uint8 이미지 입력 → 0~255 난수, float → 0~1 난수).
"""
import argparse
import collections
import datetime as dt
import hashlib
import os
import platform
import statistics
import subprocess
import sys
import time

import numpy as np
import onnx
import onnxruntime as ort
from onnx import TensorProto, shape_inference  # noqa: F401

DTYPE_MAP = {
    TensorProto.FLOAT: np.float32,
    TensorProto.FLOAT16: np.float16,
    TensorProto.UINT8: np.uint8,
    TensorProto.INT8: np.int8,
    TensorProto.INT32: np.int32,
    TensorProto.INT64: np.int64,
    TensorProto.BOOL: np.bool_,
    TensorProto.DOUBLE: np.float64,
}


def tensor_type_str(tt):
    dtype = TensorProto.DataType.Name(tt.elem_type)
    dims = []
    for d in tt.shape.dim:
        if d.HasField("dim_value"):
            dims.append(str(d.dim_value))
        elif d.HasField("dim_param"):
            dims.append(d.dim_param)
        else:
            dims.append("?")
    return dtype, dims


def shape_for_input(tt, batch=1):
    _, dims = tensor_type_str(tt)
    out = []
    for d in dims:
        if d.isdigit():
            out.append(int(d))
        else:
            out.append(batch)
    return out


def cpu_model():
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unknown"


def uptime():
    try:
        return subprocess.check_output(["uptime"], text=True).strip()
    except Exception:
        return "n/a"


def sha256_of(path, bufsize=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(bufsize)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def analyze(path, lines):
    model = onnx.load(path, load_external_data=True)
    g = model.graph
    opsets = {(o.domain or "ai.onnx"): o.version for o in model.opset_import}
    lines.append(f"### `{os.path.basename(path)}`\n")
    lines.append(f"- 파일 크기: {os.path.getsize(path):,} bytes ({os.path.getsize(path)/1e6:.1f} MB)")
    lines.append(f"- sha256: `{sha256_of(path)}`")
    lines.append(f"- IR version: {model.ir_version}, producer: {model.producer_name} {model.producer_version}")
    lines.append(f"- opset: {opsets}")

    init_names = {t.name for t in g.initializer}
    n_params = 0
    n_bytes = 0
    dtype_hist = collections.Counter()
    for t in g.initializer:
        cnt = int(np.prod(t.dims)) if len(t.dims) else 1
        n_params += cnt
        n_bytes += cnt * np.dtype(DTYPE_MAP.get(t.data_type, np.float32)).itemsize
        dtype_hist[TensorProto.DataType.Name(t.data_type)] += cnt
    lines.append(f"- 파라미터 수: {n_params:,} ({n_params/1e6:.2f} M), initializer 바이트: {n_bytes:,} ({n_bytes/1e6:.1f} MB)")
    lines.append(f"- initializer dtype 분포: {dict(dtype_hist)}")

    lines.append(f"- 노드 수: {len(g.node)}")
    op_hist = collections.Counter(n.op_type for n in g.node)
    lines.append("\n**연산자 히스토그램 (상위 15)**\n")
    lines.append("| op | count |\n|---|---|")
    for op, c in op_hist.most_common(15):
        lines.append(f"| {op} | {c} |")
    lines.append(f"\n(고유 연산자 {len(op_hist)}종)\n")

    lines.append("**입력**\n")
    lines.append("| name | dtype | shape | elements |\n|---|---|---|---|")
    inputs = [i for i in g.input if i.name not in init_names]
    for i in inputs:
        dtype, dims = tensor_type_str(i.type.tensor_type)
        shp = shape_for_input(i.type.tensor_type)
        lines.append(f"| {i.name} | {dtype} | {dims} | {int(np.prod(shp)):,} |")
    lines.append("\n**출력**\n")
    lines.append("| name | dtype | shape |\n|---|---|---|")
    for o in g.output:
        dtype, dims = tensor_type_str(o.type.tensor_type)
        lines.append(f"| {o.name} | {dtype} | {dims} |")
    lines.append("")
    return model, inputs


def make_feed(inputs, rng):
    feed = {}
    for i in inputs:
        tt = i.type.tensor_type
        shp = shape_for_input(tt)
        npdt = DTYPE_MAP.get(tt.elem_type, np.float32)
        if npdt == np.uint8:
            feed[i.name] = rng.integers(0, 256, size=shp, dtype=np.uint8)
        elif npdt in (np.int8,):
            feed[i.name] = rng.integers(-128, 128, size=shp, dtype=np.int8)
        elif npdt in (np.int32, np.int64):
            feed[i.name] = np.zeros(shp, dtype=npdt)
        elif npdt == np.bool_:
            feed[i.name] = np.zeros(shp, dtype=np.bool_)
        else:
            feed[i.name] = rng.random(size=shp).astype(npdt)
    return feed


def bench(path, inputs, threads, warmup, runs, lines):
    so = ort.SessionOptions()
    so.intra_op_num_threads = threads
    so.inter_op_num_threads = 1
    so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    so.log_severity_level = 3
    t0 = time.perf_counter()
    sess = ort.InferenceSession(path, so, providers=["CPUExecutionProvider"])
    load_ms = (time.perf_counter() - t0) * 1e3
    rng = np.random.default_rng(0)
    feed = make_feed(inputs, rng)
    # 세션이 실제로 요구하는 입력만 남긴다 (일부 그래프 입력은 optional일 수 있음)
    wanted = {i.name for i in sess.get_inputs()}
    feed = {k: v for k, v in feed.items() if k in wanted}
    for _ in range(warmup):
        sess.run(None, feed)
    ts = []
    for _ in range(runs):
        t = time.perf_counter()
        sess.run(None, feed)
        ts.append((time.perf_counter() - t) * 1e3)
    ts_sorted = sorted(ts)
    p = lambda q: ts_sorted[min(len(ts_sorted) - 1, int(round(q * (len(ts_sorted) - 1))))]
    row = {
        "threads": threads,
        "load_ms": load_ms,
        "mean": statistics.mean(ts),
        "median": statistics.median(ts),
        "p95": p(0.95),
        "p99": p(0.99),
        "min": ts_sorted[0],
        "max": ts_sorted[-1],
    }
    lines.append(
        f"| {os.path.basename(path)} | {threads} | {row['mean']:.1f} | {row['median']:.1f} | {row['p95']:.1f} | {row['p99']:.1f} | {row['min']:.1f} | {row['max']:.1f} | {1000/row['mean']:.1f} | {load_ms:.0f} |"
    )
    del sess
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("models", nargs="+")
    ap.add_argument("--warmup", type=int, default=20)
    ap.add_argument("--runs", type=int, default=200)
    ap.add_argument("--threads", default="4,1")
    ap.add_argument("--commit", default=os.environ.get("OPENPILOT_COMMIT", "unknown"))
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    threads = [int(t) for t in args.threads.split(",")]

    lines = []
    lines.append("# D3 — openpilot ONNX 모델 해부 + CPU 추론 프로브 로그\n")
    lines.append(f"- 실행 일시: {dt.datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"- openpilot commit: `{args.commit}`")
    lines.append(f"- onnx {onnx.__version__}, onnxruntime {ort.__version__} (providers: {ort.get_available_providers()}), numpy {np.__version__}, python {platform.python_version()}")
    lines.append(f"- CPU: {cpu_model()}, 논리 코어 {os.cpu_count()}, platform {platform.platform()}")
    lines.append(f"- uptime/부하 (측정 시작 시): `{uptime()}`")
    lines.append("- 주의: 이 머신은 다른 작업과 공유 중이라 수치는 **참고용(indicative)** 이다. 합성(난수) 입력이므로 출력 값 자체는 의미 없다.")
    lines.append("")

    parsed = []
    lines.append("## 1. 모델 구조\n")
    for m in args.models:
        model, inputs = analyze(m, lines)
        parsed.append((m, inputs))

    lines.append("## 2. CPU 추론 지연 (onnxruntime CPUExecutionProvider)\n")
    lines.append(f"warmup {args.warmup}회 후 {args.runs}회 측정, inter_op=1, graph_opt=ALL, 배치 1.\n")
    lines.append("| model | intra_op threads | mean ms | median ms | p95 ms | p99 ms | min ms | max ms | ≈FPS(1/mean) | session load ms |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for m, inputs in parsed:
        for t in threads:
            print(f"[bench] {os.path.basename(m)} threads={t} ...", file=sys.stderr, flush=True)
            try:
                bench(m, inputs, t, args.warmup, args.runs, lines)
            except Exception as e:  # noqa: BLE001
                lines.append(f"| {os.path.basename(m)} | {t} | FAIL: {type(e).__name__}: {str(e)[:120]} | | | | | | | |")
    lines.append("")
    lines.append(f"- uptime/부하 (측정 종료 시): `{uptime()}`")

    text = "\n".join(lines) + "\n"
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w") as f:
            f.write(text)
        print(f"wrote {args.out}", file=sys.stderr)
    print(text)


if __name__ == "__main__":
    main()
