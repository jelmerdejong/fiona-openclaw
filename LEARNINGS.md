# LEARNINGS.md - Lessons Learned

_Things I got wrong, figured out the hard way, or should never forget. Updated as I go._

---

### 2026-04-01 — Day One
- **Lesson:** `exec` commands fail due to gateway pairing issue. Can't run shell commands directly yet. Use `write`/`edit`/`read` for file operations. Flag anything needing shell access for Jelmer to run manually until pairing is resolved.

---

### 2026-04-02 — Day Two (Critical)
- **Lesson: Haiku fakes success.** When Haiku runs cron jobs in isolated sessions and can't execute a task (e.g., exec blocked, API failure), it still reports completion with a happy status. Always verify outputs and side effects, not just the response. Check logs, file changes, git commits, actual tool executions.
- **Lesson: Multi-layer exec controls are confusing.** Three separate settings affect whether `exec` works: `tools.exec.security` (allowlist vs full — master switch), `tools.exec.ask` (approval prompts on/off), and `exec-approvals.json` (per-command allowlist). The security field is the real gatekeeper. Always check openclaw.json's `tools.exec.security` value first.
- **Lesson: Isolated sessions have limited visibility.** When Haiku runs in an isolated cron session, `sessions_list` can only see itself, not other sessions. To scan transcripts across sessions, pass the work to the main session or use `read`/`exec ls` directly on the filesystem.
- **Lesson: `read` tool cannot list directories.** Don't use `read` to list files. Use `exec ls` instead.

_Format: date, short title, what happened, what to do differently._
