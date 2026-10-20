# Robot Payload Catalog

An open dataset of **35 robot platforms** (quadruped robot dogs, UGVs and drones) and **198 payload components** (LiDAR, depth cameras, gimbals, thermal cores, RTK receivers, edge compute, radios, power modules and robot arms), with weight, power, size and source links — plus a small command-line tool to budget payload weight and power.

It is the data behind the free 3D [online payload configurator](https://www.yuanzhirobot.com/?lang=en#config) by [YUANZHI ROBOTICS](https://www.yuanzhirobot.com/en/).

## What is inside

| File | Contents |
|---|---|
| `data/platforms.json` / `.csv` | 35 platforms: Unitree B2 / B2-W / Go2 EDU / Go2-W / A2 / AS2 / B1 / Go1 / A1, Boston Dynamics Spot, ANYbotics ANYmal C / D, DEEP Robotics X30 / Lite3 / M20, Clearpath Husky A200 / Jackal / Warthog / Ridgeback / Dingo-D, AgileX Scout Mini / Hunter 2.0 / Hunter SE / Bunker / Bunker Pro / Bunker Mini / Tracer / Tracer 2.0, DJI Matrice 400 / 350 RTK / 300 RTK / 30T / 4T / 4TD / Mavic 3 Enterprise. Fields: category, weight, rated payload, dimensions, native sensors. |
| `data/payload_items.json` / `.csv` | 198 components in 15 types: `lidar`, `radar`, `depth_camera`, `gimbal_pod`, `thermal_core`, `360_camera`, `rtk_receiver`, `gnss_antenna`, `imu_ins`, `gas_acoustic`, `speaker_light_mic`, `edge_compute`, `comms_radio`, `power_network`, `robot_arm`. Fields: weight (g), power (W), size (mm), notes, key specs, source URL, data quality. |
| `payload_budget.py` | Adds up weight and power for a platform plus a list of items, with an allowance for brackets and cables, and compares the total with the rated payload. |

`data_quality` tells you where a number came from: `official` (manufacturer datasheet or product page), `official_partial`, `reseller_listing_of_official`, `reseller`, `distributor_list`. Empty weight or power means we did not find a reliable figure.

## Quick start

Python 3.8+, no dependencies.

```bash
python payload_budget.py --platforms
python payload_budget.py --items lidar
python payload_budget.py go2 livox-mid360 orbbec-gemini335 nv-orin-nano-super-dk
```

Example output:

```
Platform: Unitree Go2 EDU (quadruped)
  - Livox Mid-360: 265 g, 6.5 W
  - Orbbec Gemini 335: 97 g, 3 W
  - NVIDIA Jetson Orin Nano Super Developer Kit: weight unknown, 25 W
Sensors and compute: 0.36 kg, 34.5 W
With 25% allowance for brackets and cables: 0.45 kg
Rated payload 8 kg -> 6% used (OK)
No weight data for: nv-orin-nano-super-dk
```

Change the allowance with `--margin 0.4`. Rated payload is the OEM reference figure; runtime, center of mass and stair performance get worse well before you reach it, so the tool flags anything above 60% as "tight".

## Accuracy

All figures are reference values compiled from public manufacturer datasheets and listings. They can be out of date or differ between product versions — check the official specification before you design or buy. Corrections are welcome: open an issue or a pull request with a source link.

Product names and trademarks belong to their owners. This project is not affiliated with or endorsed by any of the manufacturers listed.

## Want it built?

YUANZHI ROBOTICS (Beijing Yuanzhi Technology Co., Ltd.) designs and integrates sensor payloads and does secondary development for robot dogs, UGVs and drones: back shells and mounts, harnesses, compute and comms, ROS 2 mapping and navigation, recognition and ground-station software.

- Solutions: [English](https://www.yuanzhirobot.com/en/) · [Español](https://www.yuanzhirobot.com/es/) · [Português](https://www.yuanzhirobot.com/pt/) · [Français](https://www.yuanzhirobot.com/fr/) · [Deutsch](https://www.yuanzhirobot.com/de/) · [Русский](https://www.yuanzhirobot.com/ru/) · [العربية](https://www.yuanzhirobot.com/ar/) · [日本語](https://www.yuanzhirobot.com/ja/) · [한국어](https://www.yuanzhirobot.com/ko/) · [中文](https://www.yuanzhirobot.com/zh/)
- 3D configurator: https://www.yuanzhirobot.com/?lang=en#config
- Email: lizhongpan@yuanzhirobot.com

## 中文说明

本仓库整理了 35 款机器人平台（四足机器狗、无人车、无人机）和 198 款上装部件（激光雷达、深度相机、云台、热成像、RTK、算力、通信、电源、机械臂）的重量、功耗、尺寸和资料出处，并附一个重量功耗核算小工具。数据来自厂商公开资料，仅供选型参考，以官方最新规格为准。在线三维上装配置器：https://www.yuanzhirobot.com/#config ，北京垣知科技有限公司（垣知科技）。

## License

Code (`payload_budget.py`): MIT. Data (`data/`): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — free to use, including commercially, with attribution to "YUANZHI ROBOTICS Robot Payload Catalog".
