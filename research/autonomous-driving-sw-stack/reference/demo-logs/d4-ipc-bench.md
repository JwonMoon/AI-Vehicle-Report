# D4 — 동일 호스트 IPC 마이크로벤치 (Zenoh vs CycloneDDS vs 파이프 기준선)

- 실행일: 2026-09-08 01:57:38 UTC
- 환경: Python 3.11.15 · Linux-6.18.44-fc-v24-x86_64-with-glibc2.39 · CPU Intel(R) Xeon(R) Processor @ 2.80GHz × 4 · loadavg (0.0498046875, 0.197265625, 0.10791015625)
- 버전: {'eclipse-zenoh': '1.10.1', 'cyclonedds': '11.0.1'}
- 명령: `/home/user/AI-Vehicle-Research/research/autonomous-driving-sw-stack/scripts/ipc_bench.py --sizes 64,4096,65536,1048576 --n 1000 --warmup 50 --transports pipe,zenoh,cyclonedds --out /home/user/AI-Vehicle-Research/research/autonomous-driving-sw-stack/reference/demo-logs/d4-ipc-bench.md`
- 방법: ping 프로세스가 페이로드를 발행하고 pong 프로세스가 같은 크기로 되돌려 보내는 왕복 지연(RTT). 워밍업 50회 제외, 샘플 1000회(1 MB는 1/5). 파이프는 multiprocessing.Pipe(바이트) 기준선. Zenoh는 peer 모드 기본 설정, CycloneDDS는 Reliable·KeepLast(16), sequence<uint8> IDL(파이썬 리스트 직렬화 포함). **Python 바인딩·GIL 오버헤드가 포함된 수치이므로 절대치가 아닌 상대 비교용.**

| 전송 | 페이로드 | n | 평균 RTT(µs) | 중앙값 | p95 | p99 | 최소 | 단방향 msg/s | 단방향 MB/s |
|---|---|---|---|---|---|---|---|---|---|
| pipe | 64 B | 1000 | 76 | 73 | 90 | 129 | 59 | 26,192 | 1.7 |
| pipe | 4,096 B | 1000 | 96 | 92 | 114 | 156 | 76 | 20,925 | 85.7 |
| pipe | 65,536 B | 1000 | 163 | 155 | 210 | 248 | 114 | 12,233 | 801.7 |
| pipe | 1,048,576 B | 200 | 1968 | 1840 | 2862 | 3405 | 1290 | 1,016 | 1065.5 |
| zenoh | 64 B | 1000 | 280 | 270 | 352 | 422 | 238 | 7,140 | 0.5 |
| zenoh | 4,096 B | 1000 | 319 | 300 | 413 | 532 | 251 | 6,270 | 25.7 |
| zenoh | 65,536 B | 1000 | 405 | 377 | 607 | 757 | 267 | 4,938 | 323.6 |
| zenoh | 1,048,576 B | 200 | 1285 | 1284 | 1462 | 1548 | 1016 | 1,556 | 1631.7 |
| cyclonedds | 64 B | 1000 | 232 | 224 | 315 | 373 | 177 | 8,605 | 0.6 |
| cyclonedds | 4,096 B | 1000 | 584 | 567 | 726 | 815 | 461 | 3,426 | 14.0 |
| cyclonedds | 65,536 B | 1000 | 6600 | 6435 | 8042 | 9232 | 5119 | 303 | 19.9 |
| cyclonedds | 1,048,576 B | 200 | 113546 | 111368 | 123231 | 167557 | 99846 | 18 | 18.5 |

```json
{
 "env": {
  "date": "2026-09-08 01:57:38 UTC",
  "python": "3.11.15",
  "platform": "Linux-6.18.44-fc-v24-x86_64-with-glibc2.39",
  "cpu": "Intel(R) Xeon(R) Processor @ 2.80GHz",
  "ncpu": 4,
  "loadavg_1_5_15": [
   0.0498046875,
   0.197265625,
   0.10791015625
  ],
  "versions": {
   "eclipse-zenoh": "1.10.1",
   "cyclonedds": "11.0.1"
  }
 },
 "results": [
  {
   "n": 1000,
   "mean_us": 76.360001,
   "median_us": 73.3875,
   "p95_us": 90.0553,
   "p99_us": 129.36956999999998,
   "min_us": 58.588,
   "max_us": 172.026,
   "transport": "pipe",
   "size": 64,
   "ok": true,
   "oneway_msgs_per_s": 26191.723072397548,
   "oneway_MBps": 1.676270276633443
  },
  {
   "n": 1000,
   "mean_us": 95.58069400000001,
   "median_us": 91.7795,
   "p95_us": 113.65854999999996,
   "p99_us": 156.15524,
   "min_us": 75.513,
   "max_us": 226.664,
   "transport": "pipe",
   "size": 4096,
   "ok": true,
   "oneway_msgs_per_s": 20924.727748890375,
   "oneway_MBps": 85.70768485945497
  },
  {
   "n": 1000,
   "mean_us": 163.496426,
   "median_us": 155.2175,
   "p95_us": 210.46465,
   "p99_us": 247.66313,
   "min_us": 113.765,
   "max_us": 314.531,
   "transport": "pipe",
   "size": 65536,
   "ok": true,
   "oneway_msgs_per_s": 12232.683300367678,
   "oneway_MBps": 801.6811327728961
  },
  {
   "n": 200,
   "mean_us": 1968.280955,
   "median_us": 1839.5495,
   "p95_us": 2862.108599999999,
   "p99_us": 3404.517649999998,
   "min_us": 1290.257,
   "max_us": 5383.724,
   "transport": "pipe",
   "size": 1048576,
   "ok": true,
   "oneway_msgs_per_s": 1016.1151002957299,
   "oneway_MBps": 1065.4739074076954
  },
  {
   "n": 1000,
   "mean_us": 280.116798,
   "median_us": 269.94100000000003,
   "p95_us": 351.85229999999996,
   "p99_us": 422.39063,
   "min_us": 237.874,
   "max_us": 612.771,
   "transport": "zenoh",
   "size": 64,
   "ok": true,
   "oneway_msgs_per_s": 7139.878844395472,
   "oneway_MBps": 0.4569522460413102
  },
  {
   "n": 1000,
   "mean_us": 318.978322,
   "median_us": 300.2375,
   "p95_us": 412.61084999999997,
   "p99_us": 531.90926,
   "min_us": 250.971,
   "max_us": 4512.185,
   "transport": "zenoh",
   "size": 4096,
   "ok": true,
   "oneway_msgs_per_s": 6270.018562578055,
   "oneway_MBps": 25.681996032319713
  },
  {
   "n": 1000,
   "mean_us": 405.057156,
   "median_us": 376.6555,
   "p95_us": 607.0096499999999,
   "p99_us": 757.2390699999999,
   "min_us": 267.389,
   "max_us": 1132.81,
   "transport": "zenoh",
   "size": 65536,
   "ok": true,
   "oneway_msgs_per_s": 4937.574785124892,
   "oneway_MBps": 323.5889011179449
  },
  {
   "n": 200,
   "mean_us": 1285.274975,
   "median_us": 1284.1554999999998,
   "p95_us": 1462.3068999999998,
   "p99_us": 1547.667,
   "min_us": 1015.689,
   "max_us": 1621.153,
   "transport": "zenoh",
   "size": 1048576,
   "ok": true,
   "oneway_msgs_per_s": 1556.087248956201,
   "oneway_MBps": 1631.6757431614974
  },
  {
   "n": 1000,
   "mean_us": 232.41154500000002,
   "median_us": 224.148,
   "p95_us": 315.41194999999993,
   "p99_us": 373.06645999999995,
   "min_us": 176.682,
   "max_us": 892.574,
   "transport": "cyclonedds",
   "size": 64,
   "ok": true,
   "oneway_msgs_per_s": 8605.424485259542,
   "oneway_MBps": 0.5507471670566106
  },
  {
   "n": 1000,
   "mean_us": 583.7802399999999,
   "median_us": 567.356,
   "p95_us": 726.3467,
   "p99_us": 814.6280299999999,
   "min_us": 460.982,
   "max_us": 1425.863,
   "transport": "cyclonedds",
   "size": 4096,
   "ok": true,
   "oneway_msgs_per_s": 3425.9467226914026,
   "oneway_MBps": 14.032677776143984
  },
  {
   "n": 1000,
   "mean_us": 6599.990283,
   "median_us": 6434.8195,
   "p95_us": 8041.7962,
   "p99_us": 9231.884729999998,
   "min_us": 5118.709,
   "max_us": 23838.916,
   "transport": "cyclonedds",
   "size": 65536,
   "ok": true,
   "oneway_msgs_per_s": 303.03074917421054,
   "oneway_MBps": 19.859423177881062
  },
  {
   "n": 200,
   "mean_us": 113545.88167999999,
   "median_us": 111368.3945,
   "p95_us": 123230.91319999998,
   "p99_us": 167556.88808999935,
   "min_us": 99845.98,
   "max_us": 245786.645,
   "transport": "cyclonedds",
   "size": 1048576,
   "ok": true,
   "oneway_msgs_per_s": 17.614025012694764,
   "oneway_MBps": 18.469643891711424
  }
 ]
}
```
