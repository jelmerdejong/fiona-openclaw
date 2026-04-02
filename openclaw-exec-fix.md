# Fixing "exec denied: allowlist miss" in OpenClaw

If your agent can't run shell commands and you're seeing `exec denied: allowlist miss`, here's the fix.

## The Problem

OpenClaw has **three separate layers** controlling exec permissions. All three need to be permissive, or commands get blocked:

| Layer | Config Path | What it does |
|---|---|---|
| **Security mode** | `tools.exec.security` | Master switch. Defaults to `"allowlist"` which blocks any command not explicitly whitelisted. |
| **Ask mode** | `tools.exec.ask` | Controls whether allowed commands need human approval before running. |
| **Approvals file** | `~/.openclaw/exec-approvals.json` | Per-command allowlist entries (only matters when security = allowlist). |

The `tools.profile` setting (`minimal`, `coding`, `messaging`, `full`) also sets a baseline allowlist. Even removing the profile doesn't clear the security mode — it keeps defaulting to `"allowlist"`.

## The Fix

```bash
# 1. Set security to "full" (disables the allowlist entirely)
openclaw config set tools.exec.security full

# 2. Set ask to "off" (no approval prompts)
openclaw config set tools.exec.ask off

# 3. Restart the gateway to apply
openclaw gateway restart
```

That's it. Two commands + restart.

## Common Traps

- **`ask: "off"` alone doesn't work** — it only skips approval prompts. The allowlist still blocks unlisted commands.
- **Removing `tools.profile` doesn't help** — the security mode persists independently.
- **The approvals file (`exec-approvals.json`) is a red herring** — setting `defaults.security: "full"` there doesn't override the config-level security mode.
- **`tools.exec.security` is a protected config path** — you must set it via CLI (`openclaw config set`), not through the agent's `gateway config.patch` tool.
- **Sessions cache the policy at creation time** — after changing config, you need a gateway restart AND a new session (`/reset` or `/new`). Existing sessions may keep the old policy.

## Verify It Works

After restart, in a fresh session, the agent should be able to run:
```
echo "hello world"
git status
cat /etc/hostname
```

If you still see "allowlist miss", do `/reset` to start a fresh session that picks up the new policy.
