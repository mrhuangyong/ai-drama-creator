---
name: ad-xuanhuan-engine
description: 独立设计玄幻修仙、仙侠斗法、飞剑、法阵、法相、巨兽与神魔群战的分镜提示词，保留原文强弱与结果，写清元素材质、尺度、攻防反馈及跨段连续性，支持15秒及30秒，不依赖总控或其他技能。
metadata:
  version: "1.0.0-standalone"
  origin: "漫剧老李 V7.5.0-SLIM 本地独立改造"
---

# 玄幻仙侠打戏分镜·独立版

## 直接开始

读[独立接收与连续性](references/standalone-usage.md)和[输出格式](references/output-format.md)。直接处理用户材料，不需要外部总控、锁文件、其他技能或图片。未指定且未明确沿用片段时长时，先询问15秒还是30秒；可以先整理动作，不能自行默认交稿时长。只产提示词文本，不运行媒体生成。

保留原文人物能力、目的、台词、胜负与伤亡结果；补动作不能篡改剧情。缺少图片可用文字基准，已有姓名、图号与别名沿用。成稿默认用户案例的“风格→场景→站位参考→发声角色声音→镜头一：（X秒）自然句→负面”格式，用户另指定时覆盖。全段整数秒累计到确认时长，超过30秒按已确认规格连续分段。

## 独立工作步骤

1. 在当前材料中整理角色状态、空间轴线、武器与战损、环境参照物和段缝；不索要外部流程产物。
2. 定动机、强弱差、赌注与环境变化，选择贴身、武侠、远程法术或群战。五段节奏、三轮反杀等只作合适场面的模板；碾压、缴械、救人不强写双方受创。
3. 每镜确定任务、机位与一个主要攻防动作，通常2—3秒、复杂节点可4秒；动作发生后有即时身体、兵器或环境反馈。先让人看懂力从哪里来，再描述运镜和特效。
4. 按风格写材质、能量来源与运动方向；大招交代画框占比、量级、参照物与人物相对位置。3D不强加手绘笔法，写实不强加气爆，大场面不套贴身时长配额。
5. 收束到原文结果或下一段可承接的状态；自检轴线、伤势、持物、攻防因果、对白完整和时长。仅在需要时解释设计选择，代码块只留模型可读的画面与声音语言。

## 本地知识库

生成前读[ core-combat-laws.md ](references/core-combat-laws.md)及[ combat-rhythm-and-load-guardrails.md ](references/combat-rhythm-and-load-guardrails.md)的适用档位；其他按场面读取。完整玄幻库与用到的通用打戏补充已全部内置references/，复制此文件夹即可独立使用。

| 内容 | 本地文件 | 何时使用 |
| --- | --- | --- |
| 颗粒度、反馈与收束 | [core-combat-laws.md](references/core-combat-laws.md) | 每次设计玄幻打戏 |
| 镜头与空间 | [camera-specs-15modes.md](references/camera-specs-15modes.md) | 机位与运镜 |
| 贴身对招 | [close-quarters-engine.md](references/close-quarters-engine.md) | 近身攻防与微反馈 |
| 三层复合元素 | [xuanhuan-elements-vfx.md](references/xuanhuan-elements-vfx.md) | 术法材质、阵营色、3D表现 |
| 巨物、飞剑与法相 | [grand-scale-domains.md](references/grand-scale-domains.md) | 宏观尺度与构图参照 |
| 法武合一与参数 | [arsenal-moves-library.md](references/arsenal-moves-library.md)、[arsenal-parameter-library.md](references/arsenal-parameter-library.md) | 招式动作与物理量转画面 |
| 人物场景预设 | [character-scene-presets.md](references/character-scene-presets.md) | 信息缺失时最小设计，不覆盖用户角色 |
| 史诗战场 | [epic-battlefield-protocols.md](references/epic-battlefield-protocols.md) | 群战、位移、武器变形 |
| 本地节奏与激烈度 | [combat-rhythm-and-load-guardrails.md](references/combat-rhythm-and-load-guardrails.md)、[combat-intensity-guardrails.md](references/combat-intensity-guardrails.md) | 远程术法与法阵不强迫肉搏 |
| 笔法与冲击帧 | [vfx-rendering-mandate.md](references/vfx-rendering-mandate.md)、[impact-frame-and-banlist.md](references/impact-frame-and-banlist.md) | 水墨／2D用笔法，3D保留立体材质 |
| 动机与自然句 | [combat-construction.md](references/combat-construction.md)、[eight-sentence-masters.md](references/eight-sentence-masters.md) | 补足动机、动作因果和自然投喂句 |

## 交付检查

运行本目录中的`python scripts/check_combat_prompt.py 成稿.md --duration 15`（30秒版用`--duration 30`）。检查器只核对本地格式与时间，不承诺测出所有肢体、尺度或语义问题；另人工核对剧情结果、攻防反馈、跨镜伤势及轴线。不调用或宣称通过外部总控检查器。只有用户确认的素材才可说已提供参考图。
