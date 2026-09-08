# D1 — Autoware 소스 정적 해부 (autoware_anatomy.py 실행 로그)

- 실행일: 2026-09-08 (UTC)
- 환경: Linux, 4 CPU cores, GPU 없음, Python 3.11.15, git 2.43.0
- 클론 방식: `git clone --depth 1` (main HEAD). 참고: `autoware/repositories/autoware.repos`는 `autoware_core 1.9.0`, `autoware_universe 0.52.1`, `autoware_launch 0.52.0`을 pin하지만, 본 측정은 각 저장소의 **main HEAD** 기준이다.
- 클론 커밋 (git log -1):

| repo | commit | commit date | last subject |
|---|---|---|---|
| autoware | 3354a273fc2f374e99fb3a759f6f4ab2947b5ada | 2026-09-07T12:04:53+03:00 | fix(acados): pin CasADi to 3.7.2 for Humble ARM64 (#7307) |
| autoware_core | 6e1e1673011e90aacb5f387d829b81280172b539 | 2026-09-08T10:00:13+09:00 | feat(autoware_path_generator): implement characterization test (#1403) |
| autoware_universe | 089d327d8fab0ce44bbb7ca1b045e6e57f96375b | 2026-09-08T10:06:00+09:00 | feat(autoware_carla_interface): allow overriding the wheel max steer angle ... (#13278) |
| autoware_launch | 045c07f45c4191e97930896d5cce105be8119953 | 2026-09-07T11:40:30+00:00 | chore(sync-params): update planning params (#1977) |
| autoware_msgs | bb8e7bf5d97168663e0e7b357929e4fcdbd3a967 | 2026-05-20T18:05:09+09:00 | chore: bump version (1.13.0) (#166) |
| autoware_adapi_msgs | 35a7aeb97dfbbbc363c49fc032ded0c8ba172e24 | 2026-06-23T10:42:34-07:00 | chore: bump version (1.9.2) (#111) |
| autoware_internal_msgs | 4144effa727d194554ad78d343683201bbbbc427 | 2026-09-04T02:17:28+03:00 | chore: bump version (1.16.0) (#95) |

- 명령:

```bash
WORK=$SCRATCH/work/autoware   # 세션 스크래치패드 (저장소 밖)
for r in autoware autoware_core autoware_universe autoware_launch autoware_msgs autoware_adapi_msgs autoware_internal_msgs; do
  git clone --depth 1 https://github.com/autowarefoundation/$r.git $WORK/$r
done
python3 research/autonomous-driving-sw-stack/scripts/autoware_anatomy.py $WORK > d1-autoware-anatomy.md
# 실행 시간: real 2.3s (전체 7개 클론, 약 470MB)
```

- 측정 정의(스크립트 기준): 패키지 = `package.xml` 존재 디렉터리(`COLCON_IGNORE` 하위 제외); 노드 등록 = `RCLCPP_COMPONENTS_REGISTER_NODE(` 출현 횟수 및 `public rclcpp::Node|LifecycleNode` 상속 선언 횟수; LOC = 공백 제외 줄 수(cpp=.cpp/.cc/.cxx/.c, hpp=.hpp/.h/.hh/.hxx, py=.py, cu=.cu/.cuh); dep edges = package.xml의 `<depend>`, `<build_depend>`, `<build_export_depend>`, `<exec_depend>`, `<test_depend>`, `<buildtool_depend>`, `<doc_depend>` 합계; 기술 언급 = 패키지 내 소스/헤더/CMakeLists/package.xml에 정규식(agnocast, cuda_blackboard, tensorrt|nvinfer, \bonnx) 매치.
- 한계: 정적 텍스트 측정이므로 실제 빌드/실행 시 활성화되는 노드 수와 다를 수 있음. `.launch.py`는 트리에서 leaf로만 표시(파싱 안 함). `$(var ...)`로 동적으로 결정되는 include(센서킷, 차량 인터페이스, preset yaml)는 UNRESOLVED로 표시.

---

# Autoware static anatomy report

- generated: 2026-09-08T01:31:21+00:00
- python: 3.11.15
- clone_root: `/tmp/claude-0/-home-user-AI-Vehicle-Research/a65f6795-d733-5b00-b96f-54b90fbc966f/scratchpad/work/autoware`

## Repositories scanned

| repo | HEAD (short hash, commit date) | LICENSE (1st line) |
|---|---|---|
| autoware | 3354a27 2026-09-07T12:04:53+03:00 | Apache License |
| autoware_core | 6e1e167 2026-09-08T10:00:13+09:00 | Apache License |
| autoware_universe | 089d327 2026-09-08T10:06:00+09:00 | Apache License |
| autoware_launch | 045c07f 2026-09-07T11:40:30+00:00 | Apache License |
| autoware_msgs | bb8e7bf 2026-05-20T18:05:09+09:00 | Apache License |
| autoware_adapi_msgs | 35a7aeb 2026-06-23T10:42:34-07:00 | Apache License |
| autoware_internal_msgs | 4144eff 2026-09-04T02:17:28+03:00 | Apache License |

## autoware.repos manifest (meta repo)

- entries: 31  by group: core=12, launcher=1, sensor_component=5, universe=13

| path (group/name) | url | version |
|---|---|---|
| core/agnocast | https://github.com/autowarefoundation/agnocast.git | 2.4.0 |
| core/autoware_msgs | https://github.com/autowarefoundation/autoware_msgs.git | 1.13.0 |
| core/autoware_adapi_msgs | https://github.com/autowarefoundation/autoware_adapi_msgs.git | 1.9.2 |
| core/autoware_internal_msgs | https://github.com/autowarefoundation/autoware_internal_msgs.git | 1.16.0 |
| core/autoware_cmake | https://github.com/autowarefoundation/autoware_cmake.git | 1.4.0 |
| core/autoware_utils | https://github.com/autowarefoundation/autoware_utils.git | 1.10.0 |
| core/autoware_lanelet2_extension | https://github.com/autowarefoundation/autoware_lanelet2_extension.git | 1.2.0 |
| core/autoware_core | https://github.com/autowarefoundation/autoware_core.git | 1.9.0 |
| core/autoware_rviz_plugins | https://github.com/autowarefoundation/autoware_rviz_plugins.git | 0.6.0 |
| core/autoware_simple_planning_simulator |  | 1.0.0 |
| core/autoware_system_designer | https://github.com/autowarefoundation/autoware_system_designer.git | v0.4.2 |
| core/external/rviz_2d_overlay_plugins | https://github.com/teamspatzenhirn/rviz_2d_overlay_plugins.git | 1.4.0 |
| universe/autoware_universe | https://github.com/autowarefoundation/autoware_universe.git | 0.52.1 |
| universe/external/tier4_autoware_msgs | https://github.com/tier4/tier4_autoware_msgs.git | v0.70.0-rc |
| universe/external/morai_msgs | https://github.com/MORAI-Autonomous/MORAI-ROS2_morai_msgs.git | e2e75fc1603a9798773e467a679edf68b448e705 |
| universe/external/muSSP | https://github.com/tier4/muSSP.git | c79e98fd5e658f4f90c06d93472faa977bc873b9 |
| universe/external/pointcloud_to_laserscan | https://github.com/tier4/pointcloud_to_laserscan.git | d969ec699f84fad827fbadfa3001c9c657482fbe |
| universe/external/eagleye | https://github.com/MapIV/eagleye.git | 575136ebba99892946d36d8398f228aee2136af0 |
| universe/external/rtklib_ros_bridge | https://github.com/MapIV/rtklib_ros_bridge.git | ef094407bba4f475a8032972e0c60cbb939b51b8 |
| universe/external/llh_converter | https://github.com/MapIV/llh_converter.git | 4fc2a2e1bc9dcf3e6ab0a8085d8257168e160342 |
| universe/external/glog | https://github.com/tier4/glog.git | ea36766fdc2ac8e8c8e3ac988ae69acd6d09bb30 |
| universe/external/bevdet_vendor | https://github.com/autowarefoundation/bevdet_vendor.git | 0.2.1 |
| universe/external/cuda_blackboard | https://github.com/autowarefoundation/cuda_blackboard.git | 0.4.0 |
| universe/external/negotiated | https://github.com/osrf/negotiated.git | eac198b55dcd052af5988f0f174902913c5f20e7 |
| universe/external/managed_transform_buffer | https://github.com/autowarefoundation/managed_transform_buffer.git | 0.2.0 |
| launcher/autoware_launch | https://github.com/autowarefoundation/autoware_launch.git | 0.52.0 |
| sensor_component/external/sensor_component_description | https://github.com/tier4/sensor_component_description.git | 03ba094851ec90febfcfc0adb20b64b0e19df7a8 |
| sensor_component/external/nebula | https://github.com/tier4/nebula.git | v1.1.0 |
| sensor_component/external/sync_tooling_msgs | https://github.com/tier4/sync_tooling_msgs.git | v0.2.10 |
| sensor_component/transport_drivers | https://github.com/autowarefoundation/transport_drivers | 39ebd8afe1bb9760a6cd6272e428468480f6de90 |
| sensor_component/ros2_socketcan | https://github.com/autowarefoundation/ros2_socketcan | e39a814180b03f00a5692b6951a5d4e9f0463486 |

## Per-repo summary

| repo | pkgs | REGISTER_NODE | public rclcpp::Node | launch.xml | launch.py | msg | srv | action | LOC cpp | LOC hpp | LOC py | LOC cu | dep edges |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| autoware | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| autoware_core | 74 | 36 | 39 | 39 | 10 | 0 | 0 | 0 | 108976 | 40394 | 4449 | 0 | 1320 |
| autoware_universe | 241 | 251 | 178 | 215 | 19 | 14 | 0 | 0 | 366123 | 141342 | 24215 | 16721 | 4376 |
| autoware_launch | 30 | 0 | 0 | 124 | 1 | 0 | 0 | 0 | 0 | 0 | 212 | 0 | 331 |
| autoware_msgs | 12 | 0 | 0 | 0 | 0 | 75 | 12 | 0 | 0 | 0 | 0 | 0 | 104 |
| autoware_adapi_msgs | 2 | 0 | 0 | 0 | 0 | 61 | 19 | 0 | 0 | 0 | 0 | 0 | 16 |
| autoware_internal_msgs | 6 | 0 | 0 | 0 | 0 | 40 | 8 | 0 | 0 | 0 | 0 | 0 | 55 |
| **TOTAL** | 365 | 287 | 217 | 378 | 30 | 190 | 39 | 0 | 475099 | 181736 | 28876 | 16721 | 6202 |

## Per top-level module directory

| repo | module | pkgs | REGISTER_NODE | public rclcpp::Node | launch.xml | launch.py | msg+srv+action | LOC cpp | LOC hpp | LOC py | LOC cu | dep edges |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| autoware_adapi_msgs | autoware_adapi_v1_msgs | 1 | 0 | 0 | 0 | 0 | 79 | 0 | 0 | 0 | 0 | 11 |
| autoware_adapi_msgs | autoware_adapi_version_msgs | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 5 |
| autoware_core | api | 4 | 5 | 5 | 3 | 1 | 0 | 1068 | 1010 | 126 | 0 | 57 |
| autoware_core | autoware_core | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 14 |
| autoware_core | common | 21 | 0 | 4 | 1 | 5 | 0 | 52408 | 20680 | 2878 | 0 | 294 |
| autoware_core | control | 3 | 2 | 2 | 2 | 1 | 0 | 1433 | 202 | 26 | 0 | 41 |
| autoware_core | description | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 |
| autoware_core | localization | 8 | 6 | 7 | 7 | 0 | 0 | 10485 | 6115 | 231 | 0 | 163 |
| autoware_core | map | 5 | 5 | 1 | 6 | 0 | 0 | 4973 | 917 | 737 | 0 | 91 |
| autoware_core | perception | 4 | 4 | 4 | 5 | 3 | 0 | 4199 | 1231 | 324 | 0 | 68 |
| autoware_core | planning | 15 | 8 | 10 | 6 | 0 | 0 | 28154 | 8009 | 0 | 0 | 451 |
| autoware_core | sensing | 5 | 5 | 4 | 6 | 0 | 0 | 3241 | 556 | 0 | 0 | 75 |
| autoware_core | testing | 4 | 1 | 2 | 1 | 0 | 0 | 3015 | 1674 | 127 | 0 | 52 |
| autoware_core | vehicle | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 5 |
| autoware_internal_msgs | autoware_internal_debug_msgs | 1 | 0 | 0 | 0 | 0 | 14 | 0 | 0 | 0 | 0 | 7 |
| autoware_internal_msgs | autoware_internal_localization_msgs | 1 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 8 |
| autoware_internal_msgs | autoware_internal_metric_msgs | 1 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 6 |
| autoware_internal_msgs | autoware_internal_msgs | 1 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 12 |
| autoware_internal_msgs | autoware_internal_perception_msgs | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 9 |
| autoware_internal_msgs | autoware_internal_planning_msgs | 1 | 0 | 0 | 0 | 0 | 26 | 0 | 0 | 0 | 0 | 13 |
| autoware_launch | autoware_launch | 1 | 0 | 0 | 15 | 1 | 0 | 0 | 0 | 66 | 0 | 31 |
| autoware_launch | autoware_sample_designs | 1 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 10 |
| autoware_launch | autoware_universe_launch | 8 | 0 | 0 | 72 | 0 | 0 | 0 | 0 | 146 | 0 | 137 |
| autoware_launch | sensor_kit | 10 | 0 | 0 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 69 |
| autoware_launch | tier4_universe_launch | 6 | 0 | 0 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | 78 |
| autoware_launch | vehicle | 4 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| autoware_msgs | autoware_common_msgs | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 5 |
| autoware_msgs | autoware_control_msgs | 1 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 6 |
| autoware_msgs | autoware_localization_msgs | 1 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 8 |
| autoware_msgs | autoware_map_msgs | 1 | 0 | 0 | 0 | 0 | 13 | 0 | 0 | 0 | 0 | 9 |
| autoware_msgs | autoware_msgs | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 12 |
| autoware_msgs | autoware_perception_msgs | 1 | 0 | 0 | 0 | 0 | 19 | 0 | 0 | 0 | 0 | 9 |
| autoware_msgs | autoware_planning_msgs | 1 | 0 | 0 | 0 | 0 | 13 | 0 | 0 | 0 | 0 | 11 |
| autoware_msgs | autoware_sensing_msgs | 1 | 0 | 0 | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 8 |
| autoware_msgs | autoware_simulation_msgs | 1 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 9 |
| autoware_msgs | autoware_system_msgs | 1 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 12 |
| autoware_msgs | autoware_v2x_msgs | 1 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 7 |
| autoware_msgs | autoware_vehicle_msgs | 1 | 0 | 0 | 0 | 0 | 15 | 0 | 0 | 0 | 0 | 8 |
| autoware_universe | common | 17 | 4 | 9 | 3 | 0 | 0 | 26371 | 7556 | 0 | 0 | 224 |
| autoware_universe | control | 21 | 18 | 15 | 19 | 1 | 7 | 22739 | 8858 | 10418 | 0 | 484 |
| autoware_universe | e2e | 1 | 1 | 1 | 1 | 0 | 0 | 2564 | 2936 | 0 | 450 | 31 |
| autoware_universe | evaluator | 7 | 10 | 7 | 8 | 1 | 0 | 7919 | 3956 | 21 | 0 | 158 |
| autoware_universe | examples | 1 | 0 | 0 | 0 | 0 | 0 | 64 | 0 | 0 | 0 | 6 |
| autoware_universe | localization | 14 | 22 | 20 | 15 | 0 | 2 | 7956 | 3718 | 152 | 0 | 210 |
| autoware_universe | map | 1 | 2 | 1 | 1 | 0 | 0 | 216 | 31 | 0 | 0 | 17 |
| autoware_universe | perception | 51 | 73 | 41 | 72 | 9 | 0 | 92382 | 38827 | 1740 | 12408 | 919 |
| autoware_universe | planning | 67 | 25 | 19 | 26 | 0 | 5 | 152279 | 49046 | 3462 | 0 | 1466 |
| autoware_universe | sensing | 13 | 38 | 18 | 36 | 3 | 0 | 19769 | 12931 | 1097 | 3863 | 185 |
| autoware_universe | simulator | 7 | 5 | 7 | 8 | 0 | 0 | 2695 | 1101 | 4600 | 0 | 101 |
| autoware_universe | system | 24 | 50 | 37 | 22 | 4 | 0 | 20902 | 8482 | 621 | 0 | 312 |
| autoware_universe | vehicle | 4 | 3 | 3 | 4 | 1 | 0 | 3948 | 1301 | 2104 | 0 | 96 |
| autoware_universe | visualization | 13 | 0 | 0 | 0 | 0 | 0 | 6319 | 2599 | 0 | 0 | 167 |

## Interface packages (msg/srv/action per package)

| repo | package | msg | srv | action |
|---|---|---|---|---|
| autoware_adapi_msgs | autoware_adapi_v1_msgs | 61 | 18 | 0 |
| autoware_adapi_msgs | autoware_adapi_version_msgs | 0 | 1 | 0 |
| autoware_internal_msgs | autoware_internal_planning_msgs | 21 | 5 | 0 |
| autoware_internal_msgs | autoware_internal_debug_msgs | 13 | 1 | 0 |
| autoware_internal_msgs | autoware_internal_msgs | 3 | 0 | 0 |
| autoware_internal_msgs | autoware_internal_metric_msgs | 2 | 0 | 0 |
| autoware_internal_msgs | autoware_internal_localization_msgs | 0 | 2 | 0 |
| autoware_internal_msgs | autoware_internal_perception_msgs | 1 | 0 | 0 |
| autoware_msgs | autoware_perception_msgs | 19 | 0 | 0 |
| autoware_msgs | autoware_vehicle_msgs | 14 | 1 | 0 |
| autoware_msgs | autoware_map_msgs | 9 | 4 | 0 |
| autoware_msgs | autoware_planning_msgs | 9 | 4 | 0 |
| autoware_msgs | autoware_sensing_msgs | 9 | 0 | 0 |
| autoware_msgs | autoware_system_msgs | 3 | 2 | 0 |
| autoware_msgs | autoware_control_msgs | 4 | 0 | 0 |
| autoware_msgs | autoware_v2x_msgs | 4 | 0 | 0 |
| autoware_msgs | autoware_simulation_msgs | 2 | 0 | 0 |
| autoware_msgs | autoware_localization_msgs | 1 | 1 | 0 |
| autoware_msgs | autoware_common_msgs | 1 | 0 | 0 |
| autoware_universe | autoware_trajectory_validator | 4 | 0 | 0 |
| autoware_universe | autoware_control_performance_analysis | 4 | 0 | 0 |
| autoware_universe | yabloc_particle_filter | 2 | 0 | 0 |
| autoware_universe | autoware_planning_validator | 1 | 0 | 0 |
| autoware_universe | autoware_vehicle_cmd_gate | 1 | 0 | 0 |
| autoware_universe | autoware_operation_mode_transition_manager | 1 | 0 | 0 |
| autoware_universe | autoware_control_validator | 1 | 0 | 0 |

## Dependency edges (package.xml)

- edges by tag: `<depend>`=3977, `<test_depend>`=1033, `<buildtool_depend>`=731, `<exec_depend>`=406, `<build_depend>`=54, `<build_export_depend>`=1
- unique (src,dst) edges: internal(dst cloned)=1664, external(dst not cloned: rclcpp, pcl, ...)=4538

### Top-20 most-depended packages (all)

| rank | package | in-degree | cloned? |
|---|---|---|---|
| 1 | ament_lint_auto | 326 | no |
| 2 | autoware_cmake | 316 | no |
| 3 | ament_cmake_auto | 315 | no |
| 4 | autoware_lint_common | 297 | no |
| 5 | rclcpp | 272 | no |
| 6 | rclcpp_components | 198 | no |
| 7 | geometry_msgs | 162 | no |
| 8 | ament_cmake_ros | 142 | no |
| 9 | autoware_utils | 135 | no |
| 10 | tf2 | 102 | no |
| 11 | autoware_perception_msgs | 98 | yes |
| 12 | autoware_planning_msgs | 98 | yes |
| 13 | autoware_motion_utils | 94 | yes |
| 14 | tf2_ros | 86 | no |
| 15 | visualization_msgs | 81 | no |
| 16 | nav_msgs | 79 | no |
| 17 | sensor_msgs | 78 | no |
| 18 | autoware_agnocast_wrapper | 78 | yes |
| 19 | tf2_geometry_msgs | 74 | no |
| 20 | std_msgs | 73 | no |

### Top-20 most-depended packages (cloned Autoware packages only)

| rank | package | in-degree | repo/module |
|---|---|---|---|
| 1 | autoware_perception_msgs | 98 | autoware_msgs/autoware_perception_msgs |
| 2 | autoware_planning_msgs | 98 | autoware_msgs/autoware_planning_msgs |
| 3 | autoware_motion_utils | 94 | autoware_core/common |
| 4 | autoware_agnocast_wrapper | 78 | autoware_core/common |
| 5 | autoware_vehicle_info_utils | 72 | autoware_core/common |
| 6 | autoware_internal_debug_msgs | 63 | autoware_internal_msgs/autoware_internal_debug_msgs |
| 7 | autoware_map_msgs | 52 | autoware_msgs/autoware_map_msgs |
| 8 | autoware_internal_planning_msgs | 52 | autoware_internal_msgs/autoware_internal_planning_msgs |
| 9 | autoware_lanelet2_utils | 52 | autoware_core/common |
| 10 | autoware_vehicle_msgs | 50 | autoware_msgs/autoware_vehicle_msgs |
| 11 | autoware_test_utils | 49 | autoware_core/testing |
| 12 | autoware_adapi_v1_msgs | 45 | autoware_adapi_msgs/autoware_adapi_v1_msgs |
| 13 | autoware_route_handler | 38 | autoware_core/planning |
| 14 | autoware_object_recognition_utils | 37 | autoware_core/common |
| 15 | autoware_interpolation | 25 | autoware_core/common |
| 16 | autoware_control_msgs | 22 | autoware_msgs/autoware_control_msgs |
| 17 | autoware_cuda_dependency_meta | 22 | autoware_universe/common |
| 18 | autoware_point_types | 20 | autoware_core/common |
| 19 | autoware_cuda_utils | 18 | autoware_universe/sensing |
| 20 | autoware_planning_factor_interface | 17 | autoware_core/planning |

### Top-10 packages by out-degree (most dependencies declared)

| package | repo/module | #deps |
|---|---|---|
| autoware_behavior_velocity_planner_common | autoware_core/planning | 50 |
| autoware_perception_launch | autoware_launch/autoware_universe_launch | 50 |
| autoware_motion_velocity_planner | autoware_core/planning | 49 |
| autoware_behavior_velocity_planner | autoware_core/planning | 46 |
| autoware_minimum_rule_based_planner | autoware_universe/planning | 42 |
| autoware_trajectory_processor | autoware_universe/planning | 42 |
| autoware_ndt_scan_matcher | autoware_core/localization | 41 |
| autoware_behavior_path_planner | autoware_universe/planning | 41 |
| autoware_diffusion_planner | autoware_universe/planning | 40 |
| autoware_motion_velocity_obstacle_stop_module | autoware_core/planning | 39 |

## Technology mentions (agnocast / cuda_blackboard / tensorrt / onnx)

### agnocast: 80 packages

- by module: autoware_universe/perception=17, autoware_universe/planning=14, autoware_universe/system=9, autoware_universe/control=8, autoware_core/localization=5, autoware_universe/sensing=4, autoware_core/map=3, autoware_core/planning=3, autoware_launch/autoware_universe_launch=3, autoware_universe/evaluator=3, autoware_core/sensing=2, autoware_universe/localization=2, autoware_universe/vehicle=2, autoware_core/common=1, autoware_launch/autoware_launch=1, autoware_launch/tier4_universe_launch=1, autoware_universe/map=1, autoware_universe/simulator=1
- packages: `autoware_agnocast_wrapper`, `autoware_ekf_localizer`, `autoware_gyro_odometer`, `autoware_ndt_scan_matcher`, `autoware_stop_filter`, `autoware_twist2accel`, `autoware_lanelet2_map_visualizer`, `autoware_map_loader`, `autoware_map_projection_loader`, `autoware_motion_velocity_planner`, `autoware_planning_factor_interface`, `autoware_velocity_smoother`, `autoware_gnss_poser`, `autoware_vehicle_velocity_converter`, `autoware_launch`, `autoware_control_launch`, `autoware_perception_launch`, `autoware_planning_launch`, `tier4_map_launch`, `autoware_autonomous_emergency_braking`, `autoware_collision_detector`, `autoware_control_command_gate`, `autoware_external_cmd_selector`, `autoware_lane_departure_checker`, `autoware_shift_decider`, `autoware_trajectory_follower_node`, `autoware_vehicle_cmd_gate`, `autoware_control_evaluator`, `autoware_perception_online_evaluator`, `autoware_planning_evaluator`, `autoware_localization_error_monitor`, `autoware_pose_instability_detector`, `autoware_map_tf_generator`, `autoware_crosswalk_traffic_light_estimator`, `autoware_detected_object_feature_remover`, `autoware_detected_object_validation`, `autoware_detection_by_tracker`, `autoware_euclidean_cluster`, `autoware_image_projection_based_fusion`, `autoware_map_based_prediction`, `autoware_multi_object_tracker`, `autoware_object_merger`, `autoware_object_sorter`, `autoware_raindrop_cluster_filter`, `autoware_shape_estimation`, `autoware_simple_object_merger`, `autoware_tracking_object_merger`, `autoware_traffic_light_arbiter`, `autoware_traffic_light_multi_camera_fusion`, `autoware_traffic_light_visualization`, `autoware_diffusion_planner`, `autoware_hazard_lights_selector`, `autoware_minimum_rule_based_planner`, `autoware_mission_planner_universe`, `autoware_path_optimizer`, `autoware_path_smoother`, `autoware_planning_validator`, `autoware_scenario_selector`, `autoware_trajectory_adapter`, `autoware_trajectory_concatenator`, `autoware_trajectory_processor`, `autoware_trajectory_ranker`, `autoware_trajectory_selector`, `autoware_trajectory_validator`, `autoware_cuda_pointcloud_preprocessor`, `autoware_imu_corrector`, `autoware_pointcloud_preprocessor`, `autoware_radar_objects_adapter`, `autoware_carla_interface`, `autoware_command_mode_decider`, `autoware_command_mode_switcher`, `autoware_component_state_monitor`, `autoware_diagnostic_graph_aggregator`, `autoware_mrm_comfortable_stop_operator`, `autoware_mrm_emergency_stop_operator`, `autoware_mrm_handler`, `autoware_processing_time_checker`, `autoware_topic_relay_controller`, `autoware_external_cmd_converter`, `autoware_raw_vehicle_cmd_converter`

### cuda_blackboard: 7 packages

- by module: autoware_universe/perception=6, autoware_universe/sensing=1
- packages: `autoware_bevfusion`, `autoware_ground_segmentation_cuda`, `autoware_lidar_centerpoint`, `autoware_lidar_frnet`, `autoware_lidar_transfusion`, `autoware_ptv3`, `autoware_cuda_pointcloud_preprocessor`

### tensorrt: 23 packages

- by module: autoware_universe/perception=19, autoware_launch/autoware_universe_launch=1, autoware_universe/e2e=1, autoware_universe/planning=1, autoware_universe/sensing=1
- packages: `autoware_perception_launch`, `autoware_tensorrt_vad`, `autoware_bevfusion`, `autoware_bytetrack`, `autoware_camera_streampetr`, `autoware_image_projection_based_fusion`, `autoware_lidar_apollo_instance_segmentation`, `autoware_lidar_centerpoint`, `autoware_lidar_frnet`, `autoware_lidar_transfusion`, `autoware_ptv3`, `autoware_shape_estimation`, `autoware_simpl_prediction`, `autoware_tensorrt_bevdet`, `autoware_tensorrt_bevformer`, `autoware_tensorrt_classifier`, `autoware_tensorrt_common`, `autoware_tensorrt_plugins`, `autoware_tensorrt_yolox`, `autoware_traffic_light_classifier`, `autoware_traffic_light_fine_detector`, `autoware_diffusion_planner`, `autoware_calibration_status_classifier`

### onnx: 18 packages

- by module: autoware_universe/perception=14, autoware_universe/e2e=1, autoware_universe/localization=1, autoware_universe/planning=1, autoware_universe/sensing=1
- packages: `autoware_tensorrt_vad`, `yabloc_pose_initializer`, `autoware_bevfusion`, `autoware_camera_streampetr`, `autoware_lidar_apollo_instance_segmentation`, `autoware_lidar_frnet`, `autoware_lidar_transfusion`, `autoware_ptv3`, `autoware_simpl_prediction`, `autoware_tensorrt_bevdet`, `autoware_tensorrt_bevformer`, `autoware_tensorrt_classifier`, `autoware_tensorrt_common`, `autoware_tensorrt_plugins`, `autoware_tensorrt_yolox`, `autoware_traffic_light_classifier`, `autoware_diffusion_planner`, `autoware_calibration_status_classifier`

## Packages with most node registrations (RCLCPP_COMPONENTS_REGISTER_NODE)

| package | repo/module | REGISTER_NODE | public rclcpp::Node | LOC cpp+hpp+cu |
|---|---|---|---|---|
| autoware_pointcloud_preprocessor | autoware_universe/sensing | 23 | 7 | 20222 |
| autoware_default_adapi_universe | autoware_universe/system | 15 | 15 | 2694 |
| autoware_system_monitor | autoware_universe/system | 14 | 8 | 14354 |
| yabloc_image_processing | autoware_universe/localization | 6 | 6 | 1376 |
| autoware_compare_map_segmentation | autoware_universe/perception | 6 | 0 | 3646 |
| autoware_cuda_pointcloud_preprocessor | autoware_universe/sensing | 5 | 4 | 6746 |
| autoware_image_projection_based_fusion | autoware_universe/perception | 5 | 0 | 5832 |
| autoware_detected_object_validation | autoware_universe/perception | 5 | 3 | 2825 |
| yabloc_particle_filter | autoware_universe/localization | 4 | 3 | 2613 |
| autoware_default_adapi | autoware_core/api | 3 | 3 | 1039 |
| autoware_mission_planner_universe | autoware_universe/planning | 3 | 2 | 3353 |
| autoware_probabilistic_occupancy_grid_map | autoware_universe/perception | 3 | 3 | 4886 |
| autoware_ground_segmentation | autoware_universe/perception | 3 | 0 | 3425 |
| autoware_euclidean_cluster | autoware_universe/perception | 3 | 2 | 3100 |
| autoware_diagnostic_graph_utils | autoware_universe/system | 3 | 3 | 803 |

## Largest packages by LOC (cpp+hpp+cu+py)

| package | repo/module | LOC total | cpp | hpp | cu | py |
|---|---|---|---|---|---|---|
| autoware_pointcloud_preprocessor | autoware_universe/sensing | 21319 | 12858 | 7364 | 0 | 1097 |
| autoware_trajectory | autoware_core/common | 20747 | 15604 | 5143 | 0 | 0 |
| autoware_universe_utils | autoware_universe/common | 19970 | 16862 | 3108 | 0 | 0 |
| autoware_behavior_path_planner_common | autoware_universe/planning | 17854 | 13084 | 4770 | 0 | 0 |
| autoware_multi_object_tracker | autoware_universe/perception | 17197 | 11880 | 5317 | 0 | 0 |
| autoware_motion_utils | autoware_core/common | 15836 | 12465 | 3371 | 0 | 0 |
| autoware_system_monitor | autoware_universe/system | 14354 | 11269 | 3085 | 0 | 0 |
| autoware_behavior_velocity_intersection_module | autoware_universe/planning | 14300 | 11345 | 2687 | 0 | 268 |
| autoware_trajectory_processor | autoware_universe/planning | 13696 | 9663 | 3116 | 0 | 917 |
| autoware_smart_mpc_trajectory_follower | autoware_universe/control | 11329 | 1412 | 0 | 0 | 9917 |
| autoware_diffusion_planner | autoware_universe/planning | 11057 | 8282 | 2775 | 0 | 0 |
| autoware_behavior_path_static_obstacle_avoidance_module | autoware_universe/planning | 10785 | 8172 | 2613 | 0 | 0 |
| autoware_lanelet2_utils | autoware_core/common | 10580 | 8793 | 1285 | 0 | 502 |
| autoware_behavior_path_goal_planner_module | autoware_universe/planning | 10527 | 8775 | 1752 | 0 | 0 |
| autoware_tensorrt_bevformer | autoware_universe/perception | 9833 | 4398 | 2614 | 2821 | 0 |

## Static launch include tree (depth <= 4) from `autoware_launch/autoware_launch/launch/autoware.launch.xml`

Legend: `N includes` = number of `<include file=...>` in the file; `py-leaf` = .launch.py (not parsed); `UNRESOLVED` = path uses `$(var ...)` or package not in the clone set; `MISSING` = resolved path not found.

```
- autoware_launch/autoware_launch/launch/autoware.launch.xml  [12 includes]
  - autoware_global_parameter_loader/launch/global_params.launch.py  [py-leaf]
  - autoware_launch/launch/pointcloud_container.launch.py  [py-leaf]
  - tier4_vehicle_launch/launch/vehicle.launch.xml  [1 includes]
    - $(var vehicle_launch_pkg)/launch/vehicle_interface.launch.xml  [UNRESOLVED(dynamic/pkg-not-cloned)]
  - autoware_launch/launch/components/tier4_system_component.launch.xml  [2 includes]
    - tier4_system_launch/launch/system.launch.xml  [13 includes]
      - autoware_command_mode_switcher/launch/switcher.launch.xml  [0 includes]
      - autoware_command_mode_decider/launch/decider.launch.xml  [0 includes]
      - autoware_system_monitor/launch/system_monitor.launch.xml  [0 includes]
      - autoware_duplicated_node_checker/launch/duplicated_node_checker.launch.xml  [0 includes]
      - autoware_processing_time_checker/launch/processing_time_checker.launch.xml  [1 includes]
        - autoware_agnocast_wrapper/launch/agnocast_env.launch.xml  [1 includes]
      - autoware_pipeline_latency_monitor/launch/pipeline_latency_monitor.launch.xml  [0 includes]
      - autoware_component_state_monitor/launch/component_state_monitor.launch.py  [py-leaf]
      - autoware_mrm_comfortable_stop_operator/launch/mrm_comfortable_stop_operator.launch.py  [py-leaf]
      - autoware_mrm_emergency_stop_operator/launch/mrm_emergency_stop_operator.launch.py  [py-leaf]
      - autoware_diagnostic_graph_aggregator/launch/aggregator.launch.xml  [1 includes]
        - autoware_agnocast_wrapper/launch/agnocast_env.launch.xml  [1 includes]
      - autoware_hazard_status_converter/launch/hazard_status_converter.launch.xml  [0 includes]
      - autoware_mrm_handler/launch/mrm_handler.launch.xml  [1 includes]
        - autoware_agnocast_wrapper/launch/agnocast_env.launch.xml  [1 includes]
      - autoware_dummy_diag_publisher/launch/dummy_diag_publisher.launch.xml  [1 includes]
        - autoware_dummy_diag_publisher/launch/dummy_diag_publisher_node.launch.xml  [0 includes]
    - autoware_diagnostic_graph_utils/launch/logging.launch.xml  [0 includes]
  - autoware_launch/launch/components/tier4_map_component.launch.xml  [1 includes]
    - tier4_map_launch/launch/map.launch.xml  [2 includes]
      - autoware_agnocast_wrapper/launch/agnocast_env.launch.xml  [1 includes]
        - autoware_agnocast_wrapper/launch/discovery_agent.launch.py  [py-leaf]
      - autoware_map_projection_loader/launch/map_projection_loader.launch.xml  [1 includes]
        - autoware_agnocast_wrapper/launch/agnocast_env.launch.xml  [1 includes]
  - autoware_launch/launch/components/component_sensing.launch.xml  [3 includes]
    - autoware_global_parameter_loader/launch/global_params.launch.py  [py-leaf]
    - autoware_launch/launch/pointcloud_container.launch.py  [py-leaf]
    - $(find-pkg-share $(var sensor_kit_launch_package))/launch/sensing.launch.xml  [UNRESOLVED(dynamic/pkg-not-cloned)]
  - autoware_launch/launch/components/tier4_localization_component.launch.xml  [3 includes]
    - autoware_launch/launch/pointcloud_container.launch.py  [py-leaf]
    - autoware_global_parameter_loader/launch/global_params.launch.py  [py-leaf]
    - tier4_localization_launch/launch/localization.launch.xml  [3 includes]
      - tier4_localization_launch/launch/pose_twist_estimator/pose_twist_estimator.launch.xml  [11 includes]
        - tier4_localization_launch/launch/pose_twist_estimator/ndt_scan_matcher.launch.xml  [1 includes]
        - autoware_pose_covariance_modifier/launch/pose_covariance_modifier.launch.xml  [0 includes]
        - tier4_localization_launch/launch/pose_twist_estimator/yabloc.launch.xml  [5 includes]
        - tier4_localization_launch/launch/pose_twist_estimator/gyro_odometer.launch.xml  [1 includes]
        - tier4_localization_launch/launch/pose_twist_estimator/eagleye/eagleye_rt.launch.xml  [3 includes]
        - tier4_localization_launch/launch/pose_twist_estimator/ar_tag_based_localizer.launch.xml  [1 includes]
        - tier4_localization_launch/launch/pose_twist_estimator/lidar_marker_localizer.launch.xml  [1 includes]
        - autoware_pose_estimator_arbiter/launch/pose_estimator_arbiter.launch.xml  [0 includes]
        - autoware_pose_initializer/launch/pose_initializer.launch.xml  [0 includes]
        - autoware_automatic_pose_initializer/launch/automatic_pose_initializer.launch.xml  [0 includes]
        - tier4_localization_launch/launch/util/util.launch.xml  [0 includes]
      - tier4_localization_launch/launch/pose_twist_fusion_filter/pose_twist_fusion_filter.launch.xml  [4 includes]
        - autoware_ekf_localizer/launch/ekf_localizer.launch.xml  [1 includes]
        - autoware_stop_filter/launch/stop_filter.launch.xml  [1 includes]
        - autoware_twist2accel/launch/twist2accel.launch.xml  [1 includes]
        - autoware_pose_instability_detector/launch/pose_instability_detector.launch.xml  [1 includes]
      - tier4_localization_launch/launch/localization_error_monitor/localization_error_monitor.launch.xml  [1 includes]
        - autoware_localization_error_monitor/launch/localization_error_monitor.launch.xml  [1 includes]
  - autoware_launch/launch/components/component_perception.launch.xml  [11 includes]
    - autoware_launch/launch/pointcloud_container.launch.py  [py-leaf]
    - autoware_global_parameter_loader/launch/global_params.launch.py  [py-leaf]
    - autoware_perception_launch/launch/common/pointcloud_downsample.launch.xml  [0 includes]
    - autoware_perception_launch/launch/obstacle_segmentation/ground_segmentation_rule_based_cuda.launch.xml  [0 includes]
    - autoware_perception_launch/launch/obstacle_segmentation/ground_segmentation_ml.launch.xml  [1 includes]
      - autoware_ptv3/launch/ptv3.launch.xml  [0 includes]
    - autoware_perception_launch/launch/obstacle_segmentation/ground_segmentation_rule_based.launch.xml  [0 includes]
    - autoware_perception_launch/launch/occupancy_grid_map/probabilistic_occupancy_grid_map.launch.xml  [3 includes]
      - autoware_probabilistic_occupancy_grid_map/launch/pointcloud_based_occupancy_grid_map.launch.py  [py-leaf]
      - autoware_probabilistic_occupancy_grid_map/launch/laserscan_based_occupancy_grid_map.launch.py  [py-leaf]
      - autoware_probabilistic_occupancy_grid_map/launch/multi_lidar_pointcloud_based_occupancy_grid_map.launch.py  [py-leaf]
    - autoware_perception_launch/launch/object_recognition/object_recognition_lidar_ptv3.launch.xml  [4 includes]
      - autoware_perception_launch/launch/object_recognition/detection/detector/lidar_semantic_segmentation_detector.launch.xml  [1 includes]
        - autoware_euclidean_cluster/launch/label_based_euclidean_cluster.launch.xml  [1 includes]
      - autoware_perception_launch/launch/object_recognition/detection/detector/lidar_dnn_detector.launch.xml  [7 includes]
        - autoware_lidar_centerpoint/launch/lidar_centerpoint.launch.xml  [0 includes]
        - autoware_bevfusion/launch/bevfusion.launch.xml  [0 includes]
        - autoware_lidar_transfusion/launch/lidar_transfusion.launch.xml  [0 includes]
        - autoware_lidar_centerpoint/launch/lidar_centerpoint.launch.xml  [0 includes]
        - autoware_lidar_apollo_instance_segmentation/launch/lidar_apollo_instance_segmentation.launch.xml  [0 includes]
        - autoware_shape_estimation/launch/shape_estimation.launch.xml  [1 includes]
        - autoware_detected_object_feature_remover/launch/detected_object_feature_remover.launch.xml  [1 includes]
      - autoware_multi_object_tracker/launch/multi_object_tracker.launch.xml  [1 includes]
        - autoware_agnocast_wrapper/launch/agnocast_env.launch.xml  [1 includes]
      - autoware_perception_launch/launch/object_recognition/prediction/prediction.launch.xml  [2 includes]
        - autoware_map_based_prediction/launch/map_based_prediction.launch.xml  [1 includes]
        - autoware_simpl_prediction/launch/simpl.launch.xml  [0 includes]
    - autoware_perception_launch/launch/object_recognition/object_recognition_lidar.launch.xml  [8 includes]
      - autoware_perception_launch/launch/object_recognition/detection/detector/lidar_dnn_detector.launch.xml  [7 includes]
        - autoware_lidar_centerpoint/launch/lidar_centerpoint.launch.xml  [0 includes]
        - autoware_bevfusion/launch/bevfusion.launch.xml  [0 includes]
        - autoware_lidar_transfusion/launch/lidar_transfusion.launch.xml  [0 includes]
        - autoware_lidar_centerpoint/launch/lidar_centerpoint.launch.xml  [0 includes]
        - autoware_lidar_apollo_instance_segmentation/launch/lidar_apollo_instance_segmentation.launch.xml  [0 includes]
        - autoware_shape_estimation/launch/shape_estimation.launch.xml  [1 includes]
        - autoware_detected_object_feature_remover/launch/detected_object_feature_remover.launch.xml  [1 includes]
      - autoware_perception_launch/launch/object_recognition/detection/detector/lidar_rule_detector.launch.xml  [2 includes]
        - autoware_euclidean_cluster/launch/voxel_grid_based_euclidean_cluster.launch.xml  [1 includes]
        - autoware_detected_object_feature_remover/launch/detected_object_feature_remover.launch.xml  [1 includes]
      - autoware_perception_launch/launch/object_recognition/detection/filter/pointcloud_map_filter.launch.xml  [0 includes]
      - autoware_perception_launch/launch/object_recognition/detection/filter/pointcloud_downsample_filter.launch.xml  [0 includes]
      - autoware_perception_launch/launch/object_recognition/detection/filter/object_validator.launch.xml  [2 includes]
        - autoware_detected_object_validation/launch/obstacle_pointcloud_based_validator.launch.xml  [0 includes]
        - autoware_detected_object_validation/launch/occupancy_grid_based_validator.launch.xml  [0 includes]
      - autoware_perception_launch/launch/object_recognition/detection/filter/object_filter.launch.xml  [2 includes]
        - autoware_detected_object_validation/launch/object_lanelet_filter.launch.xml  [1 includes]
        - autoware_detected_object_validation/launch/object_position_filter.launch.xml  [0 includes]
      - autoware_multi_object_tracker/launch/multi_object_tracker.launch.xml  [1 includes]
        - autoware_agnocast_wrapper/launch/agnocast_env.launch.xml  [1 includes]
      - autoware_perception_launch/launch/object_recognition/prediction/prediction.launch.xml  [2 includes]
        - autoware_map_based_prediction/launch/map_based_prediction.launch.xml  [1 includes]
        - autoware_simpl_prediction/launch/simpl.launch.xml  [0 includes]
    - autoware_perception_online_evaluator/launch/perception_online_evaluator.launch.xml  [0 includes]
    - autoware_perception_online_evaluator/launch/perception_analytics_publisher.launch.xml  [1 includes]
      - autoware_agnocast_wrapper/launch/agnocast_env.launch.xml  [1 includes]
        - autoware_agnocast_wrapper/launch/discovery_agent.launch.py  [py-leaf]
  - autoware_launch/launch/components/component_traffic_light.launch.xml  [3 includes]
    - autoware_perception_launch/launch/traffic_light_recognition/traffic_light_recognition_fine.launch.xml  [5 includes]
      - autoware_perception_launch/launch/traffic_light_recognition/traffic_light_detector_fine.launch.xml  [1 includes]
        - autoware_traffic_light_map_based_detector/launch/traffic_light_map_based_detector.launch.xml  [0 includes]
      - autoware_perception_launch/launch/traffic_light_recognition/traffic_light_occlusion_predictor.launch.xml  [1 includes]
        - autoware_traffic_light_occlusion_predictor/launch/traffic_light_occlusion_predictor.launch.xml  [0 includes]
      - autoware_perception_launch/launch/traffic_light_recognition/traffic_light_detector_fine.launch.xml  [1 includes]
        - autoware_traffic_light_map_based_detector/launch/traffic_light_map_based_detector.launch.xml  [0 includes]
      - autoware_perception_launch/launch/traffic_light_recognition/traffic_light_occlusion_predictor.launch.xml  [1 includes]
        - autoware_traffic_light_occlusion_predictor/launch/traffic_light_occlusion_predictor.launch.xml  [0 includes]
      - autoware_perception_launch/launch/traffic_light_recognition/traffic_light_fusion.launch.xml  [4 includes]
        - autoware_traffic_light_multi_camera_fusion/launch/traffic_light_multi_camera_fusion.launch.xml  [1 includes]
        - autoware_traffic_light_arbiter/launch/traffic_light_arbiter.launch.xml  [1 includes]
        - autoware_crosswalk_traffic_light_estimator/launch/crosswalk_traffic_light_estimator.launch.xml  [1 includes]
        - autoware_traffic_light_visualization/launch/traffic_light_map_visualizer.launch.xml  [1 includes]
    - autoware_perception_launch/launch/traffic_light_recognition/traffic_light_recognition_whole_image.launch.xml  [3 includes]
      - autoware_perception_launch/launch/traffic_light_recognition/traffic_light_detector_whole_image.launch.xml  [1 includes]
        - autoware_traffic_light_map_based_detector/launch/traffic_light_map_based_detector.launch.xml  [0 includes]
      - autoware_perception_launch/launch/traffic_light_recognition/traffic_light_detector_whole_image.launch.xml  [1 includes]
        - autoware_traffic_light_map_based_detector/launch/traffic_light_map_based_detector.launch.xml  [0 includes]
      - autoware_perception_launch/launch/traffic_light_recognition/traffic_light_fusion.launch.xml  [4 includes]
        - autoware_traffic_light_multi_camera_fusion/launch/traffic_light_multi_camera_fusion.launch.xml  [1 includes]
        - autoware_traffic_light_arbiter/launch/traffic_light_arbiter.launch.xml  [1 includes]
        - autoware_crosswalk_traffic_light_estimator/launch/crosswalk_traffic_light_estimator.launch.xml  [1 includes]
        - autoware_traffic_light_visualization/launch/traffic_light_map_visualizer.launch.xml  [1 includes]
    - autoware_perception_launch/launch/traffic_light_recognition/traffic_light_recognition_rough.launch.xml  [3 includes]
      - autoware_perception_launch/launch/traffic_light_recognition/traffic_light_detector_rough.launch.xml  [1 includes]
        - autoware_traffic_light_map_based_detector/launch/traffic_light_map_based_detector.launch.xml  [0 includes]
      - autoware_perception_launch/launch/traffic_light_recognition/traffic_light_occlusion_predictor.launch.xml  [1 includes]
        - autoware_traffic_light_occlusion_predictor/launch/traffic_light_occlusion_predictor.launch.xml  [0 includes]
      - autoware_perception_launch/launch/traffic_light_recognition/traffic_light_fusion.launch.xml  [4 includes]
        - autoware_traffic_light_multi_camera_fusion/launch/traffic_light_multi_camera_fusion.launch.xml  [1 includes]
        - autoware_traffic_light_arbiter/launch/traffic_light_arbiter.launch.xml  [1 includes]
        - autoware_crosswalk_traffic_light_estimator/launch/crosswalk_traffic_light_estimator.launch.xml  [1 includes]
        - autoware_traffic_light_visualization/launch/traffic_light_map_visualizer.launch.xml  [1 includes]
  - autoware_launch/launch/components/component_planning.launch.xml  [2 includes]
    - autoware_global_parameter_loader/launch/global_params.launch.py  [py-leaf]
    - autoware_planning_launch/launch/planning.launch.xml  [8 includes]
      - $(find-pkg-share $(var planning_config_pkg))/config/preset/$(var module_preset)_preset.yaml  [UNRESOLVED(dynamic/pkg-not-cloned)]
      - autoware_manual_lane_change_handler/launch/manual_lane_change_handler.launch.xml  [0 includes]
      - autoware_planning_launch/launch/mission_planning/mission_planning.launch.xml  [2 includes]
        - autoware_mission_planner_universe/launch/mission_planner.launch.xml  [1 includes]
        - autoware_mission_planner_universe/launch/goal_pose_visualizer.launch.xml  [0 includes]
      - autoware_planning_launch/launch/scenario_planning/scenario_planning.launch.xml  [6 includes]
        - autoware_scenario_selector/launch/scenario_selector.launch.xml  [0 includes]
        - autoware_external_velocity_limit_selector/launch/external_velocity_limit_selector.launch.xml  [0 includes]
        - autoware_agnocast_wrapper/launch/agnocast_env.launch.xml  [1 includes]
        - autoware_hazard_lights_selector/launch/hazard_lights_selector.launch.xml  [1 includes]
        - autoware_planning_launch/launch/scenario_planning/lane_driving.launch.xml  [2 includes]
        - autoware_planning_launch/launch/scenario_planning/parking.launch.xml  [0 includes]
      - autoware_planning_launch/launch/learning_based_planning/diffusion_planner.launch.xml  [2 includes]
        - autoware_diffusion_planner/launch/diffusion_planner.launch.xml  [0 includes]
        - autoware_trajectory_processor/launch/trajectory_processor.launch.xml  [1 includes]
      - autoware_planning_validator/launch/planning_validator.launch.xml  [0 includes]
      - autoware_planning_evaluator/launch/planning_evaluator.launch.xml  [1 includes]
        - autoware_agnocast_wrapper/launch/agnocast_env.launch.xml  [1 includes]
      - autoware_remaining_distance_time_calculator/launch/remaining_distance_time_calculator.launch.xml  [0 includes]
  - autoware_launch/launch/components/component_control.launch.xml  [2 includes]
    - autoware_global_parameter_loader/launch/global_params.launch.py  [py-leaf]
    - autoware_control_launch/launch/control.launch.xml  [7 includes]
      - $(var control_config_dir)/preset/$(var module_preset)_preset.yaml  [UNRESOLVED(dynamic/pkg-not-cloned)]
      - autoware_agnocast_wrapper/launch/agnocast_env.launch.xml  [1 includes]
        - autoware_agnocast_wrapper/launch/discovery_agent.launch.py  [py-leaf]
      - autoware_control_launch/launch/trajectory_follower/trajectory_follower.launch.xml  [0 includes]
      - autoware_control_launch/launch/command_gate/command_gate.launch.xml  [2 includes]
        - autoware_control_command_gate/launch/control_command_gate.launch.xml  [0 includes]
        - autoware_stop_mode_operator/launch/stop_mode_operator.launch.xml  [0 includes]
      - autoware_control_launch/launch/external_command/external_command.launch.xml  [2 includes]
        - autoware_external_cmd_selector/launch/external_cmd_selector.launch.py  [py-leaf]
        - autoware_external_cmd_converter/launch/external_cmd_converter.launch.py  [py-leaf]
      - autoware_control_launch/launch/control_checker/control_checker.launch.xml  [0 includes]
      - autoware_control_evaluator/launch/control_evaluator.launch.xml  [1 includes]
        - autoware_agnocast_wrapper/launch/agnocast_env.launch.xml  [1 includes]
  - autoware_launch/launch/components/tier4_autoware_api_component.launch.xml  [2 includes]
    - autoware_global_parameter_loader/launch/global_params.launch.py  [py-leaf]
    - tier4_autoware_api_launch/launch/autoware_api.launch.xml  [3 includes]
      - autoware_default_adapi_universe/launch/default_adapi.launch.py  [py-leaf]
      - autoware_adapi_adaptors/launch/rviz_adaptors.launch.xml  [0 includes]
      - autoware_evaluation_adapter/launch/evaluation_adapter.launch.xml  [1 includes]
        - autoware_evaluation_adapter/launch/namespace.launch.py  [py-leaf]
```

- lines: 195; resolved xml nodes: 167, py-leaf: 24, unresolved: 4, missing: 0

