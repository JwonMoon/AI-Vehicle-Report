# 이미지 출처 목록

> 작성일 2026-09-08. images/ 폴더의 모든 파일과 출처·사용 위치.

## 자체 작성 (SVG)

| 파일 | 설명 | 근거 데이터 | 사용 문서 |
|---|---|---|---|
| `stack-map.svg` | 자율주행 SW 스택 8층 지도(L1 HW~L8 API). 왼쪽 열 모듈형 스택(Autoware·Apollo·openpilot) 실제 구성요소, 오른쪽 열 E2E/VLA에서 달라지는 점 | 보고서 §1.1 표(층 정의는 이 보고서 자체 정의); D1~D3 정적 측정(demo-logs/d1·d2·d3), 8장 미들웨어 노트 | `autonomous-driving-sw-stack.md` 그림 1, §1.1 |
| `stack-matrix.svg` | 열두 스택 × 여덟 축(아키텍처·미들웨어·OS·SoC·센서·안전·데이터·공개도) 히트맵. 색이 진할수록 공개 자료로 확인된 정도가 높음 | 보고서 §3 비교표(각 셀의 등급 💻🔍📰⚠️); references.md §2.1~2.5 | `autonomous-driving-sw-stack.md` 그림 2, §3 |
| `three-stack-anatomy.svg` | Autoware·Apollo·openpilot 조립 방식 비교 — 파이프라인·프로세스·IPC·스케줄링·안전층 | D1~D3 demo-logs: `reference/demo-logs/d1-autoware-anatomy.md`(365 pkgs·287 노드 등록·런치 167노드·Agnocast/cuda_blackboard), `d2-apollo-anatomy.md`(dag 109·컴포넌트 188·INTRA/SHM/RTPS·prio 20단계), `d3-openpilot-onnx.md`(프로세스 44·서비스 69·30M 파라미터·msgq/VisionIPC) | `autonomous-driving-sw-stack.md` 그림 3, §4 |
| `e2e-lineage.svg` | 학계 오픈 E2E 스택 계보(TransFuser→UniAD/VAD→NAVSIM→DiffusionDrive→VLA·월드모델·RL)와 벤치마크 전환 | 5장 노트 계보 표·모델 비교표(각 README raw 🔍 및 논문 스니펫 📰); references.md P35~P54, A1~A17 | `autonomous-driving-sw-stack.md` 그림 4, §5 |
| `middleware-landscape.svg` | 미들웨어·OS 층 지형 — ROS 2 rmw 계열(Fast DDS·Cyclone·Connext·Zenoh·iceoryx·Agnocast), 자체 미들웨어(Cyber RT·msgq), AUTOSAR Adaptive 계열(ara::com·vsomeip·LoLa), SDV 프레임워크(SOAFEE·S-CORE), OS/하이퍼바이저(QNX 8·DriveOS·Linux). 인증 상태와 zero-copy 범위 표시 | 8장 노트(클론 문서 💻: rmw_zenoh design.md·agnocast docs·score ipc architecture·vsomeip README·SOAFEE architecture.rst; 인증은 📰); references.md C18~C39, N40~N46 | `autonomous-driving-sw-stack.md` 그림 5, §8 |
| `ipc-latency-bench.svg` | D4 실측 평균 RTT 막대(로그 스케일, pipe·Zenoh·CycloneDDS × 64 B/4 KB/64 KB/1 MB)와 문헌 수치(iceoryx2·iRobot·Agnocast) 병기 | `reference/demo-logs/d4-ipc-bench.md`(2026-09-08, Xeon 4코어, eclipse-zenoh 1.10.1·cyclonedds 11.0.1, Python 바인딩 포함); 문헌은 references.md C21·C35·P23 | `autonomous-driving-sw-stack.md` 그림 6, §8.3 |

규약: 실선 = 출처로 확인, 점선 = 추정·유동. 외부 그림은 내려받지 않음(접근 차단).
