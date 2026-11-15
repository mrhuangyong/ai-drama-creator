# AI Drama Creator

中文 AI 漫剧创作技能包：从短篇、网文或长篇小说出发，完成正式剧本、视觉资产提取与 Seedance 分镜提示词；打斗场景自动使用通用或玄幻打戏知识推理。

## 技能组成

| 技能 | 用途 |
| --- | --- |
| [drama-creator](skills/drama-creator/SKILL.md) | 总控入口，串联剧本 → 资产 → 分镜，并自动路由打戏 |
| [ad-novel-to-screenplay](skills/ad-novel-to-screenplay/SKILL.md) | 小说改编，按实际篇幅组织阅读、分集与正式剧本 |
| [ad-asset-engine](skills/ad-asset-engine/SKILL.md) | 人物、场景、道具及群体资产，生图提示词与素材接线单 |
| [ad-seedance25-shot-prompts](skills/ad-seedance25-shot-prompts/SKILL.md) | 保留动作、对白、旁白，输出15秒／30秒分镜提示词 |
| [ad-combat-engine](skills/ad-combat-engine/SKILL.md) | 写实、武侠与物理动作的发力、攻防反馈、机位设计 |
| [ad-xuanhuan-engine](skills/ad-xuanhuan-engine/SKILL.md) | 玄幻术法、飞剑、法阵、法相、巨兽与大场面设计 |

专业技能统一以 `ad-` 开头，入口按指定保留 `drama-creator`。五个专业技能可独立使用；总控需要它们与自己处于同一父目录。

## 下载和安装

下载 [v1.0.0 完整技能包](dist/ai-drama-creator-v1.0.0.zip)，或克隆仓库：

```bash
git clone https://github.com/mrhuangyong/ai-drama-creator.git
cd ai-drama-creator
```

将 `skills/` 里面的**六个技能文件夹**复制到 Codex 的技能目录，默认是 `~/.codex/skills/`。保持六者同级，不能只复制总控，也不要把 `skills` 整体作为一个技能文件夹。已有同名技能时先核对并备份自己的修改，再更新文件。

首次安装的示例命令（会复制六个目录，执行前确认目标没有需要保留的同名版本）：

```bash
mkdir -p ~/.codex/skills
cp -R skills/drama-creator skills/ad-* ~/.codex/skills/
```

安装后重新打开使用技能的会话；支持直接读取本地技能文件的客户端，也可指定 `skills/drama-creator/SKILL.md` 的完整路径。这里只安装文本规则和本地检查脚本，不配置视频供应商或收费服务。

## 使用示例

全流程：

```text
使用 $drama-creator，将我提供的小说改编成AI漫剧，完成剧本、资产提取和30秒版分镜提示词。
画风沿用3D国漫CG，保留原著人物、主线和结局。
```

从已有成果继续：

```text
使用 $drama-creator，读取已有八集剧本，从资产提取继续，最后输出15秒版分镜提示词。
```

只处理一个环节：

```text
使用 $ad-asset-engine，为这个剧本提取人物、场景和道具，输出生图提示词与素材接线单。
```

没有明确选择分镜时长时会先询问15秒、30秒或两版；用户答复前可读取材料、写剧本和提资产，不先排依赖时长的镜头。单集剧本可长于30秒，最终拆成多个已确认时长的片段。

## 工作流与交付约定

1. **剧本**：按实际阅读覆盖整理来源、人物、剧情与分集，再写场景、动作和对白；不把章节摘要当剧本，不为短篇硬凑集数。
2. **打戏推理与资产**：识别真实攻击、格挡、闪避或施法对抗，按戏型读取打戏规则，梳理必要武器与状态后提取资产；持剑聊天或威胁台词不会自动扩写成战斗。
3. **分镜提示词**：以生效剧本、资产及动作设计排程，文戏和打戏统一成自然语言案例格式，保留语音内容与跨段连续性。

人物设定图顶部居中只写角色本名，音色说明与英文标签留在图外。图片尚未生成时，引用仍为待绑定占位，不会冒称已经上传或锁定。

通用打戏与玄幻打戏推理保持原文强弱、胜负与伤亡结果；不强迫每场三轮反杀或双方受伤。混合场面共享人物、武器、空间与伤势状态，最后统一由分镜技能排镜和检查语音时长。

默认交付 Markdown 剧本、资产清单及生图提示词、接线单、分集分镜文件与完整合集。技能本身不生成图片、视频、配音，不上传原小说。

## 本地检查与重新打包

Python 3.9及以上，无需额外Python依赖：

```bash
python3 scripts/check.py
python3 scripts/package.py
```

检查包括六个技能的命名、总控引用、相对链接和55项现有测试。检查器验证文本结构、时长或配置；原著覆盖、动作因果、角色一致性和实际出片效果仍需人工核对，不能用测试通过代替成片验证。

重新打包会生成 `dist/ai-drama-creator-v<版本>.zip` 与 SHA-256 校验文件。ZIP内含说明和完整 `skills/`，排除缓存、Git目录与本地项目材料。

## 来源

资产与打戏技能由所提供的“漫剧老李 V7.5.0-SLIM”规则改造成本地独立版，保留原知识库和来源标记；详见 [来源说明](THIRD_PARTY_NOTICES.md)。本仓库不包含课程视频、原始小说、PDF课件或真实项目媒体素材。
