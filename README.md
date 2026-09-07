# AI-Vehicle-Research

차량용 AI(자율주행·차량 HPC·모빌리티 데이터 생태계) 관련 리서치, 스터디 세미나, 뉴스 다이제스트 아카이브.

## 구조

```
├── seminars/    # 사내 자율주행 스터디 세미나 자료
├── research/    # 주제별 심층 리서치 보고서
└── news/        # 데일리 AI 뉴스 다이제스트
```

## seminars — 자율주행 스터디

차량용 HPC 아키텍처 설계 관점의 자율주행/ADAS 스터디. → [개요](seminars/README.md)

| 회차 | 주제 | 자료 |
|---|---|---|
| ⭐ 통합 | 자율주행 기술 + 차량용 HPC 아키텍처 통합 보고서 | [report.html](seminars/full-report/report.html) |
| 1 | 자율주행 AD 워크로드 | [material](seminars/01-ad-workloads/material.md) · [slides](seminars/01-ad-workloads/slides.html) |
| 2 | 차량용 HPC 플랫폼 | [material](seminars/02-hpc-platform/material.md) · [slides](seminars/02-hpc-platform/slides.html) |

## research — 주제별 심층 리서치

| 주제 | 요약 | 작성 | 핵심 문서 |
|---|---|---|---|
| [tier4-alpamayo-autoware](research/tier4-alpamayo-autoware/) | TIER IV × NVIDIA 협력의 실체 — Alpamayo 1.5 VLA를 Autoware에 얹은 ROS 2 노드 코드 해부, 0.600s/1.67FPS 지연 현실, Cosmos × Co-MLOps 데이터 축, Isuzu L4 버스 트랙 | 2026-09 | [보고서](research/tier4-alpamayo-autoware/tier4_alpamayo_autoware_보고서.md) · [웹 버전](research/tier4-alpamayo-autoware/tier4_alpamayo_autoware_보고서.html) · [출처 기록](research/tier4-alpamayo-autoware/reference/references.md) |
| [aumovio-sensor-cleaning](research/aumovio-sensor-cleaning/) | AUMOVIO 광학 센서 세정 시스템 기술 해부 — Coanda 라이다·카메라 노즐, 유체 공급 체인, SOTIF 관점, CERTINA 매각 분석 | 2026-09 | [보고서](research/aumovio-sensor-cleaning/aumovio-sensor-cleaning.md) · [웹 버전](research/aumovio-sensor-cleaning/aumovio-sensor-cleaning.html) |
| [flashdrive](research/flashdrive/) | Z Lab(UCSD)의 자율주행 VLA 추론 4.5× 가속 논문 분석 — Alpamayo 1.5를 716→159ms로 | 2026-09 | [분석 보고서](research/flashdrive/flashdrive_analysis.md) |
| [nvidia-alpamayo](research/nvidia-alpamayo/) | NVIDIA Alpamayo(추론형 주행 VLA)와 자율주행 패러다임 전환 — 종합·1vs2 비교·SW/HW 요구사항 | 2026-07 | [종합 보고서](research/nvidia-alpamayo/alpamayo_종합보고서.md) · [1 vs 2 비교](research/nvidia-alpamayo/alpamayo_1_vs_2_비교보고서.md) · [SW/HW 요구사항](research/nvidia-alpamayo/alpamayo_sw_hw_요구사항.md) |
| [tractus-x](research/tractus-x/) | Eclipse Tractus-X — Catena-X 자동차 데이터 스페이스 오픈소스 조사 | 2026-07 | [보고서](research/tractus-x/tractus-x-report.md) · [상세 자료집](research/tractus-x/tractus-x-research.md) |
| [liquid-ai](research/liquid-ai/) | Liquid AI 기업 조사 — 리퀴드 신경망 기반 엣지 AI 스타트업 | 2026-06 | [보고서](research/liquid-ai/liquid_ai_research.md) |

각 주제 폴더 구성: 보고서 `.md`(원본) · `.html`(웹 버전, 있는 경우) · `images/`·`assets/`(그림) · `reference/`(출처·자막·원시 수집 자료).

## news — 데일리 다이제스트

| 날짜 | 문서 |
|---|---|
| 2026-06-08 | [NVIDIA 관련 5건](news/2026-06-08-nvidia.md) · [상세 HTML](news/2026-06-08-nvidia-detailed.html) |
