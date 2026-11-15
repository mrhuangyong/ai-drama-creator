---
name: ad-combat-engine
description: 独立设计打斗、武打、动作戏与群战分镜提示词，从剧本或动作梗概直接编排动机、发力、攻防反馈、机位与收束，支持15秒及30秒；适用于通用武侠、写实动作及商业高燃场面，不依赖总控工作流。
metadata:
  version: "1.0.0-standalone"
  origin: "漫剧老李 V7.5.0-SLIM 本地独立改造"
---

# 通用打戏分镜·独立版

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

每次动作生成先读[ combat-iron-laws.md ](references/combat-iron-laws.md)中的核心动作链与[ combat-rhythm-and-load-guardrails.md ](references/combat-rhythm-and-load-guardrails.md)的适用档位；按本入口的剧情优先级选用，不把整本硬燃模板全部套上。以下文件均位于references/。

| 内容 | 本地文件 | 何时使用 |
| --- | --- | --- |
| 动作核心、强度与终结 | [combat-iron-laws.md](references/combat-iron-laws.md)、[tier-and-finisher-system.md](references/tier-and-finisher-system.md) | 确定动作强度、收束方式 |
| 动机与自然句 | [combat-construction.md](references/combat-construction.md)、[eight-sentence-masters.md](references/eight-sentence-masters.md) | 编排、逐镜成句 |
| 招式与句法 | [moves-library.md](references/moves-library.md)、[syntax-corpus.md](references/syntax-corpus.md) | 按武器取材，不照抄工程标记 |
| 摄影与场景 | [combat-cheatsheet.md](references/combat-cheatsheet.md)、[presets-library.md](references/presets-library.md) | 运镜、群战、风格 |
| 大招与术法 | [ultimate-array-library.md](references/ultimate-array-library.md)、[spell-system.md](references/spell-system.md) | 阵法、终结、法术 |
| 媒介与转译 | [seedance-dual-engine.md](references/seedance-dual-engine.md)、[vfx-rendering-mandate.md](references/vfx-rendering-mandate.md) | 沿用用户模型与3D／2D基底 |
| 节奏与负载 | [combat-rhythm-and-load-guardrails.md](references/combat-rhythm-and-load-guardrails.md)、[combat-intensity-guardrails.md](references/combat-intensity-guardrails.md) | 按近身／远程／大场面区别核对 |
| 冲击与局部负面 | [impact-frame-and-banlist.md](references/impact-frame-and-banlist.md) | 选本镜最易崩点 |
| 写实与多人 | [physical-combat-basics.md](references/physical-combat-basics.md) | 不含超能力的动作 |
| 玄幻补充（已内置） | [core-combat-laws.md](references/core-combat-laws.md)、[grand-scale-domains.md](references/grand-scale-domains.md)、[xuanhuan-elements-vfx.md](references/xuanhuan-elements-vfx.md) | 玄幻尺度、元素与攻防；其余玄幻专库按这些文件的本地引用查阅 |

## 交付检查

运行本目录中的`python scripts/check_combat_prompt.py 成稿.md --duration 15`（30秒版用`--duration 30`）。检查器只核对本地格式与时间，不承诺测出所有肢体、尺度或语义问题；另人工核对剧情结果、攻防反馈、跨镜伤势及轴线。不调用或宣称通过外部总控检查器。只有用户确认的素材才可说已提供参考图。
