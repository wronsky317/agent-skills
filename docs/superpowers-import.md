# Superpowers skills 吸收映射

本仓库从 [obra/superpowers](https://github.com/obra/superpowers) 吸收并适配通用工程工作流。基线 commit：`b36e0829c6d0140e93cfef2ca599b1b07d4a7797`（本地源目录状态无未提交修改）。

这里的“吸收”指按当前仓库的触发规则、分类、共享工作区模型和安全边界进行治理式整合，不保证与上游文件逐字同步。

## 映射

| 上游 skill | 当前仓库处理 |
|---|---|
| `brainstorming` | 已存在于 `skills/productivity/brainstorming`，保留当前较温和的触发与 runtime 适配 |
| `dispatching-parallel-agents` | 新增到 `skills/productivity/dispatching-parallel-agents` |
| `executing-plans` | 新增到 `skills/engineering/executing-plans`，与 `plan-tracker` 分离“执行”和“状态持久化” |
| `finishing-a-development-branch` | 新增到 `skills/engineering/finishing-a-development-branch` |
| `receiving-code-review` | 新增到 `skills/engineering/receiving-code-review` |
| `requesting-code-review` | 新增到 `skills/engineering/requesting-code-review`；现有 `code-review` 负责实际审查 |
| `subagent-driven-development` | 新增到 `skills/engineering/subagent-driven-development`，适配共享文件系统和授权边界 |
| `systematic-debugging` | 合并到现有 `skills/engineering/investigate`，保留根因追踪、分层防御、条件等待和污染测试定位资源 |
| `test-driven-development` | 新增到 `skills/engineering/test-driven-development`，把严格 TDD 限定在用户或计划明确要求的场景 |
| `using-git-worktrees` | 新增到 `skills/engineering/using-git-worktrees`，适配 host-managed workspace 和 `codex/` 分支前缀 |
| `using-superpowers` | 不导入；它是上游插件的全局强制启动器，与本仓库/runtime 的 skill 路由规则冲突 |
| `verification-before-completion` | 新增到 `skills/engineering/verification-before-completion` |
| `writing-plans` | 合并到现有 `skills/engineering/implementation-plan`，补入任务粒度、接口契约、占位符扫描和自审 |
| `writing-skills` | 由现有 `skills/skill-management/create-skill` 与 `skill-repo-governance` 覆盖；不新增同触发 skill |

## 适配原则

- 删除或改写 `superpowers:`、Claude 专用工具名和“每轮必须触发”等宿主耦合要求。
- 并行代理默认共享同一文件系统；只有明确授权且文件所有权不重叠时才并行写入。
- Git 合并、推送、PR、worktree 删除等外部或破坏性动作继续遵守当前 runtime 的用户授权规则。
- 新增 skill 的描述同时说明能力和触发条件，并与相邻 skill 保持边界。
- 长案例和模板放入一级 `references/`，确定性脚本放入 `scripts/`。

## 上游同步

后续同步时先比较上游 commit，再按本映射逐项审查；不要用整目录覆盖本地适配。新增上游 skill 先做重叠检查，再决定新增、合并或排除。
