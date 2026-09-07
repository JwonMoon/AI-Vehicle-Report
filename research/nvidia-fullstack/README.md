# NVIDIA 차량용 풀스택 소프트웨어 조사

> **작성일**: 2026-09-02 · **상태**: 3장·7장·부록 A 초판 완료(📄 등급 출처의 원문 재확인은 후속 과제), 나머지 장은 다른 담당자 작성 예정
> **목적**: NVIDIA가 차량(자율주행·ADAS)용으로 제공하는 하드웨어부터 에이전틱 AI까지 풀스택을 7개 장으로 나눠 조사하고, 마지막에 "Tier-1이 NVIDIA 위에서 무엇을 더 만들어야 하는가"를 정리한다.

## 문서 목록

| 장 | 문서 | 담당 | 상태 |
|---|---|---|---|
| 1. 차량 플랫폼 HW | (예정) | 팀 | 미작성 |
| 2. DriveOS / Halos | (예정) | 팀 | 미작성 |
| **3. 자율주행 스택** | [03-autonomous-driving-stack.md](03-autonomous-driving-stack.md) | 본 폴더 작성자 | ✅ 초판 |
| 4. AI 학습 스택 | (예정) | 팀 | 미작성 |
| 5. AI 추론 스택 | (예정) | 팀 | 미작성 |
| 6. 에이전틱 AI 스택 | (예정) | 팀 | 미작성 |
| **7. Physical AI / Cosmos** | [07-physical-ai-cosmos.md](07-physical-ai-cosmos.md) | 본 폴더 작성자 | ✅ 초판 |
| **부록 A. Tier-1 관점 작업 범위** | [appendix-a-tier1-workscope.md](appendix-a-tier1-workscope.md) | 본 폴더 작성자 | ✅ 초판 |
| 출처 목록 | [reference/references.md](reference/references.md) · [reference/images.md](reference/images.md) | — | ✅ |
| **3장 보고서 (HTML)** | [report-03-autonomous-driving-stack.html](report-03-autonomous-driving-stack.html) — Alpamayo↔DRIVE AV 관계를 맨 앞에 두고, 핵심 타임라인 4개·버전 비교표 5행·"Alpamayo만 특별한 학습" 3가지·도입 사례를 명확한 순서(풀스택 양산 → 계약 → 칩+OS → 칩만 → 불분명)로 정리한 설명형 보고서. AlpaSim(폐루프 시뮬레이터)·AlpaGym(강화학습 하니스) 절과 자사 관점 절(특이사항·LG전자 VS와의 접점·협업 고려사항) 포함 | 본 폴더 작성자 | ✅ |
| **7장 보고서 (HTML)** | [report-07-physical-ai-cosmos.html](report-07-physical-ai-cosmos.html) — 세계 모델 개념, Cosmos 세대별 이야기(1→2→2.5→Cosmos 3, 비교표는 접힘), 데이터 파이프라인, Omniverse vs Cosmos 역할 구분, 활용 패턴 A~D("언제·누가·주의"), 채택사·한계·성숙도. 각 부 앞에 개념 절(Cosmos란 무엇인가, Omniverse란 무엇인가, 데이터 파이프라인·활용 패턴 개념) 포함. Cosmos 세대 비교 도식(1 → 2·2.5 → 3 입력·모델·출력, 그림 6), NuRec 파이프라인 도식(NCore → NRE → USDZ → serve-grpc → 시뮬레이터, 그림 11), 자사 관점 절(특이사항·LG전자 VS와의 접점 지도·협업 고려사항·결정 항목) 포함 | 본 폴더 작성자 | ✅ |
| **부록 A 보고서 (HTML)** | [report-appendix-a-tier1.html](report-appendix-a-tier1.html) — Android 대입표, 11개 계층별 "NVIDIA가 주는 것 / Tier-1이 해야 할 일" 카드, 차별화 매트릭스, 실제 Tier-1 사례, 세 가지 결론 | 본 폴더 작성자 | ✅ |

세 HTML은 같은 사이드바·등급 표기를 쓰고 서로 링크된다. 각 문서 상단에 "3분 요약"과 "읽기 전에(등급·조사 제약·필요 용어)"가 있다. 사실·수치·출처는 md 원본과 동일하며, 본문에서 줄인 세부(커밋 단위 타임라인, 이력 토큰 수, 학습 레시피 수치 등)는 각 절 끝의 "md 원본 §번호" 링크와 출처 절의 접힌 목록으로 이어진다. md 3종은 사실 목록 형식의 조사 원본이다.

## 팀 합의 전체 목차

1. **차량 플랫폼 HW** — 1.1 DRIVE AGX Thor · 1.2 DRIVE Hyperion 10
2. **DriveOS / Halos** — 2.1 DriveOS 7 · 2.2 인증 현황 3구분 · 2.3 Halos 3계층 · 2.4 Halos Workflow / Safety Evaluation Framework
3. **자율주행 스택** — 3.1 Alpamayo · 3.2 DRIVE AV 구성
4. **AI 학습 스택** — 4.1 CUDA 계층 구조 · 4.2 CUDA-X 기능 분류 · 4.3 Nemotron 3 아키텍처 · 4.4 공개 산출물 범위 · 4.5 NeMo 구성요소 · 4.6 Framework와 microservices 구분
5. **AI 추론 스택** — 5.1 계층 역할 · 5.2 오픈소스 엔진과의 구조 관계
6. **에이전틱 AI 스택** — 6.1 OpenClaw · 6.2 NemoClaw · 6.3 OpenShell · 6.4 실행 인프라 · 6.5 에이전트 평가 방법
7. **Physical AI / Cosmos** — 7.1 Cosmos 세대 · 7.2 데이터 파이프라인 · 7.3 Omniverse와의 역할 구분 · 7.4 활용 패턴

## 장 간 경계 규칙 (중복 방지)

| 주제 | 주인 장 | 3·7장에서는 |
|---|---|---|
| Thor/Orin SoC·Hyperion 센서 사양 | 1장 | 스택이 그것을 "어떻게 소비하는가"만 |
| DriveOS·하이퍼바이저·Halos 정의·ISO 인증 | 2장 | 런타임 이중화·가드레일 관점만 참조 |
| CUDA/CUDA-X·NeMo·Nemotron 일반 | 4장 | Cosmos Curator 등 Physical AI 특화 사용만 |
| TensorRT/Triton/NIM 일반 | 5장 | 온보드 지연·양자화 등 도메인 특화 수치만 |
| 차량 내 LLM 에이전트 | 6장 | 언급하지 않음 |

## 작성 규약

- **사실근거 원칙**: 모든 사실 문장에 인라인 출처 `([출처](url))`와 검증 등급을 붙인다. 등급: ✅ 두 출처 교차검증 · 🔍 1차 출처 원문 확인 · 📄 검색 요약·2차 출처만 · ⚠️ 미확인/추정.
- **이미지**: GitHub 등 접근 가능한 1차 출처의 그림은 `images/`에 내려받아 캡션에 출처를 남기고, 접근 불가한 그림은 링크만 남긴다. 설명용 도식은 자체 SVG로 그린다(실선 = 출처로 확인, 점선 = 추정). 목록: [reference/images.md](reference/images.md).
- **용어**: 처음 나오는 약어·전문 용어는 각주 `[^n]`로 설명하고 문서 끝 용어집에 모은다.
- **조사 환경 제약(2026-09-02)**: 조사 세션의 네트워크 정책상 nvidia.com·arxiv.org·huggingface.co·주요 언론사 페이지 원문에 직접 접근할 수 없었고, 웹 검색 요약과 GitHub 원문(README·모델카드·LICENSE)만 직접 확인 가능했다. 따라서 검색 요약에만 근거한 사실은 📄로 표시했으며, 후속 세션에서 원문 확인이 필요하다.
