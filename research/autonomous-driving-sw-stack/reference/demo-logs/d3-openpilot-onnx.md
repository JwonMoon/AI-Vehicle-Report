# D3 — openpilot ONNX 모델 해부 + CPU 추론 프로브 로그

- 실행 일시: 2026-09-08T01:31:30
- openpilot commit: `3eafb658bf3e12fa2e515958aa641fd5a99fdf67`
- onnx 1.22.0, onnxruntime 1.29.0 (providers: ['AzureExecutionProvider', 'CPUExecutionProvider']), numpy 2.4.6, python 3.11.15
- CPU: Intel(R) Xeon(R) Processor @ 2.80GHz, 논리 코어 4, platform Linux-6.18.44-fc-v24-x86_64-with-glibc2.39
- uptime/부하 (측정 시작 시): `01:31:30 up 30 min,  0 user,  load average: 1.20, 0.53, 0.25`
- 주의: 이 머신은 다른 작업과 공유 중이라 수치는 **참고용(indicative)** 이다. 합성(난수) 입력이므로 출력 값 자체는 의미 없다.

## 1. 모델 구조

### `driving_supercombo.onnx`

- 파일 크기: 60,881,999 bytes (60.9 MB)
- sha256: `659727c4d4839adc4992a254409a54259a8756a743f2d567bf5fdc6579f8009b`
- IR version: 10, producer: onnx.compose.merge_models 1.0
- opset: {'ai.onnx': 20}
- 파라미터 수: 30,003,321 (30.00 M), initializer 바이트: 60,006,795 (60.0 MB)
- initializer dtype 분포: {'FLOAT16': 30003201, 'INT64': 39, 'BOOL': 81}
- 노드 수: 351

**연산자 히스토그램 (상위 15)**

| op | count |
|---|---|
| Gemm | 82 |
| Relu | 64 |
| Conv | 60 |
| Add | 47 |
| Gelu | 20 |
| Mul | 19 |
| MatMul | 8 |
| Concat | 5 |
| Reshape | 5 |
| Transpose | 5 |
| Sigmoid | 4 |
| Slice | 4 |
| Div | 3 |
| Identity | 3 |
| Squeeze | 3 |

(고유 연산자 27종)

**입력**

| name | dtype | shape | elements |
|---|---|---|---|
| img | UINT8 | ['1', '12', '128', '256'] | 393,216 |
| big_img | UINT8 | ['1', '12', '128', '256'] | 393,216 |
| features_buffer | FLOAT16 | ['1', '24', '512'] | 12,288 |
| desire_pulse | FLOAT16 | ['1', '25', '8'] | 200 |
| traffic_convention | FLOAT16 | ['1', '2'] | 2 |
| action_t | FLOAT16 | ['1', '2'] | 2 |

**출력**

| name | dtype | shape |
|---|---|---|
| outputs | FLOAT16 | ['1', '2576'] |

### `dmonitoring_model.onnx`

- 파일 크기: 7,497,335 bytes (7.5 MB)
- sha256: `dd299afabe7a3e0d04cbe2bd97fdb0c93bba8ad6d3cc3663a0e0ededaf243ac2`
- IR version: 10, producer: pytorch 2.13.0+cu130
- opset: {'ai.onnx': 20}
- 파라미터 수: 3,438,288 (3.44 M), initializer 바이트: 6,876,672 (6.9 MB)
- initializer dtype 분포: {'FLOAT16': 3438272, 'INT64': 16}
- 노드 수: 201

**연산자 히스토그램 (상위 15)**

| op | count |
|---|---|
| Gemm | 53 |
| Conv | 46 |
| Relu | 39 |
| Gelu | 30 |
| Add | 10 |
| Slice | 10 |
| Reshape | 3 |
| Cast | 2 |
| Transpose | 2 |
| Concat | 2 |
| Sub | 1 |
| Mul | 1 |
| Div | 1 |
| ReduceMean | 1 |

(고유 연산자 14종)

**입력**

| name | dtype | shape | elements |
|---|---|---|---|
| input_img | UINT8 | ['1', '1382400'] | 1,382,400 |
| calib | FLOAT | ['1', '3'] | 3 |

**출력**

| name | dtype | shape |
|---|---|---|
| outputs | FLOAT16 | ['1', '553'] |

## 2. CPU 추론 지연 (onnxruntime CPUExecutionProvider)

warmup 20회 후 200회 측정, inter_op=1, graph_opt=ALL, 배치 1.

| model | intra_op threads | mean ms | median ms | p95 ms | p99 ms | min ms | max ms | ≈FPS(1/mean) | session load ms |
|---|---|---|---|---|---|---|---|---|---|
| driving_supercombo.onnx | 4 | 395.5 | 390.2 | 430.5 | 478.9 | 376.6 | 495.6 | 2.5 | 578 |
| driving_supercombo.onnx | 1 | 405.5 | 404.5 | 416.4 | 432.9 | 396.0 | 460.4 | 2.5 | 361 |
| dmonitoring_model.onnx | 4 | 56.4 | 48.7 | 97.6 | 103.6 | 42.5 | 107.0 | 17.7 | 143 |
| dmonitoring_model.onnx | 1 | 49.2 | 48.6 | 53.2 | 61.4 | 44.3 | 76.4 | 20.3 | 130 |

- uptime/부하 (측정 종료 시): `01:34:52 up 33 min,  0 user,  load average: 2.16, 1.41, 0.68`
