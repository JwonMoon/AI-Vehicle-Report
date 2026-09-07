# 출처 목록 — 3장 · 7장 · 부록 A

> 작성일 2026-09-02. 본문 인라인 인용의 통합 목록. **유형**: 1차(NVIDIA 공식 페이지·문서·보도자료·GitHub) / 파트너(OEM·Tier-1 공식) / 논문 / 2차(언론·블로그). **등급**: 🔍 원문 직접 확인(이 세션에서는 GitHub만 가능) · 📄 검색 엔진 요약으로만 확인 · ✅ 두 개 이상 독립 출처 일치 · ⚠️ 미확인.
> **조사 제약**: 네트워크 정책으로 `*.nvidia.com`, `arxiv.org`, `huggingface.co`, 주요 언론사·보도자료 배포 사이트가 차단되어 해당 URL은 검색 요약(📄) 기준이다. 후속 세션에서 원문 재확인 권장.

---

## A. Alpamayo (3장 3.1)

| # | 출처 | URL | 유형 | 날짜 | 확인 사실 | 등급 |
|---|---|---|---|---|---|---|
| A1 | NVlabs/alpamayo README | https://raw.githubusercontent.com/NVlabs/alpamayo/main/README.md | 1차 GitHub | 2025-11~2026-08 | "Alpamayo 1 Nano는 10B 오픈 추론 VLA"; 4카메라; 6.4초/64 웨이포인트; "not a fully fledged driving stack… no automotive-grade validation"; 코드 Apache-2.0, 가중치 OpenMDW-1.1; DRIVE/Thor 언급 없음 | 🔍 |
| A2 | NVlabs/alpamayo 데이터 로더 코드 | https://raw.githubusercontent.com/NVlabs/alpamayo/main/src/alpamayo_r1/load_physical_aiavdataset.py | 1차 GitHub | — | 카메라 ID 0,1,2,6(cross-left/front-wide/cross-right 120°, front-tele 30°); 이력 16스텝@10Hz | 🔍 |
| A3 | NVlabs/alpamayo 커밋 이력 | https://github.com/NVlabs/alpamayo/commits/main | 1차 GitHub | 2025-11-19~2026-08-29 | 초기 커밋, SFT/RL 스크립트(2026-04-14), CUDA graph 최적화(2026-08-29) | 🔍 |
| A4 | NVlabs/alpamayo1.5 README·커밋 | https://raw.githubusercontent.com/NVlabs/alpamayo1.5/main/README.md · https://github.com/NVlabs/alpamayo1.5/commits/main | 1차 GitHub | 2026-03-20 릴리스 | Cosmos-Reason 백본, RL 후학습, 내비 조건·VQA, 가변 카메라, VRAM 24/40/60GB, "상용 사용 허용" | 🔍 |
| A5 | NVlabs/alpamayo2 README | https://raw.githubusercontent.com/NVlabs/alpamayo2/main/README.md | 1차 GitHub | 2026-08-04 갱신 | "34B = 32B VLM + 2B diffusion expert"; 코드 Apache-2.0 / 가중치 OpenMDW-1.1; H100 80GB; 아키텍처 그림 | 🔍 |
| A6 | NVlabs/alpamayo2 코드(input_profiles.py, config.py, text_tasks.py) | https://raw.githubusercontent.com/NVlabs/alpamayo2/main/src/alpamayo2_super/ | 1차 GitHub | — | 6카메라×4프레임 프로파일; 이력 토큰 48/미래 128; CoC 자동 라벨 4단계 | 🔍 |
| A7 | NVlabs/alpamayo-recipes README | https://raw.githubusercontent.com/NVlabs/alpamayo-recipes/main/README.md | 1차 GitHub | 2026-04~ | 세대표(1 Nano/1.5 Nano/2 Super, 백본 Reason→Reason2→Cosmos 3); 80,000h/1B 이미지; 110,000h+; "teacher model for distillation… on DRIVE AGX Thor"; 데이터셋 라이선스 | 🔍 |
| A8 | alpamayo-recipes SFT 레시피 | https://raw.githubusercontent.com/NVlabs/alpamayo-recipes/main/recipes/alpamayo1_sft/README.md | 1차 GitHub | 2026-05 | 2단계 SFT, 8×H100, 약 97TB, 검증 지표 예 | 🔍 |
| A9 | alpamayo-recipes RL 레시피 | https://raw.githubusercontent.com/NVlabs/alpamayo-recipes/main/recipes/alpamayo1_x_rl/README.md | 1차 GitHub | 2026-05 | GRPO via Cosmos-RL, 보상 ADE+승차감, 640 GPU | 🔍 |
| A10 | alpamayo-recipes 양자화 레시피 | https://raw.githubusercontent.com/NVlabs/alpamayo-recipes/main/recipes/alpamayo1_5_quant/README.md | 1차 GitHub | 2026-06-29 | FP8 11GB 2.00×, FP8+NVFP4 9GB 2.44×, ModelOpt, TensorRT용 Q/DQ | 🔍 |
| A11 | NVlabs/alpasim README·DESIGN.md·VIDEO_MODEL.md | https://raw.githubusercontent.com/NVlabs/alpasim/main/README.md | 1차 GitHub | 2025-10~2026-08 | 연구용 오픈 시뮬, NuRec 기본/OmniDreams 옵션, gRPC 마이크로서비스, "실시간·정밀 물리 비목표", 지원 정책, 데이터셋 NuRec 26.01 | 🔍 |
| A12 | NVlabs/alpagym README | https://raw.githubusercontent.com/NVlabs/alpagym/main/README.md | 1차 GitHub | 2026-06-16 | AlpaSim+Cosmos-RL 폐루프 RL, Alpamayo 1.5만 지원, Apache-2.0 | 🔍 |
| A13 | Alpamayo-R1 논문 | https://arxiv.org/abs/2511.00088 | 논문 | 2025-11 | Cosmos-Reason + 디퓨전 궤적 디코더; SFT+RL; +12% 계획 정확도, −35% 근접 조우, RL +45%/+37%; CoC 정의 | 📄 ✅ |
| A14 | NVIDIA 뉴스룸 CES 2026 Alpamayo | https://nvidianews.nvidia.com/news/alpamayo-autonomous-vehicle-development | 1차 보도자료 | 2026-01-05 | 패밀리 정의; NuRec/Cosmos-Dreams/AlpaSim 문장; 파인튜닝→Hyperion 통합→시뮬 검증; 파트너 JLR·Lucid·Uber·Berkeley DeepDrive | 📄 ✅ |
| A15 | NVIDIA 뉴스룸 Alpamayo 2 Super | https://nvidianews.nvidia.com/news/nvidia-alpamayo-2-super-robotaxis | 1차 보도자료 | 2026-06-01 | 32B 추론 VLA(초기 표기), teacher→Thor 증류 | 📄 |
| A16 | NVIDIA 블로그 Alpamayo 2 Super 공개 | https://blogs.nvidia.com/blog/alpamayo-2-super-open-model-now-available/ | 1차 블로그 | 2026-08 | 32B 백본 + 2.3B 디코더, LingoQA 79.2, OpenMDW 1.1 상용 허용, 50만+ 다운로드 | 📄 |
| A17 | NVIDIA 개발자 블로그 Alpamayo 2 Super | https://developer.nvidia.com/blog/generate-trajectories-reasoning-traces-and-auto-labels-with-nvidia-alpamayo-2-super/ | 1차 블로그 | 2026-08 | 최대 7카메라, minADE₆ 0.911, 메타액션 IoU, AlpaSim Score 1.50 | 📄 |
| A18 | HF 블로그 nvidia-alpamayo-2 | https://huggingface.co/blog/nvidia/nvidia-alpamayo-2 | 1차 블로그 | 2026-06-01 | "Rather than running directly in-vehicle… teacher models"; embodiment misalignment | 📄 |
| A19 | NVIDIA Alpamayo 제품 페이지 | https://www.nvidia.com/en-us/solutions/autonomous-vehicles/alpamayo/ | 1차 페이지 | 2026 | "validated path to in-vehicle deployment on Thor"; Hyperion+Alpamayo로 L4 | 📄 |
| A20 | TechCrunch CES 2026 | https://techcrunch.com/2026/01/05/nvidia-launches-alpamayo-open-ai-models-that-allow-autonomous-vehicles-to-think-like-a-human/ | 2차 | 2026-01-05 | 10B CoT VLA 설명 | 📄 |
| A21 | TechCrunch NeurIPS 2025 | https://techcrunch.com/2025/12/01/nvidia-announces-new-open-ai-models-and-tools-for-autonomous-driving-research | 2차 | 2025-12-01 | R1 10B + 1,727h 데이터셋 공개 | 📄 ✅ |
| A22 | Uber IR 2026-03-16 | https://investor.uber.com/news-events/news/press-release-details/2026/NVIDIA-to-Launch-L4-Software-Driven-Robotaxis-on-Uber-Across-28-Cities-by-2028/default.aspx | 파트너 | 2026-03-16 | LA·SF 2027 H1 → 28개 도시 2028; "Hyperion과 Alpamayo 중심"; "풀스택 L4 소프트웨어 공급자로 진화" | ✅ |
| A23 | HF 데이터셋 PhysicalAI-Autonomous-Vehicles | https://huggingface.co/datasets/nvidia/PhysicalAI-Autonomous-Vehicles | 1차 | 2025-12~ | 1,727h/1,700h, 25개국 2,500+ 도시, 클립 수, 7카메라·LiDAR·레이더 | 📄 |
| A24 | NVlabs/physical_ai_av wiki | https://github.com/NVlabs/physical_ai_av | 1차 GitHub | — | 센서 상세(7카메라 f-theta, 128채널 LiDAR, 레이더 9) | 🔍 |
| A25 | 지연 분석 논문 | https://arxiv.org/html/2605.08975v1 | 논문 | 2026-05 | Alpamayo 1 지연 5성분 프로파일링(DGX Spark), 단일 추론으로 감소 | 📄 |
| A26 | NVIDIA 개발자 블로그 DriveOS LLM SDK | https://developer.nvidia.com/blog/streamline-llm-deployment-for-autonomous-vehicle-applications-with-nvidia-driveos-llm-sdk/ | 1차 블로그 | 2025 | 순수 C++ LLM 런타임, 추측 디코딩·KV 캐시·LoRA, FP16/FP8/NVFP4/INT4 | 📄 |
| A27 | introl 블로그 | https://introl.com/blog/nvidia-neurips-alpamayo-r1-physical-ai-december-2025 | 2차 | 2025-12 | "99ms" 지연 주장(하드웨어 미상) | ⚠️ |
| A28 | radiancefields GTC 2026 인터뷰 | https://radiancefields.com/inside-nvidia-s-alpamayo-1.5-nurec-and-alpadreams-a-gtc-conversation-with-matt-cragun | 2차 | 2026-03 | 1.5·NuRec·AlpaDreams 프리뷰 | 📄 |
| A29 | unite.ai Alpamayo 2 Super | https://www.unite.ai/nvidias-alpamayo-2-super-opens-robotaxi-development-to-commercial-use/ | 2차 | 2026-08 | OpenMDW-1.1 Linux Foundation 2026-05-28, NVIDIA 채택 | 📄 |
| A30 | NVIDIA/Cosmos LICENSE (OpenMDW-1.1 원문) | https://raw.githubusercontent.com/NVIDIA/Cosmos/main/LICENSE | 1차 GitHub | 2026-05 | 무제한 사용·수정·공유, 출력물 무제한, 특허 보복 종료, 고지 유지 | 🔍 |
| A31 | NVlabs/alpasim CHANGELOG | https://github.com/NVlabs/alpasim/blob/main/CHANGELOG.md | 1차 GitHub | 2026-07~08 | 2026-07/08 공개 동기화: 롤아웃 재시도, 장면 배치, GPU 이미지 전처리, driver=alpamayo2, Slurm enroot | 🔍 |
| A32 | NVlabs/alpasim data/scenes/README | https://github.com/NVlabs/alpasim/blob/main/data/scenes/README.md | 1차 GitHub | 2026 | 공개 스위트 public_2601(913)/2604(1,606)/2507(910), HF NuRec 데이터셋 리비전 | 🔍 |
| A33 | NVlabs/alpagym docs/ONBOARDING.md | https://github.com/NVlabs/alpagym/blob/main/docs/ONBOARDING.md | 1차 GitHub | 2026-06 | 요구 사양(2×40GB GPU, 디스크 100~150GB, 장면당 1.5GB, 전체 ~1.5TB), 설치 절차 | 🔍 |
| A34 | NVlabs/alpasim docs/DESIGN.md | https://github.com/NVlabs/alpasim/blob/main/docs/DESIGN.md | 1차 GitHub | 2025-10 | 설계 원칙 3·비목표, 서비스 구성, 데이터 흐름, 복제 우선순위 | 🔍 |
| A35 | PR Newswire aiMotive–LG CES 2026 | https://www.prnewswire.com/news-releases/aimotive-and-lg-to-unveil-advanced-integrated-iviadas-controller-at-ces-2026-302645698.html | 파트너 보도자료 | 2025-12 | LG전자–aiMotive IVI/ADAS 통합 컨트롤러 CES 2026 공개 | 📄 |
| A36 | 헤럴드경제 LG–aiMotive | https://mbiz.heraldcorp.com/article/10847536 | 2차 보도 | 2025 | LG전자 IVI/ADAS 통합 컨트롤러(aiMotive) | 📄 |

## B. DRIVE AV · DriveWorks · Hyperion 10 · 도입 사례 (3장 3.2)

| # | 출처 | URL | 유형 | 날짜 | 확인 사실 | 등급 |
|---|---|---|---|---|---|---|
| B1 | NVIDIA DRIVE AV 제품 페이지 | https://www.nvidia.com/en-us/solutions/autonomous-vehicles/drive-av/ | 1차 페이지 | 2026 | "full-stack… L2++ to L4"; "dual-stack architecture"; "AI end-to-end stack… parallel classical safety stack built on Halos"; "Alpamayo VLA deployed on the E2E stack" | 📄 |
| B2 | NVIDIA 블로그 Mercedes CLA DRIVE AV | https://blogs.nvidia.com/blog/drive-av-software-mercedes-benz-cla/ | 1차 블로그 | 2026-01-05 | 풀스택 DRIVE AV 첫 양산; 듀얼 스택 문장; 3-computer; 미국 L2++ 2026 | ✅ |
| B3 | NVIDIA 블로그 L4 자율주행 | https://blogs.nvidia.com/blog/level-4-autonomous-driving-ai/ | 1차 블로그 | 2025 | "independent modular stack runs parallel… redundancy and guardrails" | 📄 |
| B4 | NVIDIA 블로그 Halos 로보택시 | https://blogs.nvidia.com/blog/halos-os-robotaxi-safety/ | 1차 블로그 | 2025~26 | "Halos Applications layer… deterministic, rule-based functions"; "Drive AGX ensures runtime safety" | 📄 |
| B5 | NVIDIA Halos AV 페이지 | https://www.nvidia.com/en-us/ai-trust-center/halos/autonomous-vehicles/ | 1차 페이지 | 2025~26 | 설계/배포/검증 시 가드레일; DriveOS 6.0 ASIL D 인증, Thor-X 평가; 3-computer | 📄 |
| B6 | developer.nvidia.com/drive | https://developer.nvidia.com/drive | 1차 페이지 | 2026 | 3-computer 정의; Cosmos Curator가 Reason 활용 | 📄 |
| B7 | NVIDIA 블로그 Thor 개발 키트 GA | https://blogs.nvidia.com/blog/drive-agx-developer-kit-general-availability/ | 1차 블로그 | 2025-08-26/27 | DriveOS 구성(세큐어 부트·하이퍼바이저·RTOS·CUDA/TensorRT·DriveWorks); Thor 양산 시스템 Tier-1 5사 | ✅ |
| B8 | NVIDIA 뉴스룸 Hyperion 안전 마일스톤 | https://nvidianews.nvidia.com/news/nvidia-drive-hyperion-platform-achieves-critical-automotive-safety-and-cybersecurity-milestones-for-av-development | 1차 보도자료 | 2025-01-06 | Hyperion 구성(2025 문구); DriveOS 6.0 ASIL D "pending"; ISO 21434 프로세스; TÜV Rheinland UNECE 평가; 검사랩 | ✅ |
| B9 | eeNews DriveOS ASIL D on Orin | https://www.eenewseurope.com/en/nvidia-certifies-drive-os-to-asil-d-but-on-orin/ | 2차 | 2025-01 | 인증은 Orin 기준 | 📄 |
| B10 | DriveWorks 모듈 문서 | https://developer.nvidia.com/docs/drive/driveworks/latest/nvsdk_dw_html/dwx_modules.html | 1차 문서 | — | 모듈 8종 목록 | 📄 |
| B11 | DriveWorks 센서 플러그인 문서 | https://docs.nvidia.com/drive/driveworks-4.0/sensorplugins_mainsection.html · https://info.nvidia.com/using-custom-sensors-with-driveworks.html | 1차 문서 | — | 커스텀 센서 `.so` 플러그인(카메라 제외); 라이다·레이더·GPS·IMU·CAN | ✅ |
| B12 | DriveWorks 7.0.3 legal | https://developer.nvidia.com/docs/drive/drive-os/7.0.3/public/drive-os-linux-sdk/embedded-software-components/DRIVE_AGX_SoC/DriveWorks/DriveWorks_SDK/legal.html | 1차 문서 | 2025 | LicenseRef-NvidiaProprietary, 리버스 엔지니어링 금지 | 📄 |
| B13 | DriveWorks 4.0 블로그 | https://developer.nvidia.com/blog/nvidia-driveworks-4-0-now-available | 1차 블로그 | — | 접근 조건(개발자 프로그램) | 📄 |
| B14 | NVIDIA 포럼 DriveOS 6.0.10 | https://forums.developer.nvidia.com/t/announcement-from-nvidia-drive-os-6-0-10-0-is-now-available/303314 | 1차 포럼 | — | DriveWorks 5.20 동봉 | 📄 |
| B15 | NVIDIA 포럼 DriveOS 7.2.5 | https://forums.developer.nvidia.com/t/announcement-from-nvidia-nvidia-driveos-7-2-5-now-available/379371 | 1차 포럼 | 2026-08경 | DriveOS 7.2.5 공지 | 📄 |
| B16 | DriveOS 7.0.3 문서(샘플·마이그레이션) | https://developer.nvidia.com/docs/drive/drive-os/7.0.3/public/ | 1차 문서 | 2025-07 | DriveWorks가 DriveOS 문서 내 구성 요소; CUDA 12.8/TensorRT 10.10.10 | 📄 |
| B17 | OxTS DriveWorks 플러그인 | https://github.com/OxfordTechnicalSolutions/nvidia-driveworks-plugin | 파트너 GitHub | 2026 | DriveWorks 7.03·Thor용 GNSS/IMU `.so` | 🔍 |
| B18 | NVlabs/Hydra-MDP | https://github.com/NVlabs/Hydra-MDP | 1차 GitHub | 2024 | CVPR 2024 E2E 챌린지 우승, "회사 정책으로 공개 지연", 제품 언급 없음 | 🔍 |
| B19 | DRIVE Labs 블로그·SignNet/LightNet | https://blogs.nvidia.com/blog/drive-labs-autonomous-vehicle-ride/ · https://developer.nvidia.com/blog/drive-labs-signnet-and-lighnet-dnns | 1차 블로그 | ≤2020 | 레거시 DNN 이름 | 📄 |
| B20 | NVIDIA 뉴스룸 Uber·Hyperion 10 | https://nvidianews.nvidia.com/news/nvidia-uber-robotaxi | 1차 보도자료 | 2025-10-28 | Hyperion 10 정의, 2×Thor, 센서 14/9/1/12, Uber 10만 대, Halos Certified Program, 생태계 목록 | ✅ |
| B21 | NVIDIA in-vehicle computing 페이지 | https://www.nvidia.com/en-us/solutions/autonomous-vehicles/in-vehicle-computing/ | 1차 페이지 | 2026 | "two Thor SoCs on a single board… certified DriveOS… qualified sensor suite" | 📄 |
| B22 | Uber IR 2025-10-28 | https://investor.uber.com/news-events/news/press-release-details/2025/Uber-to-Deploy-One-of-the-Worlds-Largest-Networks-of-Autonomous-Vehicles-Powered-by-NVIDIA-AI-Architecture/default.aspx | 파트너 | 2025-10-28 | 10만 대 2027~, Cosmos 데이터 팩토리 | ✅ |
| B23 | Stellantis 보도자료 | https://www.stellantis.com/en/news/press-releases/2025/october/stellantis-advances-global-robotaxi-strategy-with-new-collaboration-with-nvidia-uber-and-foxconn | 파트너 | 2025-10 | ≥5,000대, DRIVE AV L4 Parking/Driving, Foxconn, SOP 2028 | ✅ |
| B24 | Lucid IR CES 2026 | https://ir.lucidmotors.com/news-releases/news-release-details/lucid-nuro-and-uber-unveil-global-robotaxi-ces-announce/ | 파트너 | 2026-01 | Gravity 로보택시, Nuro Driver on Thor/Hyperion, 2만 대 | ✅ |
| B25 | NVIDIA 블로그 Mercedes S-Class L4 | https://blogs.nvidia.com/blog/mercedes-benz-l4-s-class-drive-av-platform | 1차 블로그 | 2026-01 | Hyperion + DRIVE AV L4 + Halos, 중복 설계 | 📄 |
| B26 | NVIDIA 뉴스룸 GTC 2026 Hyperion L4 | https://nvidianews.nvidia.com/news/drive-hyperion-level-4 | 1차 보도자료 | 2026-03-16 | BYD·Geely·Isuzu·Nissan 채택; Alpamayo 1.5 설명 | ✅ |
| B27 | NVIDIA 블로그 Hyperion 생태계 CES 2026 | https://blogs.nvidia.com/blog/global-drive-hyperion-ecosystem-full-autonomy/ | 1차 블로그 | 2026-01 | 센서 파트너(Aeva·Arbe·Hesai·Omnivision·Sony), Tier-1(AUMOVIO·Astemo·Bosch·Magna·Quanta·ZF) | 📄 |
| B28 | Waabi·Volvo | https://waabi.ai/insights/waabi-and-volvo-demonstrate-the-future-of-autonomous-trucking | 파트너 | 2025-10 | Waabi Driver + Thor/Hyperion 10 on VNL Autonomous | 📄 |
| B29 | Wayve·Nissan GTC 2026 | https://wayve.ai/press/wayve-nissan-robotaxi-gtc/ | 파트너 | 2026-03 | LEAF 로보택시 프로토타입, 듀얼 Thor | 📄 |
| B30 | Mercedes MB.DRIVE ASSIST PRO 페이지 | https://group.mercedes-benz.com/technology/autonomous-driving/driving/mb-drive-assist-pro.html | 파트너 | 2026 | "developed in partnership… NVIDIA"; 센서 30개; "508 TOPS"; 협조 조향 | 📄 |
| B31 | autoevolution CLA | https://www.autoevolution.com/news/nvidia-drive-av-software-debuts-in-the-all-new-mercedes-benz-cla-263671.html | 2차 | 2026-01 | "Thor SoC"(상충); "LiDAR·사전 지도 없이" | 📄 ⚠️ |
| B32 | Electrek CLA | https://electrek.co/2026/01/05/nvidia-unveils-open-source-ai-for-autonomous-driving-ships-in-mercedes-benz-cla-in-q1-2026/ | 2차 | 2026-01-05 | "Q1 2026 출하" | 📄 |
| B33 | NVIDIA 블로그 CLA Euro NCAP | https://blogs.nvidia.com/blog/drive-av-mercedes-benz-cla-euro-ncap-safety-award | 1차 블로그 | 2026-01 | Best Performer 2025, DRIVE AV+Halos 공로 | ✅ |
| B34 | NVIDIA 블로그 CES 2026 특별 발표 | https://blogs.nvidia.com/blog/2026-ces-special-presentation/ | 1차 블로그 | 2026-01-05 | "first passenger car featuring Alpamayo… CLA" | 📄 |
| B35 | JLR 보도자료 | https://media.jaguarlandrover.com/news/2022/02/jaguar-land-rover-announces-partnership-nvidia | 파트너 | 2022-02 | Hyperion 풀스택(Orin, DRIVE AV/IX), JLR OS | 📄 |
| B36 | TechCrunch Toyota | https://techcrunch.com/2025/01/06/toyotas-next-generation-cars-will-be-built-with-nvidia-supercomputers-and-operating-system/ | 2차 | 2025-01-06 | Orin + DriveOS | 📄 |
| B37 | Volvo Cars EX90 | https://www.volvocars.com/intl/media/press-releases/9DFE4A251542FAF0/ | 파트너 | — | Orin, Zenseact 자체 소프트웨어 | 📄 |
| B38 | GM 발표 | https://news.gm.com/home.detail.html/Pages/topic/us/en/2025/mar/0318-nvidia-annc.html | 파트너 | 2025-03-18 | Blackwell DRIVE AGX + DriveOS | 📄 |
| B39 | HMG 2026-03-16 | https://www.hyundaimotorgroup.com/en/news/CONT0000000000206046 | 파트너 | 2026-03-16 | L2~L4 통합 아키텍처, Motional | ✅ |
| B40 | carnewschina Zeekr 9X | https://carnewschina.com/2025/09/29/zeekr-9x-full-size-suv-from-geely-launched-in-china-for-63910-usd/ | 2차 | 2025-09-29 | Thor-U 양산 | 📄 |
| B41 | cnevpost XPeng Turing | https://cnevpost.com/2025/04/15/xpeng-to-start-using-turing-chip-q2-report/ | 2차 | 2025-04 | Thor 보류 보도 | ⚠️ |
| B42 | Turing Post AV 해설 | https://www.turingpost.com/p/av | 2차 | 2026 | 클래식 스택 역할 해설 | ⚠️ |
| B43 | Fierce Sensors Hyperion 10 | https://www.fiercesensors.com/sensors/sensors-are-key-nvidia-tie-uber-100k-robotaxis | 2차 | 2025-10 | 중복 시스템·안전 정지 서술 | 📄 |
| B44 | edge-ai-vision Into the Omniverse 2026-02 | https://www.edge-ai-vision.com/2026/02/into-the-omniverse-openusd-and-nvidia-halos-accelerate-safety-for-robotaxis-physical-ai-systems/ | 2차 | 2026-02 | NuRec Fixer, CARLA 통합 | 📄 |
| B45 | TechSpot CLA·Alpamayo | https://www.techspot.com/news/110823-nvidia-alpamayo-ai-platform-autonomous-cars-debut-new.html | 2차 | 2026-01 | "CLA에 Alpamayo 탑재" 주장 | ⚠️ |

## C. Cosmos 세대·데이터 파이프라인 (7장 7.1·7.2)

| # | 출처 | URL | 유형 | 날짜 | 확인 사실 | 등급 |
|---|---|---|---|---|---|---|
| C1 | NVIDIA/Cosmos README | https://github.com/NVIDIA/Cosmos | 1차 GitHub | 2026-05-31~ | 플랫폼 정의; Cosmos 3 MoT 정의·모델군(64B/16B/4B)·행동 조건·가드레일·배포·한계·생태계; OpenMDW-1.1 | 🔍 |
| C2 | NVIDIA/Cosmos cookbooks/cosmos3 | https://github.com/NVIDIA/Cosmos/tree/main/cookbooks/cosmos3 | 1차 GitHub | 2026 | NIM "8B Nano / 32B Super"; 아키텍처 그림 | 🔍 |
| C3 | nvidia-cosmos/cosmos-predict1 README | https://github.com/nvidia-cosmos/cosmos-predict1 | 1차 GitHub | 2025-01~ | 세 분기 정의; 모델 목록; 토크나이저; 가드레일 구성; Single2MultiView; 유지보수 | 🔍 |
| C4 | nvidia-cosmos/cosmos-transfer1 README·examples | https://github.com/nvidia-cosmos/cosmos-transfer1 | 1차 GitHub | 2025-03~ | 정의; 제어 모드; 모델 목록(Sample-AV); AV 추론 예; 멀티뷰; Edge Distilled; 라이선스 | 🔍 |
| C5 | nvidia-cosmos/cosmos-reason1 README | https://github.com/nvidia-cosmos/cosmos-reason1 | 1차 GitHub | 2025-05~ | Qwen2.5-VL 기반, SFT+RL, video critic, 타임라인 | 🔍 |
| C6 | nvidia-cosmos/cosmos-predict2 README | https://github.com/nvidia-cosmos/cosmos-predict2 | 1차 GitHub | 2025-06-11 | 모델 목록, DiT, NATTEN 2.6×, 아카이브 | 🔍 |
| C7 | nvidia-cosmos/cosmos-predict2.5 README·docs | https://github.com/nvidia-cosmos/cosmos-predict2.5 | 1차 GitHub | 2025-10-06~ | flow 통합 모델, Reason1 텍스트 인코더, 2B/14B, auto/multiview 7카메라, 8 GPU, 타임라인 | 🔍 |
| C8 | nvidia-cosmos/cosmos-transfer2.5 README·docs | https://github.com/nvidia-cosmos/cosmos-transfer2.5 | 1차 GitHub | 2025-10-06~ | 2B; Sim2Real/Real2Real 문구; auto multiview 7뷰; World Scenario 렌더; 성능 수치; LiDAR 레시피 | 🔍 |
| C9 | nvidia-cosmos/cosmos-reason2 README | https://github.com/nvidia-cosmos/cosmos-reason2 | 1차 GitHub | 2025-12-19 / 2026-04-29 | Qwen3-VL 기반, 2B/8B/32B, VRAM | 🔍 |
| C10 | nvidia-cosmos/cosmos-rl README | https://github.com/nvidia-cosmos/cosmos-rl | 1차 GitHub | 2025~ | 정의, 비동기 replica, FP8/FP4, 유지보수 모드 | 🔍 |
| C11 | nvidia-cosmos/cosmos-cookbook | https://github.com/nvidia-cosmos/cosmos-cookbook | 1차 GitHub | 2025-10-28~ | AV 3D 그라운딩, GR00T-Dreams 크리틱, Transfer 2.5 Sim2Real(CARLA), Reason 2 AV 캡셔닝, Cosmos Policy 수치 | 🔍 |
| C12 | NVIDIA/cosmos-curator README·docs | https://github.com/NVIDIA/cosmos-curator | 1차 GitHub | 2025~ | 정의(Xenna), 파이프라인 단계, 임베딩·캡셔닝·중복제거·샤딩 | 🔍 |
| C13 | nv-tlabs/Cosmos-Drive-Dreams README | https://github.com/nv-tlabs/Cosmos-Drive-Dreams | 1차 GitHub | 2025-06-10~ | SDG 파이프라인 5단계, 모델 5종, 데이터셋 5,843/81,802, 카메라 rig, 티저 | 🔍 |
| C14 | Cosmos WFM 플랫폼 논문 | https://arxiv.org/abs/2501.03575 | 논문 | 2025-01-07 | 2,000만h/1억 클립, 1만 H100 3개월, 실패 사례 | 📄 |
| C15 | Cosmos-Transfer1 논문 | https://arxiv.org/abs/2503.14492 | 논문 | 2025-03-18 | world-to-world 변환, GB200 NVL72 실시간 | 📄 |
| C16 | Cosmos-Reason1 논문 | https://arxiv.org/abs/2503.15558 | 논문 | 2025-03 | 7B/56B, 벤치마크 수치 | 📄 |
| C17 | Cosmos-Drive-Dreams 논문 | https://arxiv.org/abs/2506.09042 | 논문 | 2025-06 | 롱테일 완화·다운스트림 개선 주장(수치 미확보) | 📄 ⚠️ |
| C18 | Predict2.5/Transfer2.5 논문 | https://arxiv.org/abs/2511.00062 | 논문 | 2025-11 | 2억 클립, RL 후학습, 비교 | 📄 |
| C19 | Cosmos 3 기술 리포트 | https://arxiv.org/abs/2606.02800 | 논문 | 2026-06 | 층별 추론/생성 파라미터 세트, 리더보드 | 📄 |
| C20 | NVIDIA 뉴스룸 CES 2025 Cosmos | https://nvidianews.nvidia.com/news/nvidia-launches-cosmos-world-foundation-model-platform-to-accelerate-physical-ai-development | 1차 보도자료 | 2025-01-06 | 플랫폼 구성, 초기 채택사, Wayve "평가 중" | ✅ |
| C21 | NVIDIA 뉴스룸 GTC 2025 Cosmos | https://nvidianews.nvidia.com/news/nvidia-announces-major-release-of-cosmos-world-foundation-models-and-physical-ai-data-tools | 1차 보도자료 | 2025-03-18 | Reason/Transfer 정의, "Omniverse 정답 → 포토리얼", Blueprint 증폭, 채택사 | ✅ |
| C22 | NVIDIA 블로그 three computers | https://blogs.nvidia.com/blog/three-computer-cosmos-ces/ | 1차 블로그 | 2025-01 | 3-computer AV 정의, 데이터 플라이휠 | 📄 |
| C23 | NVIDIA 블로그 Physical AI Dataset | https://blogs.nvidia.com/blog/open-physical-ai-dataset | 1차 블로그 | 2025-03 | 15TB/32만 궤적, AV 클립 예고 | 📄 |
| C24 | NVIDIA 뉴스룸 Data Factory Blueprint | https://nvidianews.nvidia.com/news/nvidia-announces-open-physical-ai-data-factory-blueprint-to-accelerate-robotics-vision-ai-agents-and-autonomous-vehicle-development | 1차 보도자료 | 2025-10 또는 2026-03 ⚠️ | Cosmos Evaluator, 사용자 목록 | 📄 |
| C25 | NVIDIA 뉴스룸 Cosmos 3 | https://nvidianews.nvidia.com/news/nvidia-launches-cosmos-3-the-open-frontier-foundation-model-for-physical-ai | 1차 보도자료 | 2026-06-01 | 옴니모델 문구, Coalition | 📄 |
| C26 | Linux Foundation OpenMDW-1.1 | https://www.linuxfoundation.org/press/linux-foundation-releases-openmdw-1.1-nvidia-adopts-openmdw-for-cosmos-isaac-gr00t-ising-and-nemotron-ai-model-families | 2차(재단) | 2026-05-28 | NVIDIA 채택 | 📄 |
| C27 | NeMo Curator 비디오 논문 | https://arxiv.org/abs/2503.12964 | 논문 | 2025-03 | 89× 가속, 2,000 H100/일 100만h | 📄 |
| C28 | shujisado NOML 분석 | https://shujisado.org/2025/12/19/nvidia-open-model-license-a-corporate-risk-analysis/ | 2차 | 2025-12 | "Built on NVIDIA Cosmos" 표시·경쟁 제한 비판 | 📄 |
| C29 | HF 블로그 Cosmos Reason 2 | https://huggingface.co/blog/nvidia/nvidia-cosmos-reason-2-brings-advanced-reasoning | 1차 블로그 | 2026-01 | 리더보드 1위, 256K | 📄 |
| C30 | NVIDIA 블로그 SIGGRAPH 2026 | https://blogs.nvidia.com/blog/siggraph-news-2026/ | 1차 블로그 | 2026-07 | Cosmos 3 Edge | 📄 ⚠️ |

## D. Omniverse·활용 패턴·채택사 (7장 7.3·7.4)

| # | 출처 | URL | 유형 | 날짜 | 확인 사실 | 등급 |
|---|---|---|---|---|---|---|
| D1 | NVIDIA NuRec 페이지 | https://developer.nvidia.com/omniverse/nurec | 1차 페이지 | 2025~26 | 정의, Isaac Sim/AlpaSim/CARLA 지원, Transfer 연계 | 📄 |
| D2 | nv-tlabs/3dgrut | https://github.com/nv-tlabs/3dgrut | 1차 GitHub | 2024~2026 | Apache-2.0, 3DGRT/3DGUT, USD 내보내기, 변경 이력 | 🔍 |
| D3 | isaac-sim/IsaacSim 5.0 릴리스 | https://github.com/isaac-sim/IsaacSim/discussions/133 | 1차 GitHub | 2025-08-13 | NuRec/3DGUT 통합, Cosmos Transfer용 Replicator 라이터, Kit 클로즈드 | 🔍 |
| D4 | CARLA NuRec 문서 | https://raw.githubusercontent.com/carla-simulator/carla/ue4-dev/Docs/nvidia_nurec.md | 파트너 GitHub | 2025-09 | 0.9.16 NuRec 통합, 게이트 데이터셋 1.52TB, Docker 서비스 | 🔍 |
| D5 | CARLA Cosmos Transfer 문서 | https://raw.githubusercontent.com/carla-simulator/carla/ue4-dev/Docs/nvidia_cosmos_transfer.md | 파트너 GitHub | 2025-09 | 제어 비디오 생성, H100 요구, 왕복 1~2분 | 🔍 |
| D6 | CARLA AI 렌더링 문서 | https://raw.githubusercontent.com/carla-simulator/carla/ue4-dev/Docs/ai_rendering.md | 파트너 GitHub | 2025-09 | NuRec vs Transfer 보완 관계 | 🔍 |
| D7 | NVIDIA-Omniverse/ovrtx | https://github.com/NVIDIA-Omniverse/ovrtx | 1차 GitHub | 2026 | Sensor RTX 라이브러리 0.4 프리릴리스, 독점 라이선스 | 🔍 |
| D8 | NVIDIA 뉴스룸 Sensor RTX(CVPR 2024) | https://nvidianews.nvidia.com/news/omniverse-microservices-physical-ai | 1차 보도자료 | 2024-06 | Sensor RTX 정의, CARLA·Foretellix·MathWorks | ✅ |
| D9 | NVIDIA 블로그 Sensor RTX 조기 접근 | https://blogs.nvidia.com/blog/omniverse-sensor-rtx-autonomous-machines/ | 1차 블로그 | 2025-01-06 | 카메라·레이더·라이다; Accenture·Foretellix·MITRE·Mcity | 📄 |
| D10 | NVIDIA 뉴스룸 Omniverse 생성형 Physical AI | https://nvidianews.nvidia.com/news/nvidia-expands-omniverse-with-generative-physical-ai | 1차 보도자료 | 2025-01-06 | Blueprint for AV simulation 정의, Omniverse→Transfer | ✅ |
| D11 | NVIDIA 블로그 DRIVE Sim Replicator | https://blogs.nvidia.com/blog/drive-sim-replicator-synthetic-data-generation/ | 1차 블로그 | 2022 | 정답 센서·결정론 | 📄 |
| D12 | NVIDIA 뉴스룸 SIGGRAPH 2025 NuRec | https://nvidianews.nvidia.com/news/nvidia-opens-portals-to-world-of-robotics-with-new-omniverse-libraries-cosmos-physical-ai-models-and-ai-computing-infrastructure | 1차 보도자료 | 2025-08-11 | NuRec 라이브러리, Foretellix 통합 | ✅ |
| D13 | Foretellix | https://www.foretellix.com/foretellix-nvidia-ai-centric/ · https://www.foretellix.com/data-automation-toolchain-for-ai-powered-av-development/ | 파트너 | 2025 | Cosmos 시나리오 다양성, Transfer로 Sensor RTX 데이터 증폭 | ✅ |
| D14 | NVIDIA 블로그 GTC Paris 2025 AV | https://blogs.nvidia.com/blog/autonomous-vehicle-ecosystem-ai-models-developer-tools/ | 1차 블로그 | 2025-06-11 | CARLA 통합, NuRec Fixer, Transfer NIM | 📄 |
| D15 | NVIDIA 블로그 MITRE·Mcity | https://blogs.nvidia.com/blog/mitre-digital-proving-ground/ | 1차 블로그 | 2025 | Sensor RTX 기반 검증 플랫폼 | ✅ |
| D16 | Wayve–NVIDIA | https://wayve.ai/thinking/wayve-nvidia-collaboration/ | 파트너 | 2025~26 | Cosmos 코너케이스 탐색 평가 | 📄 |
| D17 | Waabi–Thor | https://waabi.ai/insights/nvidia-drivethor | 파트너 | 2025 | Cosmos 시뮬·큐레이션 | 📄 |
| D18 | NVIDIA 블로그 auto ecosystem physical AI | https://blogs.nvidia.com/blog/auto-ecosystem-physical-ai/ | 1차 블로그 | 2025-03 | Plus SuperDrive | 📄 |
| D19 | NVIDIA 개발자 블로그 Cosmos WFM E2E AV | https://developer.nvidia.com/blog/simplify-end-to-end-autonomous-vehicle-development-with-new-nvidia-cosmos-world-foundation-models/ | 1차 블로그 | 2025 | Oxa Foundry, Voxel51 | 📄 |
| D20 | Voxel51 GTC DC 2025 | https://voxel51.com/gtc-dc-2025 | 파트너 | 2025-10 | FiftyOne + Cosmos Transfer | 📄 |
| D21 | TechCrunch Uber CES 2025 | https://techcrunch.com/2025/01/07/at-ces-2025-uber-teams-up-with-nvidia-to-scale-autonomous-driving-faster/ | 2차 | 2025-01-07 | Cosmos+DGX Cloud, Khosrowshahi 인용 | ✅ |
| D22 | NVIDIA/GR00T-Dreams | https://github.com/NVIDIA/GR00T-Dreams | 1차 GitHub | 2025 | Cosmos 기반 합성 궤적, IDM, DreamGen | 🔍 |
| D23 | PhysicsMind 벤치마크 | https://arxiv.org/pdf/2601.16007 | 논문 | 2026-01 | 세계 모델 물리 일관성 한계 | 📄 |
| D24 | Pebblous 세계 모델 물리 검증 | https://blog.pebblous.ai/report/world-model-physics-verification/en/ | 2차 | 2026 | 시각 사실성 ≠ 물리 정확성 | 📄 |
| D25 | AV 세계 모델 서베이 | https://arxiv.org/pdf/2501.11260 | 논문 | 2025-01 | 분포 이동 시 성능 저하 | 📄 |
| D26 | TeraSim-World | https://arxiv.org/html/2509.13164v1 | 논문 | 2025-09 | Cosmos-Drive 사용 | 📄 |
| D27 | Axios Cosmos 3 | https://www.axios.com/2026/06/01/nvidia-ai-push-cosmos-3-world-model | 2차 | 2026-06-01 | 출시일 | 📄 |
| D28 | NVIDIA/nurec-skills README | https://github.com/NVIDIA/nurec-skills | 1차 GitHub | 2026-04-30 | NuRec 스택 = physical-ai-datasets·ncore·nre·asset-harvester·nurec-fixer 5개 스킬, NRE NGC 컨테이너(독점) | 🔍 |
| D29 | nurec-skills nurec-index workflows.md | https://raw.githubusercontent.com/NVIDIA/nurec-skills/main/skills/nurec-index/references/workflows.md | 1차 GitHub | 2026-04 | 워크플로 A~G: 기록 → NCore → NRE 학습 → USDZ → 렌더/serve-grpc → 시뮬레이터, 객체 편집, Fixer, 데이터셋 크기 | 🔍 |
| D30 | nurec-skills nre SKILL.md | https://raw.githubusercontent.com/NVIDIA/nurec-skills/main/skills/nre/SKILL.md | 1차 GitHub | 2026-04-30 | NRE release 26.04, 3DGUT/3DGRT 학습, aux 데이터, carline adaptation, serve-grpc sensorsim API, USDZ 구성, VRAM 24~48 GB | 🔍 |
| D31 | nurec-skills nurec-fixer SKILL.md | https://raw.githubusercontent.com/NVIDIA/nurec-skills/main/skills/nurec-fixer/SKILL.md | 1차 GitHub | 2026-04 | NuRec Fixer = DiffusionHarmonizer, Cosmos-Predict2 0.6B 기반, NOML, arXiv 2602.24096 | 🔍 |
| D32 | NVIDIA/ncore README | https://github.com/NVIDIA/ncore | 1차 GitHub | 2026 | NCore: 오픈 다중 센서 데이터 플랫폼, Apache-2.0, 신경 재구성용 형식·센서 모델·변환기 | 🔍 |
| D33 | NVIDIA/instant-nurec README | https://github.com/NVIDIA/instant-nurec | 1차 GitHub | 2026-07 | 피드포워드 3DGS 재구성, NCore V4 입력, PLY + 하늘 큐브맵 출력, NRE 초기화 가능, Apache-2.0 | 🔍 |
| D34 | nv-tlabs/3dgrut README (export 절) | https://github.com/nv-tlabs/3dgrut#exporting-trained-scenes-usd-ply-nurec | 1차 GitHub | 2026-06 | USD ParticleField / NuRec USDZ / PLY 내보내기, Isaac Sim 6.0에서 NuRec USDZ 폐기 예정, NCore v4 학습 지원(2026-03) | 🔍 |

## E. Tier-1 관점·파트너 경계 (부록 A)

| # | 출처 | URL | 유형 | 날짜 | 확인 사실 | 등급 |
|---|---|---|---|---|---|---|
| E1 | DriveOS 6.0.6 Getting Started | https://developer.nvidia.com/docs/drive/drive-os/6.0.6/public/drive-os-linux-sdk/common/topics/intro_sdk/GettingStarted1.html | 1차 문서 | — | PDK "non-reference hardware… requires specific agreements with NVIDIA" | ✅ |
| E2 | DriveOS 7.0.3 Customizing for a Different Board | https://developer.nvidia.com/docs/drive/drive-os/7.0.3/public/drive-os-linux-sdk/platform-customization/customizing_driveos_for_different_board.html | 1차 문서 | 2025 | pinmux XLS → DT 생성 → 통합 절차 | 📄 |
| E3 | DRIVE AGX PDK 프로그램 | https://developer.nvidia.com/drive/agx-pdk-program | 1차 페이지 | — | PDK 프로그램 존재 | 📄 |
| E4 | DriveOS 7.0.3 설치(NGC/Artifactory) | https://developer.nvidia.com/docs/drive/drive-os/7.0.3/public/drive-os-linux-installation/config-registry/config-artifactory.html | 1차 문서 | 2025 | 개발자 프로그램 vs NVONLINE 채널 | ✅ |
| E5 | DriveOS 6.0.9 MCU 문서 | https://developer.nvidia.com/docs/drive/drive-os/6.0.9/public/drive-os-linux-sdk/common/topics/mcu_setup_usage/mcu_setup_and_usage1.html | 1차 문서 | — | Orin 세이프티 MCU = AURIX TC397X B-Step | ✅ |
| E6 | Infineon 커뮤니티 블로그 | https://community.infineon.com/t5/Blogs/Driving-autonomous-safety-and-efficiency-with-Infineon-and-NVIDIA-DRIVE/ba-p/1161805 | 파트너 | 2025 | SMCU 역할(전원·결함 조정) | 📄 |
| E7 | QNX OS for Safety·Thor 키트 | https://seekingalpha.com/pr/20212880-qnx-os-for-safety-integrated-in-nvidia-drive-agx-thor-development-kit-at-general-availability | 파트너 보도자료 | 2025-09 | QNX 8 통합, ASIL-D·ISO 21434 사전 인증 | ✅ |
| E8 | edge-ai-vision Thor 개발 키트 | https://www.edge-ai-vision.com/2025/09/accelerate-autonomous-vehicle-development-with-the-nvidia-drive-agx-thor-developer-kit/ | 2차(NVIDIA 블로그 재게시) | 2025-09 | SKU 10/12, 인터페이스 사양 | ✅ |
| E9 | NVIDIA 블로그 DRIVE 안전 마일스톤 | https://blogs.nvidia.com/blog/nvidia-drive-safety-milestones | 1차 블로그 | 2025 | Orin SoC SEooC ASIL D 체계적/ASIL B 랜덤 | ✅ |
| E10 | Open Robotics 포럼 Orin 인증 | https://discourse.openrobotics.org/t/drive-orin-achieves-safety-certification-for-iso26262/31027 | 2차 | — | SEooC 문구 재인용 | 📄 |
| E11 | ANAB Halos 검사랩 인정 | https://anab.ansi.org/anab-accredits-nvidia-halos-ai-inspection-lab-advancing-independent-assurance-for-physical-ai-safety/ | 인정 기관 | 2026-06-22 | ISO/IEC 17020, 범위, 인증 기관 목록 | ✅ |
| E12 | NVIDIA 블로그 검사랩 CES 2025 | https://blogs.nvidia.com/blog/drive-ai-lab-ces/ | 1차 블로그 | 2025-01 | 검사랩 정의 | 📄 |
| E13 | Magna 2026-01-05 | https://www.magna.com/stories/news-press-release/2026/magna-to-offer-drive-hyperion-compatible-ecus-and-tier-1-integration-services-for-nvidia-drive-av | 파트너 | 2026-01-05 | 통합·검증·안전 승인·배포 서비스, Hyperion 호환 ECU | 📄 |
| E14 | Bosch 2025-10-01 | https://us.bosch-press.com/pressportal/us/en/press-release-28736.html | 파트너 | 2025-10-01 | Thor 통합, 안전 전문성·양산 배포, 역할 분담 | ✅ |
| E15 | Aurora·Continental·NVIDIA | https://ir.aurora.tech/news-events/press-releases/detail/112/aurora-continental-and-nvidia-partner-to-deploy-driverless-trucks-at-scale | 파트너 | 2025-01 | 듀얼 Thor 주 컴퓨터, Continental 2차 시스템·2027 양산 | ✅ |
| E16 | Desay SV | https://en.desaysv.com/newsDetails/544.html | 파트너 | 2025 | IPU03/04/14 계보, GAC Hyptec L4 | ✅ |
| E17 | Lenovo AD1 | https://news.lenovo.com/pressroom/press-releases/lenovo-works-with-swm-to-develop-next-generation-robotaxi-on-nvidia-drive-agx-thor/ | 파트너 | 2025 | 듀얼 Thor L4 컨트롤러, WeRide GXR | ✅ |
| E18 | eeNews Hyperion 생태계 CES 2026 | https://www.eenewseurope.com/en/nvidia-drive-hyperion-ecosystem-expands-ces-2026/ | 2차 | 2026-01 | Tier-1·센서 파트너 목록, "공통 레퍼런스 대비 검증된 ECU·센서" | 📄 |
| E19 | LG–NVIDIA | https://www.prnewswire.com/news-releases/lg-teams-with-nvidia-to-shape-the-future-with-map-mobility--ai-infra--physical-ai-302793797.html | 파트너 보도자료 | 2026 | IVI + Hyperion 통합, LG이노텍 부품 | 📄 |
| E20 | HMG 2025-10-31 AI 팩토리 | https://www.hyundaimotorgroup.com/en/news/hyundai-motor-group-nvidia-blackwell-ai-factory | 파트너 | 2025-10-31 | Thor+DriveOS 위 ADAS 자체 개발, Blackwell 5만 장 | ✅ |
| E21 | HMG 2026-03-16 확대 | https://www.hyundaimotorgroup.com/en/news/hyundai-motor-kia-and-nvidia-expand-strategic-partnership-for-next-generation-autonomous-driving-technology | 파트너 | 2026-03-16 | L2 이상 NVIDIA 자율주행 기술 통합 | ✅ |
| E22 | Intertek SEooC 해설 | https://www.intertek.com/blog/2026/01-15-exploring-safety-elements-out-of-context/ | 2차 | 2026-01-15 | 안전 매뉴얼의 역할 | 📄 |
| E23 | NVIDIA 뉴스룸 Mercedes 2020 | https://nvidianews.nvidia.com/news/mercedes-benz-and-nvidia-to-build-software-defined-computing-architecture-for-automated-driving-across-future-fleet | 1차 보도자료 | 2020-06-23 | 반복 수익 공유 구조 | ✅ |
| E24 | TechCrunch Mercedes 2020 | https://techcrunch.com/2020/06/23/mercedes-benz-nvidia-partner-to-bring-software-defined-vehicles-to-market-in-2024/ | 2차 | 2020-06-23 | 조건 비공개 | 📄 |
| E25 | DriveOS 5.2 Tegra CAN 문서 | https://docs.nvidia.com/drive/drive-os-5.2.6.0L/drive-os/DRIVE_OS_Linux_SDK_NGC_Development_Guide/Interfaces/sys_components_tegra_can.html | 1차 문서 | — | 저수준 CAN 인터페이스 문서화 | 📄 |
| E26 | Scribd DriveWorks SDK 개요 | https://www.scribd.com/document/445973609/NVIDIA-driveworks-SDK-CH8712 | 2차(문서 미러) | — | 샘플 소스+바이너리, 툴 바이너리, OS 지원 | 📄 |
