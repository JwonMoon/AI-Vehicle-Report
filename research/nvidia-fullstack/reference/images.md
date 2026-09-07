# 이미지 출처 목록

> 작성일 2026-09-02. `images/` 폴더의 모든 파일과 출처·저작권·사용 위치. 외부 그림은 설명·인용 목적으로만 사용하며 원 저작권은 각 소유자에게 있다. 접근 불가(nvidia.com·arXiv)로 내려받지 못한 그림은 문서 본문에 링크만 남겼다.

## 자체 작성 (SVG)

| 파일 | 설명 | 사용 문서 |
|---|---|---|
| `3-0-av-stack-map-v2.svg` | NVIDIA 자율주행 스택 계층·3-computer 위치·성숙도 요약 지도 (현행판: 블록 안 챕터 표기 제거, 텍스트가 블록 안에 들어오도록 열 폭·줄바꿈 조정, 증류 경로를 블록 사이로 배선, 열 제목의 원 번호·상단 범례 제거, 파랑은 Alpamayo·DRIVE AV 블록만, 열 제목은 블록이 아닌 텍스트+밑줄, 블록 사이 화살표에 관계 라벨: 사전학습 백본 → 학습 레시피 → 모델 가중치, 학습 데이터, 합성·재구성 데이터, 폐루프 RL, 증류, 검증) | 3장 3.0.3 · report-03 그림 1 |
| `3-0-av-stack-map.svg` | 위 지도의 원판 (블록 안에 담당 장 표기 포함). 참고용으로 유지 | — |
| `3-3-alpagym-loop.svg` | AlpaGym 폐루프 강화학습 루프 도식: AlpaSim 환경(runtime·renderer·trafficsim·controller/physics·장면·eval) ↔ 정책(Alpamayo 1.5) gRPC 관측/궤적 루프, Cosmos-RL 학습기(롤아웃·채점·GRPO·가중치 동기화). NVlabs/alpagym README·ONBOARDING, NVlabs/alpasim DESIGN.md·data/scenes/README 기반 자체 작성 | 3장 3.3.4 · report-03 그림 5 |
| `3-1-alpamayo1-vs-2-architecture.svg` | Alpamayo 1(R1)과 2 Super의 추론 파이프라인 비교 도식. 공식 Alpamayo 1 그림은 arXiv·HF에만 있어 접근 불가, NVlabs/alpamayo·alpamayo2 저장소 코드를 읽어 자체 작성. 형식은 NVIDIA 공식 Alpamayo 2 Super 도식(입력 → 토큰 → 모델 상자[인코더·백본·Action Expert] → 토큰 → 출력)을 따라 세대별 2단 패널로 그리고, 2 Super에서 새로 생긴 입력·출력(자동 라벨 프롬프트, 메타액션·2D 그라운딩, 자동 라벨)은 NEW 태그, 1.5부터 생긴 것은 1.5+ 태그, 미지원은 점선 회색으로 표시 | 3장 3.1.2 · report-03 그림 3 |
| `7-0-cosmos-map-v2.svg` | Cosmos·Omniverse 위치·역할·성숙도 요약 지도 (현행판: 3장 v2와 같은 규칙 — 열 제목은 텍스트+밑줄·번호 없음, 초록=Cosmos·주황=Omniverse만 채색하고 Alpamayo·AlpaSim·데이터셋은 회색, 텍스트가 블록 안에 들어오도록 조정, 화살표마다 관계 라벨, 범례 줄 삭제) | 7장 7.0.3 · report-07 그림 1 |
| `7-0-cosmos-map.svg` | 위 지도의 원판 (열 번호·범례 줄 포함). 참고용으로 유지 | — |
| `7-1-cosmos-generations-compare.svg` | Cosmos 1 → 2·2.5 → 3 세대별 입력·모델·출력 비교 도식. 입력 → 토큰 → 모델 상자 → 토큰 → 출력 틀(`3-1-alpamayo1-vs-2-architecture.svg`와 같은 틀)로 세 세대를 3단 패널에 두고, 그 세대에서 새로 생긴 입출력은 NEW 태그·초록 테두리, 미지원은 점선 회색으로 표시. Cosmos 1 = Tokenizer + Predict1(디퓨전·자기회귀) + Guardrail, 2·2.5 = Reason·Predict·Transfer 세 탑(따로 배포), 3 = 옴니모달 토크나이저 + Reasoner + Generator(Mixture-of-Transformers) 한 모델. 하단에 "무엇이 같고 무엇이 달라졌나" 요약 띠. nvidia-cosmos 각 저장소 README·NVIDIA/Cosmos README 기반 자체 작성(학습 규모만 📄) | 7장 7.1.5 · report-07 그림 6 |
| `7-2-data-flywheel-v2.svg` | AV 데이터 플라이휠 여덟 단계에 Cosmos/Omniverse가 붙는 지점 (현행판: 제목의 그림 번호·상단 범례 줄·챕터 표기 제거, 회색 단계 상자 안에 도구를 색 상자로 넣어 초록=Cosmos·주황=Omniverse·흰색=NVIDIA 제공 밖을 구분, 텍스트가 블록 안에 들어오도록 열 폭 320px, 화살표마다 흐르는 데이터 라벨(원시 로그, 정제 클립, 라벨된 로그, 3D 장면·도면, 합성 데이터, 학습된 모델, 실패 사례, 수집 지시), NuRec → 폐루프 평가 경로를 실선으로, 갭 재수집은 점선=추정) | 7장 7.2.4 · report-07 그림 8 |
| `7-2-data-flywheel.svg` | 위 도식의 원판 (범례 줄·챕터 표기 포함). 참고용으로 유지 | — |
| `7-3-omniverse-cosmos-pipeline-v2.svg` | Omniverse 출력 → Cosmos Transfer 조건 입력 결합 구조 (현행판: 열 제목은 텍스트+밑줄, 주황=Omniverse·초록=Cosmos만 채색하고 입력원·산출물은 흰색·회색, 텍스트가 블록 안에 들어오도록 조정, 화살표마다 관계 라벨(재구성·렌더·3D 투영, 각 출력을 조건으로, 변주 영상 출력, 생성물 채점), 상단 범례 줄 삭제) | 7장 7.3.3 · report-07 그림 9 |
| `7-3-omniverse-cosmos-pipeline.svg` | Omniverse 출력 → Cosmos Transfer 조건 입력 결합 구조 | 원판, 참고용 유지 |
| `7-3-nurec-architecture.svg` | Omniverse NuRec 파이프라인 도식: 센서 로그 → NCore V4(오픈) → NRE 재구성(NGC 컨테이너·독점: nre-tools 보조 데이터 → 3DGUT/3DGRT 학습 → carline adaptation) → USDZ 장면 → serve-grpc 렌더 서비스 → 시뮬레이터(CARLA·Isaac Sim·AlpaSim·커스텀), 부속 Instant NuRec·Asset Harvester·NuRec Fixer(DiffusionHarmonizer, 초록 = Cosmos 기반), 공개 데이터셋, 오픈·독점·게이트 경계. 공식 도식(docs.nvidia.com/nurec)은 접근 불가라 NVIDIA/nurec-skills·ncore·instant-nurec·3dgrut·CARLA 문서를 읽고 자체 작성 | 7장 7.3.1 · report-07 그림 11 |
| `appendix-a-tier1-workmap.svg` | NVIDIA 제공 범위 vs Tier-1 책임 레이어 지도 + 차별화 매트릭스 | 부록 A A.3 |

규약: 실선 = 출처로 확인, 점선 = 추정. 색: 파랑 = 3장 범위, 초록 = Cosmos, 주황 = Omniverse, 회색 = 다른 장/NVIDIA 제공, 노랑·빨강 = Tier-1 책임.

## 외부 출처 (GitHub에서 내려받음)

| 파일 | 원본 URL | 페이지 | 저작권·라이선스 | 사용 문서 |
|---|---|---|---|---|
| `3-1-alpamayo2-super-architecture.png` | https://raw.githubusercontent.com/NVlabs/alpamayo2/main/alpamayo2super_arch.png | https://github.com/NVlabs/alpamayo2 | © NVIDIA, 저장소 코드 Apache-2.0 | 3장 3.1.2 |
| `3-2-alpasim-architecture.png` | https://raw.githubusercontent.com/NVlabs/alpasim/main/docs/assets/images/alpasim-architecture.png | https://github.com/NVlabs/alpasim/blob/main/docs/DESIGN.md | © NVIDIA, Apache-2.0 | 3장 3.2.6 |
| `3-2-alpasim-demo.gif` | https://raw.githubusercontent.com/NVlabs/alpasim/main/docs/assets/images/thumbnail.gif | https://github.com/NVlabs/alpasim | © NVIDIA, Apache-2.0 | 3장 3.2.6 |
| `7-1-cosmos3-architecture.png` | https://raw.githubusercontent.com/NVIDIA/Cosmos/main/cookbooks/cosmos3/cosmos3-model-architecture.png | https://github.com/NVIDIA/Cosmos | © NVIDIA, OpenMDW-1.1 | 7장 7.1.4 |
| `7-1-predict1-diagram.png` | https://raw.githubusercontent.com/nvidia-cosmos/cosmos-predict1/main/assets/predict1_diagram.png | https://github.com/nvidia-cosmos/cosmos-predict1 | © NVIDIA, 코드 Apache-2.0 | 7장 7.1.2 |
| `7-1-transfer1-diagram.png` | https://raw.githubusercontent.com/nvidia-cosmos/cosmos-transfer1/main/assets/transfer1_diagram.png | https://github.com/nvidia-cosmos/cosmos-transfer1 | © NVIDIA, 코드 Apache-2.0 | 7장 7.1.3 |
| `7-1-predict2-diagram.png` | https://raw.githubusercontent.com/nvidia-cosmos/cosmos-predict2/main/assets/cosmos-predict-diagram.png | https://github.com/nvidia-cosmos/cosmos-predict2 | © NVIDIA, 코드 Apache-2.0 | 7장 7.1.3 |
| `7-2-cosmos-curator-pipelines.png` | https://raw.githubusercontent.com/NVIDIA/cosmos-curator/main/docs/assets/cosmos-curator-pipelines.png | https://github.com/NVIDIA/cosmos-curator | © NVIDIA | 7장 7.2.1 |
| `7-2-drive-dreams-teaser.png` | https://media.githubusercontent.com/media/nv-tlabs/Cosmos-Drive-Dreams/main/assets/teaser.png | https://github.com/nv-tlabs/Cosmos-Drive-Dreams | © NVIDIA, Apache-2.0 | 7장 7.2.4 |
| `7-3-transfer25-world-scenario-rendering.png` | https://media.githubusercontent.com/media/nvidia-cosmos/cosmos-transfer2.5/main/assets/docs/rendering_diagram.png | https://github.com/nvidia-cosmos/cosmos-transfer2.5/blob/main/docs/world_scenario_video_generation.md | © NVIDIA, 코드 Apache-2.0 | 7장 7.3.3 |
| `7-3-omnidreams-hdmap-overlay.png` | https://raw.githubusercontent.com/NVlabs/alpasim/main/docs/assets/images/frame-with-hdmap-render-overlaid.png | https://github.com/NVlabs/alpasim/blob/main/docs/VIDEO_MODEL.md | © NVIDIA, Apache-2.0 | 7장 7.3.3 |
| `7-3-carla-nurec-api.svg` | https://raw.githubusercontent.com/carla-simulator/carla/ue4-dev/Docs/img/carla-nurec-api.svg | https://github.com/carla-simulator/carla/blob/ue4-dev/Docs/nvidia_nurec.md | © CARLA, MIT | 7장 7.3.1 |
| `7-4-cosmos-rl-infra.svg` | https://raw.githubusercontent.com/nvidia-cosmos/cosmos-rl/main/assets/rl_infra.svg | https://github.com/nvidia-cosmos/cosmos-rl | © NVIDIA, Apache-2.0 | 7장 7.4.3 |

## 내려받지 못한 그림 (링크만, 후속 세션 과제)

| 그림 | 페이지 | 이유 |
|---|---|---|
| Alpamayo-R1 논문 Fig.1 (아키텍처) | https://arxiv.org/html/2511.00088v2 | arxiv.org 차단 |
| Cosmos WFM 플랫폼 개요 Fig.1 | https://arxiv.org/html/2501.03575v2 | arxiv.org 차단 |
| Cosmos-Transfer1 / Reason1 논문 그림 | https://arxiv.org/abs/2503.14492 · https://arxiv.org/abs/2503.15558 | arxiv.org 차단 |
| DRIVE AV 듀얼 스택 다이어그램 | https://www.nvidia.com/en-us/solutions/autonomous-vehicles/drive-av/ | nvidia.com 차단 |
| Hyperion 10 센서 배치·2×Thor 보드 | https://www.nvidia.com/en-us/solutions/autonomous-vehicles/drive-hyperion/ | nvidia.com 차단 |
| Halos 계층 다이어그램 | https://www.nvidia.com/en-us/ai-trust-center/halos/autonomous-vehicles/ | nvidia.com 차단 |
| NVIDIA "three computers" 그래픽 | https://blogs.nvidia.com/blog/three-computer-cosmos-ces/ | blogs.nvidia.com 차단 |
| Omniverse Blueprint for AV simulation 다이어그램 | https://nvidianews.nvidia.com/news/nvidia-expands-omniverse-with-generative-physical-ai | nvidianews 차단 |
| DRIVE AGX Thor 개발 키트 보드 사진 | https://developer.nvidia.com/drive/agx | developer.nvidia.com 차단 |
| 3DGRUT 플레이그라운드 GIF | https://github.com/nv-tlabs/3dgrut | Git LFS 포인터만 반환 |
| NuRec "How NuRec Works" 아키텍처 도식 | https://docs.nvidia.com/nurec/basics/how-nurec-works.html | docs.nvidia.com 차단 (자체 도식 `7-3-nurec-architecture.svg`로 대체) |
| "Accelerating AV Simulation with Neural Reconstruction and WFM" 블로그 그림 | https://developer.nvidia.com/blog/accelerating-av-simulation-with-neural-reconstruction-and-world-foundation-models/ | developer.nvidia.com 차단 |
