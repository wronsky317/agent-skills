---
name: codex-subagent-routing
description: Install, enable, and validate four Codex subagent roles by creating TOML files and writing global AGENTS.md delegation rules. Use when users ask to 安装或启用自动委派、配置子 Agent 调度、迁移四角色模型配置. For a Luna-only setup use the existing luna-subagent skill; ordinary task execution follows installed AGENTS.md rules without reinstalling this bundle.
---

# Codex Subagent Routing

Package the user's four-role selection policy as personal Codex agents and a small global instruction section. This skill manages configuration; installed AGENTS.md rules guide subsequent delegation. It does not switch the primary model or guarantee that every task triggers delegation.

## Workflow

1. Identify whether the user requests inspection, installation/enablement, or replacement. “安装这套配置”, “启用自动委派”, “用这个 Skill 配置子 Agent 调度”, or an invocation of this skill to set up delegation authorizes the complete automatic setup below. Proceed through writing and verification without asking separately for permission to create TOML files or update the delegation section. Packaging/editing the skill itself, a bare mention of its name, and inspection-only requests do not authorize live installation.
2. Read [assets/delegation.md](assets/delegation.md) for the routing policy. Inspect the four [agent templates](assets/agents/) when checking or changing role defaults. Existing role files are preserved by default, including customized Luna settings.
3. Run the commands below from this skill directory with **Python 3.11+** (standard library only). Resolve resources relative to this skill, never a source checkout or a hardcoded username. On macOS, `python3` may still be 3.9; check `python3 --version` and use an installed `python3.12` (or another 3.11+ interpreter) for every command below when necessary. Do not install a runtime automatically. Omit `--codex-home` to use `CODEX_HOME`, or `~/.codex` when unset.

   ```bash
   python3 scripts/manage.py show --codex-home /path/to/codex-home
   python3 scripts/manage.py check --codex-home /path/to/codex-home
   ```

4. For installation or enablement, automatically run `show`, review its output for scope conflicts, run `apply`, then `check`. Do not stop after presenting commands or a proposed plan. A failed pre-install `check` due only to missing configuration is expected and is a reason to install, not a blocker.

   ```bash
   python3 scripts/manage.py apply --codex-home /path/to/codex-home
   python3 scripts/manage.py check --codex-home /path/to/codex-home
   ```

   `apply` installs missing agents and adds or updates its marked AGENTS.md section. It preserves all other global instructions. An identical older unmarked `## 子 Agent 委派` section can be adopted. A differing unmarked section is a conflict, not permission to append duplicate routing rules.

   The automatic setup must produce these files under the resolved Codex home (by default `~/.codex`):

   - `agents/luna-subagent.toml`, `agents/terra-subagent.toml`, `agents/sol-subagent.toml`, and `agents/astra-subagent.toml`: create missing files from the bundled templates; retain valid existing customizations.
   - `AGENTS.md`: create if absent; otherwise write only the managed delegation section and preserve the rest. Back up an existing file before changing it.

   Use the same resolved `--codex-home` for preview, apply, and verification. Report a parse error, conflicting unmarked policy, or write failure with its evidence; do not treat it as a request to replace unrelated content. Ordinary runtime use does not repeat this setup.

5. Use `show --replace-existing` to review replacements, then `apply --replace-existing` only when replacing existing role defaults or conflicting legacy policy is within the user's request. This flag applies to all four role templates and may replace a conflicting legacy policy; inspect every proposed change and report the resolved destination. If the user requests only role changes and the preview also changes their policy, preserve that policy with a scoped edit instead of applying the combined plan. The script backs up modified existing files and reports backup paths. Do not reset customized Luna merely to make the bundle match.
6. Report created, retained, or changed files, actual configured model/effort, backups, and validation limits. If an `AGENTS.override.md` exists, inspect its effect before claiming the global policy is active. Start a new Codex task/session to load configuration; if roles remain absent, restart the app and inspect the current tools. Do not claim a successful launch based on valid TOML alone.

## Runtime use

The installed policy is the single routing reference. Select an exposed role via `agent_type`; let its TOML supply model and effort. Do not duplicate model overrides or assume conversation inheritance parameters are portable across tool versions.

Use the current runtime interface as the authority for supported roles and parameters. When the intended role is unavailable, report the limitation and use a suitable available alternative under current constraints; do not silently rewrite configs. Distinguish requested settings from confirmed runtime metadata.

The default Luna template retains `max` effort and fast-mode settings from the existing Luna setup. This is a preserved preference, not an efficiency benchmark. Terra uses `medium`; Sol and Astra use `high`. Availability, model quality, and service-tier support must be checked against the destination runtime when needed.

## Ownership and coexistence

- This bundle owns four-role installation and global routing. It does not change `config.toml`, install dependencies, or create tasks just to demonstrate delegation.
- The separate `luna-subagent` skill remains responsible for Luna-only management. Its template is independent; coordinate an intentional Luna default change across bundles rather than repeatedly overwriting one from the other.
- Role instructions define scoped work and results. AGENTS.md defines when the parent delegates and how it verifies the result. Keep those responsibilities separate.
- Only the marked routing section is managed on subsequent applies. User edits within that section are shown by `show` and replaced by an authorized apply; keep unrelated preferences outside it.

## Verification

Execute [scripts/test_manage.py](scripts/test_manage.py) against temporary homes; never use the live configuration as a destructive test fixture:

```bash
python3 scripts/test_manage.py
```

For repository maintenance also run from the repository root:

```bash
python3 scripts/validate-skills.py
```

Require successful parsing and checks, preserved unrelated instructions and existing custom agents, idempotent reapplication, backups for replacement, and failure without partial writes for malformed input. Structural checks do not establish account access, actual runtime model, or proactive delegation behavior. Report those as untested unless there is separate runtime evidence.

Official configuration reference: [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) and [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md). Consult current documentation when runtime behavior differs.
