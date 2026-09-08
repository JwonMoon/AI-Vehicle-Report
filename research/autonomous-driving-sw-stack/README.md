# 자율주행 SW Stack 파헤치기

> **작성일**: 2026-09-08 · **상태**: 초판
> **목적**: 자율주행 소프트웨어 스택을 "한 층씩" 열어 보고, 오픈소스 풀스택 3종(Autoware·Apollo·openpilot)은 코드로, 학계·상용·중국 스택은 공개 자료로, 미들웨어 층은 실측으로 비교한다. 마지막에 차량용 HPC 개발 관점에서 "주의 깊게 볼 것"과 "사업을 위해 고려할 것"을 정리한다.

## 문서 목록

| 문서 | 내용 | 상태 |
|---|---|---|
| [autonomous-driving-sw-stack.md](autonomous-driving-sw-stack.md) | 보고서 원본 (사실 목록형, 모든 문장에 출처·등급) | 초판 |
| [autonomous-driving-sw-stack.html](autonomous-driving-sw-stack.html) | 웹 버전 (설명형, 자체 완결 페이지) | 초판 |
| [article.md](article.md) | 사내 공유용 블로그형 기사 (5분 분량) | 초판 |
| [scripts/](scripts/) | 데모 스크립트 — `autoware_anatomy.py` · `apollo_dag_graph.py` · `openpilot_onnx_probe.py` · `ipc_bench.py` | — |
| [reference/demo-logs/](reference/demo-logs/) | 데모 원시 출력 (실행일·커밋·환경 포함) | — |
| [reference/references.md](reference/references.md) · [reference/images.md](reference/images.md) | 출처 목록 · 이미지 출처 | — |

## 기존 문서와의 경계 (중복 방지)

| 주제 | 주인 문서 | 이 보고서에서는 |
|---|---|---|
| NVIDIA Alpamayo 모델·DRIVE AV·AlpaSim | [nvidia-fullstack 3장](../nvidia-fullstack/03-autonomous-driving-stack.md) · [nvidia-alpamayo](../nvidia-alpamayo/) | 스택 지도상의 위치와 지연 수치만 인용 |
| Alpamayo × Autoware 노드 코드 해부 | [tier4-alpamayo-autoware](../tier4-alpamayo-autoware/) | 0.600 s → 3.35 s 지연 수치만 인용 |
| VLA 온보드 추론 최적화 | [flashdrive](../flashdrive/) | 링크만 |
| 고전 파이프라인·모델 트렌드(BEV·Occupancy·E2E·VLA 개론) | [세미나 1회차](../../seminars/01-ad-workloads/material.md) | 개론은 링크, 이 문서는 스택 단위 비교 |
| SoC 비교·E/E 아키텍처·미들웨어 개요 | [세미나 2회차](../../seminars/02-hpc-platform/material.md) | 개요는 링크, 이 문서는 rmw·ara::com·Zenoh 심층 + 실측 |
| DriveOS·Halos | (nvidia-fullstack 2장, 미작성) | 3줄 언급 |

## 작성 규약

- **사실근거 원칙**: 모든 사실 문장에 인라인 출처와 등급을 붙인다.
  - 💻 저장소 코드·스크립트 출력에서 직접 확인 (파일:줄 또는 demo-logs 표기)
  - 🔍 1차 출처 원문 직접 확인 (README·LICENSE·공식 문서 raw)
  - ✅ 복수 출처 교차검증
  - 📰 웹 검색 요약·서드파티 보도만 (원문 미열람)
  - ⚠️ 미확인·추정
- **이미지**: 설명용 도식은 자체 SVG (실선 = 출처로 확인, 점선 = 추정). 외부 그림은 접근 가능한 1차 출처만 내려받고 [reference/images.md](reference/images.md)에 출처를 남긴다.
- **데모**: 샌드박스(CPU 4코어·GPU 없음)에서 실행한 것만 "실측"으로 표기하고, GPU가 필요한 항목은 부록 B에 재현 절차만 둔다. 원시 출력은 `reference/demo-logs/`에 그대로 둔다.
- **조사 환경 제약(2026-09-08)**: 세션 네트워크 정책상 arxiv.org·huggingface.co·nvidia.com·docs.ros.org·autosar.org·벤더 사이트(Tesla·Waymo·Wayve·Huawei·Momenta·XPeng·Mobileye) 원문에 직접 접근할 수 없었다. GitHub 저장소(clone·raw)·gitlab.com·PyPI·웹 검색 요약만 가능했으므로, 검색 요약에만 근거한 사실은 📰로 표시했다. Docker 데몬이 기동되지 않아 ROS 2 컨테이너 실측은 하지 못했다.
