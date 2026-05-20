# Agent Skills

这个目录集中管理本机多个 agent/IDE 共用的 skills。目标是让 Qoder、QoderWork、Codex 等工具共享同一套 skill 内容，同时保留一个适合人工维护的分类目录。

大部分 skill 来自外部或系统安装，少部分是本机定制。`悟空` 相关内容除外。

## 目录结构

```text
agent-skills/
  config/
    agents.conf.example # 可提交的配置模板
    agents.conf         # 本机配置，不提交 git
  skills/             # 真实的人工归档目录，所有可共享 skill 的源文件放这里
  scripts/            # 维护脚本
  .system/            # 系统 skills，通常不要手动改
  README.md
```

脚本会根据自身所在位置自动推导 `agent-skills/` 根目录，不依赖固定用户名或固定安装路径。把这个目录放到别的用户、别的机器或别的父目录下也可以使用。

## 配置文件

同步对象写在本机配置文件：

```text
config/agents.conf
```

这个文件不提交 git，避免不同机器、不同用户的本地路径频繁制造 diff。第一次使用时，从模板复制：

```bash
cp config/agents.conf.example config/agents.conf
```

格式是：

```text
agent_name|skills_directory
```

模板默认配置：

```text
qoder|$HOME/.qoder/skills
qoderwork|$HOME/.qoderwork/skills
codex|$HOME/.codex/skills
```

说明：

- 空行和 `#` 开头的行会被忽略。
- `agent_name` 只能包含字母、数字、下划线和短横线。
- 路径可以使用 `$HOME` 或 `~`。
- 想增加 Claude Code，可以加一行：`claude|$HOME/.claude/skills`。
- 想临时使用另一份配置，可以设置环境变量：`AGENT_SKILLS_CONFIG=/path/to/agents.conf scripts/doctor.sh`。

也可以覆盖默认目录：

```bash
AGENT_SKILLS_ROOT=/path/to/skills scripts/link-skills.sh
AGENT_SKILLS_SYSTEM_DIR=/path/to/system-skills scripts/link-skills.sh
```

## Skill 归档目录

`skills/` 内部按用途分类：

```text
skills/
  documents/          # docx/pdf/pptx/xlsx 等文档处理
  engineering/        # 工程、诊断、项目内工具
  personal/           # 个人知识库、周报等个人工作流
  productivity/       # 思考、访谈、规划类工作流
  skill-management/   # 创建、发现、安装、维护 skill 的元技能
  inbox/              # 从各 agent 自动导入的新 skill，等待人工归档
  in-progress/        # 未稳定的新 skill
  deprecated/         # 暂时保留但不推荐继续使用的 skill
```

每个具体 skill 目录里应该包含 `SKILL.md`：

```text
skills/documents/pdf/SKILL.md
skills/engineering/map-viser-page/SKILL.md
```

## Agent 入口目录

本机 `config/agents.conf` 中配置的目录是给各 agent/IDE 扫描用的。它们不是主管理目录，而是一级软链接入口。也就是说，agent 看到的是：

```text
~/.codex/skills/pdf -> <agent-skills>/skills/documents/pdf
```

这样做的原因是有些 agent 只扫描 skills 目录的一级子目录。真实文件可以按分类存储，但暴露给 agent 时仍保持一级目录，兼容性最好。

## 从零部署

在一台新机器或新用户环境中部署时，按下面顺序执行。

### 1. 克隆仓库

把仓库克隆到你希望长期维护的位置，例如：

```bash
mkdir -p ~/Documents
git clone git@gitlab.alibaba-inc.com:shigu.rsk/skills.git ~/Documents/agent-skills
cd ~/Documents/agent-skills
```

如果你已经通过别的方式拿到了这个目录，直接进入目录即可：

```bash
cd /path/to/agent-skills
```

### 2. 创建本机配置

本机配置不提交 git，需要从模板复制：

```bash
cp config/agents.conf.example config/agents.conf
```

然后按当前机器安装的 agent 修改 `config/agents.conf`：

```text
qoder|$HOME/.qoder/skills
qoderwork|$HOME/.qoderwork/skills
codex|$HOME/.codex/skills
# claude|$HOME/.claude/skills
```

不使用的 agent 可以删掉或注释掉。新增 agent 时增加一行 `agent_name|skills_directory`。

### 3. 生成 agent 入口软链接

运行：

```bash
scripts/link-skills.sh
```

这个命令会：

- 扫描 `skills/**/SKILL.md`。
- 为每个配置的 agent skills 目录创建一级软链接。
- 如果 `.system/` 存在，尝试给 agent 入口目录创建 `.system` 软链接。
- 遇到同名 skill 时停止，避免链接到错误目录。

### 4. 检查部署结果

运行：

```bash
scripts/doctor.sh
```

确认输出里：

- `config` 指向本机 `config/agents.conf`。
- `skills root` 指向当前仓库的 `skills/`。
- `agent targets` 中每个 agent 都是 `directory target`。
- 每个 agent 目录下都有一批一级软链接。

### 5. 重启 agent/IDE

改完链接后，重启 Qoder、QoderWork、Codex 或其他相关 IDE/CLI，让它们重新扫描 skills。

## 每日例行

日常维护可以按下面顺序执行。建议在仓库根目录运行：

```bash
cd /path/to/agent-skills
```

### 1. 拉取远端更新

```bash
git pull --ff-only
```

如果远端新增、移动或删除了 skill，拉取后需要刷新本机 agent 入口软链接。

### 2. 导入本机 agent 新建的 skill

```bash
scripts/import-new-skills.sh
```

这个命令会扫描 `config/agents.conf` 中的 agent 目录。如果某个 agent 自己创建了真实 skill 目录，例如：

```text
~/.qoder/skills/new-skill/SKILL.md
```

它会被移动到：

```text
skills/inbox/qoder/new-skill/
```

然后脚本会自动调用 `link-skills.sh` 重新生成软链接。

### 3. 检查状态

```bash
scripts/validate-skills.py
scripts/doctor.sh
git status --short
```

如果 `skills/inbox/` 里出现新 skill，可以人工归档到合适分类，然后再运行：

```bash
scripts/link-skills.sh
```

### 4. 提交并推送自己的更新

当你新增、修改或归档了可共享 skill 后：

```bash
git add -A
git commit -m "Update shared skills"
git push
```

不要提交 `config/agents.conf` 和 `.system/`，它们应该被 `.gitignore` 忽略。

## 常用命令

下面的命令都可以从任意目录执行：

```bash
/path/to/agent-skills/scripts/doctor.sh
```

检查当前状态，包括配置文件、主管理目录、已管理的 skills、各 agent 入口目录。

```bash
/path/to/agent-skills/scripts/link-skills.sh
```

根据 `skills/` 重新生成所有 agent 的一级软链接。

```bash
/path/to/agent-skills/scripts/import-new-skills.sh
```

从各 agent 目录导入新建 skill，并重新生成链接。

```bash
/path/to/agent-skills/scripts/validate-skills.py
```

检查所有 `skills/**/SKILL.md` 的 frontmatter、命名、触发描述、流程章节和验证章节。结构错误会返回非零状态；历史质量问题以 warning 输出，作为后续治理清单。

## 新增 Skill 的推荐方式

推荐直接在主管理目录中创建：

```text
skills/inbox/manual/my-new-skill/SKILL.md
```

然后运行：

```bash
scripts/link-skills.sh
```

确认稳定后，再把它从 `skills/inbox/manual/` 移到合适分类，例如：

```text
skills/engineering/my-new-skill/
skills/personal/my-new-skill/
skills/skill-management/my-new-skill/
```

移动后再次运行 `link-skills.sh`。

## Agent 自己创建新 Skill 时

如果某个 agent 在自己的入口目录里创建了真实目录，例如：

```text
~/.qoder/skills/new-skill/SKILL.md
```

这个目录不会自动出现在主管理目录里。此时运行：

```bash
scripts/import-new-skills.sh
```

脚本会把它导入到：

```text
skills/inbox/qoder/new-skill/
```

然后自动重新生成软链接。你可以之后再人工归档到更合适的分类。

## 脚本说明

### `scripts/config.sh`

公共配置加载器，不需要直接执行。它被 `doctor.sh`、`link-skills.sh`、`import-new-skills.sh` 通过 `source` 引入。

它负责：

- 自动定位 `agent-skills/` 根目录。
- 读取本机 `config/agents.conf`。
- 如果本机配置不存在，提示从 `config/agents.conf.example` 创建。
- 展开 `$HOME` 和 `~`。
- 生成脚本内部使用的 agent 名称和目标目录列表。

### `scripts/link-skills.sh`

扫描：

```text
skills/**/SKILL.md
```

然后在配置文件列出的 agent 目录中创建或更新一级软链接。

如果发现同名 skill，会拒绝执行，避免一个入口名指向两个不同 skill。

如果目标位置已经存在同名的真实目录或文件，脚本会跳过它，不会覆盖。

### `scripts/import-new-skills.sh`

扫描配置文件列出的 agent 入口目录，寻找“真实目录且包含 `SKILL.md`”的新 skill。软链接会被忽略。

找到后会移动到：

```text
skills/inbox/<agent-name>/<skill-name>/
```

如果目标已存在，会自动追加时间戳，避免覆盖。

最后会调用 `link-skills.sh` 刷新所有入口。

### `scripts/validate-skills.py`

扫描所有分类目录下的 `SKILL.md`：

- `name` 和目录名必须一致。
- `description` 必须存在，且不能超过 1024 字符。
- 缺少触发语义、流程章节、验证章节或超过 500 行会输出 warning。
- 引用疑似不存在的 skill 会输出 warning。

### `scripts/doctor.sh`

打印当前配置、管理的 skill 列表，以及各 agent 入口目录的链接状态。用于迁移后、改分类后、排查 skill 未加载时快速检查。

## `.system` 目录

`.system/` 保存系统安装的 skills，通常不要人工移动到 `skills/`。

`link-skills.sh` 会尽量给各 agent 入口目录建立 `.system` 软链。如果某个 agent 自己维护真实 `.system` 目录，脚本会跳过，不会覆盖。

## 维护约定

- 一个 skill 名只能出现一次，也就是 `SKILL.md` 所在目录的 basename 必须唯一。
- 真实 skill 放在 `skills/` 下，agent 入口目录只作为软链接层。
- 稳定 skill 放到明确分类里，未归档 skill 先放 `skills/inbox/`。
- 不直接手改 agent 入口目录里的软链接；需要刷新时跑 `link-skills.sh`。
- 改完结构后重启对应 agent/IDE，让它重新扫描 skills。
