# 출처·검증 기록 — TIER IV × NVIDIA Alpamayo

- 조사일: 2026-09-07
- 대상 보고서: [`tier4_alpamayo_autoware_보고서.md`](../tier4_alpamayo_autoware_보고서.md)

## 0. 수집 방법

1. 사용자가 제시한 3개 링크(GitHub 저장소 / note.com 해설 / TIER IV Medium 블로그)에서 출발.
2. Medium 원문이 Cloudflare 403으로 막혀, 동일 내용의 원본 보도자료(PRNewswire)를 찾아 전문 확보.
3. `autowarefoundation/alpamayo-autoware`를 `--depth 50`으로 클론해 소스 전량과 커밋 이력을 직접 읽음. 서드파티 해설의 기술 서술은 전부 코드로 재검증.
4. 모델·데이터셋 사양은 Hugging Face 카드 원문에서 확인. 협력 내용은 TIER IV 공식 기술 업데이트와 NVIDIA 뉴스룸으로 교차검증.
5. 저장소 메타데이터(생성일·푸시일·스타·라이선스·포크 관계)는 GitHub REST API로 확인.

## 1. 검증 등급 정의

| 등급 | 의미 |
|---|---|
| 💻 | 클론한 저장소 소스에서 직접 확인. 파일·줄 번호 병기 |
| 🔍 | 1차 출처(공식 발표·모델 카드·논문·공식 문서) 원문 직접 확인 |
| ✅ | 복수 출처 교차검증 |
| 📰 | 서드파티 매체 보도 |
| ⚠️ | 미확인·추정 |

## 2. 접근 실패 목록

| 대상 | 결과 | 대체 |
|---|---|---|
| TIER IV Medium 블로그 (영문) | HTTP 403 (Cloudflare). WebFetch·curl(UA 위장)·r.jina.ai 모두 실패 | PRNewswire 보도자료 원문 |
| TIER IV Medium 블로그 (일문) | HTTP 403 | 동상 |
| Automotive World 기사 | HTTP 403 | 보도자료 |
| Autoware 공식 문서 `docs.autoware.org` | HTTP 404 (리다이렉트 이후) | `tier4.github.io/autoware-documentation` 미러 |

## 3. 소스별 기록

### 1. 저장소 코드 (💻)

**1.1** `https://github.com/autowarefoundation/alpamayo-autoware`
유형: 소스 저장소 (포크) · 브랜치 `alpamayo1.5` · 커밋 `65eda63`

확인 사실:
- GitHub API: `created_at` 2026-01-23, `pushed_at` 2026-08-06, stars 140, forks 14, license Apache-2.0, fork of `NVlabs/alpamayo`
- `src/alpamayo_ros/package.xml` 관리자: `shintaro.sakoda@tier4.jp`, `yukihiro.saito@tier4.jp` → ROS 2 패키지의 TIER IV 저작 확정
- `alpamayo_node.py:53` — `self.model_name: str = "nvidia/Alpamayo-1.5-10B"`
- `alpamayo_node.py:54-57` — 발행 토픽 기본값 전부 `/alpamayo/` 네임스페이스
- `alpamayo_node.py:72-74` 주석 원문: "5-step Euler keeps trajectory ADE within ~1% of 10-step but cuts ~94 ms / inference (3 saved step_fn calls)"
- `alpamayo_node.py:346-348` — 직전 추론 미완료 시 타이머 콜백 즉시 반환
- `alpamayo_node.py:360-362` 주석 원문: "Saves ~150 ms/frame vs cv2.imdecode + CPU copy"
- `alpamayo_node.py:442-444` 주석 원문: "device=\"cuda\" makes Qwen2VLImageProcessorFast run the normalize + patchify pass on GPU (~0.7 ms/frame vs ~58 ms/frame on the CPU fast-path for 4-cam × 4-frame batches)"
- `alpamayo_node.py:381-386` — `torchvision.io.decode_jpeg(buf, device="cuda")` 후 560×1008 bicubic 리사이즈
- `alpamayo_node.py:563-566` — `acceleration_mps2 = 0.0`, `heading_rate_rps = 0.0` 고정
- `alpamayo_node.py:204-209` — `TrtExpertEngine(..., enable_int8=False, enable_fp16=True)`
- `alpamayo_node.py:287-337` — Lanelet2 경로 기반 내비 지시문 생성 (`"Turn {dir}"`, `"Turn {dir} in {dist}m"`, `"Continue straight"`)
- `launch/alpamayo.launch.py:15,32` — 기본 카메라 인덱스 `[0, 1, 2, 6]`, `inference_period_sec` 1.0
- `src/alpamayo1_5/models/base_model.py:211` — `vlm_name_or_path: str = "Qwen/Qwen3-VL-8B-Instruct"`, `vlm_backend: str = "qwenvl3"`
- `src/alpamayo1_5/helper.py` — `BASE_PROCESSOR_NAME = "Qwen/Qwen3-VL-2B-Instruct"`, `MIN_PIXELS = 163840`, `MAX_PIXELS = 196608`
- `src/alpamayo1_5/diffusion/flow_matching.py:22-50` — `class FlowMatching(BaseDiffusion)`, `int_method: Literal["euler"]`, `num_inference_steps: int = 10`
- `src/alpamayo1_5/trt/expert_runtime.py:44-55` — ONNX Runtime `TensorrtExecutionProvider` + 엔진 캐시. expert denoiser 서브그래프만 대상
- `src/alpamayo1_5/trt/export.py` — `ExpertDenoiserExportModule`이 `action_in_proj` / `expert` / `action_out_proj`만 감싼다
- 저장소 전체 `grep -rn "scenario_planning"` → **0건**
- `git diff e0e2ac3 HEAD --stat` → `src/alpamayo_r1/*` 삭제, `src/alpamayo_ros/*` 신규(노드 646줄), 합계 42 files, +4,938 / −791

커밋 이력 (💻 `git log`):
| 커밋 | 날짜 | 작성자 | 내용 |
|---|---|---|---|
| `08a2460` | 2025-11-18 | Boris Ivanovic (NVIDIA) | Initial commit (상류) |
| `e0e2ac3` | 2026-01-15 | Yu Wang (NVIDIA) | 상류 마지막 커밋 |
| `8328103` | 2026-01-23 | Yukihiro Saito (TIER IV) | ROS 2 노드 최초 구현 |
| `abe1ab1` | 2026-03-22 | Shintaro Sakoda (TIER IV) | Alpamayo-1.5 대응 |
| `be16caf` | 2026-03-22 | Shintaro Sakoda | 경로(route) 구현 |
| `a405214` | 2026-04-21 | Max-Bin | GPU 전처리 + greedy + 5스텝 기본값 |
| `e76d607` | 2026-04-22 | Max-Bin | TRT expert 엔진 |
| `65eda63` | 2026-04-23 | Yukihiro Saito | PR #7 머지 (최신) |

**1.2** README "Performance" 표 원문 (🔍)
> Benchmarked on NVIDIA RTX PRO 6000 (96 GB, SM120) with 4 cameras × 4 temporal frames at 1080×1920. Latency is measured end-to-end by replaying a Tier IV rosbag through the ROS 2 node (`rate=0.5`, `max_generation_length=16`, 120 s warmup); medians are taken over 15+ per-inference samples… Trajectory Deviation is `minADE / ground-truth path length`… (GT path length = 46.64 m)

| 구성 | 지연 | FPS | 편차 |
|---|---|---|---|
| Original (CPU preproc, sampling, native, 10-step) | 0.820s | 1.22 | Reference |
| GPU preproc + greedy + native + 10-step | 0.820s | 1.22 | ~0.4% |
| GPU preproc + greedy + native + 5-step | 0.720s | 1.39 | ~0.4% |
| GPU preproc + greedy + TRT + 10-step | 0.700s | 1.43 | ~1.3% |
| GPU preproc + greedy + TRT + 5-step | 0.660s | 1.52 | ~1.8% |
| Full optimized | 0.600s | 1.67 | ~1.8% |

README 면책 원문:
> Alpamayo 1.5 is a pre-trained reasoning model for research purposes and is not a complete autonomous driving stack. It is not intended for use in production environments.

**1.3** `https://github.com/orgs/autowarefoundation/discussions/6747` (🔍)
유형: 공식 공지 (GitHub Discussion) · 2026-01-23 · 작성자 yukkysaito(Yukihiro Saito, 메인테이너)
확인 사실: "We have published the Alpamayo ROS package (for Autoware integration) in the Autoware Foundation (AWF) GitHub organization." 커뮤니티 피드백 기반 개선 예정 언급. 반응 24건, 참여자 2명. 정식 릴리스가 아닌 Discussion 형식.

### 2. 모델·데이터셋 카드

**2.1** `https://huggingface.co/nvidia/Alpamayo-1.5-10B` (🔍)
확인 사실:
- 라이선스: 가중치 OpenMDW-1.1 / 코드 Apache-2.0
- 상용 여부 원문: "This model is ready for non-commercial use. Commercial licensing available upon request."
- 구조: Transformer VLA · 백본 Cosmos-Reason2 8.2B · 확산 기반 액션 디코더 2.3B · 총 약 10.5B
- 입력: 멀티카메라 RGB(기본 4대), 텍스트 명령, 자차 운동 이력. 원문: "1080x1920 pixels (processor will downsample them to 320x576 pixels)". 시간 창 10 Hz × 0.4초
- 출력: 추론 텍스트 + 6.4초 궤적. 원문: "64 waypoints at 10Hz". 자차 좌표계 위치·회전 행렬
- 학습 데이터: 80,000시간 멀티카메라 주행 영상, 300만 건 CoC 추론 주석, 공개·비공개 16개 소스 혼합
- 하드웨어 원문: "Minimum: 1 GPU with 24GB+ VRAM (e.g., NVIDIA RTX 3090, RTX 3090 Ti, RTX 4090, A5000)"

**2.2** `https://huggingface.co/datasets/nvidia/PhysicalAI-Autonomous-Vehicles` (🔍)
확인 사실: 1,700시간 · 25개국 · 2,500+ 도시 · 306,152클립(각 20초) · 133 TB · 카메라 7대 전 클립, 상단 360° LiDAR 298,326클립, 레이더 최대 10개 160,761클립 · v25.10(2025-10) → v26.03(2026-03) · "NVIDIA Autonomous Vehicle Dataset License Agreement" 동의 필요 · 법 집행/교통법규 단속 목적 사용 금지 조항 · 최신 버전에 OOD 시나리오에 대한 human-verified CoC 추론 라벨 포함

### 3. 공식 발표

**3.1** PRNewswire, 2026-03-18 (🔍) — 전문 확보
`https://www.prnewswire.com/news-releases/tier-iv-accelerates-ai-based-level-4-autonomous-driving-with-nvidias-reasoning-based-ai-and-world-foundation-models-302717091.html`
확인 사실:
- 발신 TOKYO, 2026년 3월 18일
- "The company was an early adopter of NVIDIA Alpamayo 1, integrating it into Autoware…"
- "This 10-billion-parameter vision-language-action model introduces a reasoning layer into the driving stack, leveraging chain-of-thought processing to interpret complex scene dynamics."
- Cosmos 3종 역할 정의 (Predict / Transfer / Reason)
- Co-MLOps 2024년 출범
- 인용: Shinpei Kato(TIER IV 창업자·CEO), Marco Pavone(NVIDIA AV Research 디렉터)
- GTC 2026 세션 S81897 "Deployment of a dataset platform for autonomous driving using NVIDIA Cosmos", 발표자 Dan Umeda, 일본어
- Isuzu 버스 배치를 "Together with the autonomous bus deployment initiative with Isuzu and NVIDIA"로 **병렬 서술** — Alpamayo 탑재 언급 없음

**3.2** TIER IV 기술 업데이트, 2026-08-07 (🔍)
`https://tier4.co.jp/en/updates/technology/20260807-comlops-dataset-foundation-for-autonomous-driving-with-nvidia-cosmos`
저자: Dan Umeda (TIER IV Principal Engineer) · GTC 2026 세션 S81897 기반
확인 사실:
- Co-MLOps 8단계 능동학습 루프
- 센서: LiDAR 4대(각 120°) + 다중 화각 카메라 8대
- 수집 범위: 일본 39개 도도부현 · 127개 지점
- CoMET(Collaborative Multi-stage Ensemble-based Teacher): 12개 대규모 모델 앙상블, MoE 설계, TensorRT 배치 추론
- Cosmos Reason: 구조화 JSON 출력, 자연어 검색, ISO 34504 시나리오 태깅, 페타바이트급 처리
- Cosmos Predict 2.5: 30초 영상 생성, 2B/14B
- Cosmos Transfer 2.5: 2B, 원문 "up to a 60% performance gain on autonomous driving 3D lane and cuboid detection tasks"
- 개 검출 IoU: 실데이터만 0.671 → 실데이터+합성 0.893
- 향후: Cosmos 3 이행, Cosmos 3 Nano 사후학습, Gemma4-31B 캡션 변환, 7카메라 서라운드 생성, AutoQA

**3.3** NVIDIA 뉴스룸 DRIVE Hyperion, 2026-03-16 (🔍)
`https://nvidianews.nvidia.com/news/drive-hyperion-level-4`
확인 사실: Isuzu와 TIER IV가 DRIVE AGX Thor로 L4 자율주행 버스 개발 협력. **개별 OEM 차종·출시 시기·TFLOPS·ASIL 등급 수치는 원문에 없음** (일부 매체가 붙인 "2,000 TFLOPS / ASIL-D"는 원문 미확인).

**3.4** NVIDIA Alpamayo 2 Super (🔍)
`https://nvidianews.nvidia.com/news/nvidia-alpamayo-2-super-robotaxis` / `https://blogs.nvidia.com/blog/alpamayo-2-super-open-model-now-available/`
확인 사실: 34B 파라미터("34-billion-parameter"), GTC Taipei 2026-05-31 발표, 2026-08-04~05 상용 공개, OpenMDW-1.1(Linux Foundation), 파인튜닝·파생모델·상용 재배포 허용, 이전 Alpamayo 모델에도 소급 적용된다고 서술. 파트너 목록에 TIER IV 언급 없음.

### 4. 학술

**4.1** arXiv:2511.00088 — Alpamayo-R1 (🔍)
"Bridging Reasoning and Action Prediction for Generalizable Autonomous Driving in the Long Tail", NVIDIA, 2025-10-30 v1 / 2026-01-07 v2, 저자 42인
확인 사실: CoC 데이터셋 정의 원문 "built through a hybrid auto-labeling and human-in-the-loop pipeline producing decision-grounded, causally linked reasoning traces aligned with driving behaviors". Cosmos-Reason + 확산 궤적 디코더 모듈식 VLA. SFT → RL 다단계 학습. 계획 정확도 +12%, 폐루프 근접조우율 −35%, 추론 품질 +45%, 추론-행동 일관성 +37%, 온보드 99 ms.

**4.2** arXiv:2410.23262 — Waymo EMMA (🔍) / **4.3** OpenDriveVLA, AAAI 2026 (🔍) / **4.4** arXiv:2210.02747 — Flow Matching (💻 코드가 인용)

### 5. 문서

**5.1** Autoware Planning component design (🔍)
`https://tier4.github.io/autoware-documentation/latest/design/autoware-architecture/planning/`
확인 사실: Planning이 Control에 넘기는 Trajectory는 "a smooth sequence of pose, twist, and acceleration that the Control Component must follow", 일반적으로 10초 길이 · 0.1초 해상도. 토픽은 `/planning/scenario_planning/trajectory`, 타입 `autoware_planning_msgs/Trajectory` (✅ 커뮤니티 Discussion #2985 교차확인).

### 6. 서드파티

**6.1** note.com / AI-Driven Lab, 2026-08-27 (📰)
`https://note.com/ai_driven/n/n43fe3f1fe358`
확인 사실 및 **오차**:
- 지연 0.820→0.600초, FPS 1.22→1.67, 궤적 64점/6.4초 — README와 일치 ✅
- "Qwen2 기반 VLM" — 코드상 Qwen3-VL 계열. **오기** ⚠️
- "비상업용(OpenMDW-1.1)" — 모델 카드와 일치하나 NVIDIA 블로그 서술과 상충 (§7 참조)
- "Alpamayo 1 공개 2026년 1월(CES)", "Alpamayo 1.5 공개 2026년 3월" — 본 조사에서 1차 출처로 직접 확인하지 못함 ⚠️
- "Alpamayo 2 Super 34B" — NVIDIA 원문과 일치 ✅

**6.2** just-auto, 2026-03-25 (📰)
`https://www.just-auto.com/news/isuzu-deploys-level-4-autonomous-buses/`
확인 사실: Isuzu Erga 디젤·EV 양 모델, TIER IV Autoware 기반 L4 스택, NVIDIA DRIVE AGX Thor + Hyperion. 일본 운전자 부족 대응. 인용 — Shinpei Kato(TIER IV CEO), Hiroshi Sato(Isuzu SVP). 노선·시기·대수 미기재.

## 7. 소스 간 충돌과 판정

| 쟁점 | 판정 |
|---|---|
| 통합 버전 (1 vs 1.5) | 보도자료는 1, 코드는 1.5. 3월 커밋 `abe1ab1`로 전환. **현행 1.5** |
| VLM 백본 (Qwen2 vs Qwen3-VL vs Cosmos-Reason2) | 코드 기본값 `Qwen/Qwen3-VL-8B-Instruct`, 모델 카드 Cosmos-Reason2 8.2B. Cosmos-Reason2가 Qwen3-VL 기반. **Qwen3-VL 계열** |
| 생성 방식 (diffusion vs flow matching) | 코드 `class FlowMatching`, euler. **Flow Matching** |
| TensorRT 적용 범위 | expert denoiser만 ONNX→ORT TRT EP. **부분 적용** |
| 1.5 가중치 상용 가능 여부 | NVIDIA 블로그(소급 적용) vs HF 카드·README(비상용, 2026-09-07 확인). **미해결 — 양쪽 병기** |
| Alpamayo 2 Super 파라미터 | NVIDIA 원문 34B. 일부 요약의 "약 30억"은 오독 |
| 데이터 규모 (1,700h vs 80,000h) | 전자는 공개 데이터셋, 후자는 학습 데이터 총량. **모순 아님** |
| 저장소 pushed_at 2026-08-06 vs 최신 커밋 2026-04-23 | `alpamayo1.5` 브랜치 기준 최신 커밋은 4월. 8월 푸시 내용 **미확인** |

## 8. 이미지 출처

| 파일 | 출처 |
|---|---|
| `images/demo-rviz.png` | [autowarefoundation/alpamayo-autoware](https://github.com/autowarefoundation/alpamayo-autoware) `images/alpamayo-autoware.gif` 첫 프레임 추출 후 폭 1200px 리사이즈. Apache-2.0 |
| `images/data-flow.svg` | 본 보고서 작성. 근거는 커밋 `65eda63`의 소스 코드 |
| `images/autoware-position.svg` | 본 보고서 작성. Autoware 인터페이스 서술은 공식 문서 기준 |
| `images/latency-bench.svg` | 본 보고서 작성. 수치는 저장소 README "Performance" 표 |
