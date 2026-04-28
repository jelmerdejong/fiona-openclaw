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

### 2026-04-03 — Day Three
- **Lesson: Telegram long-polling issue with forum/topic groups.** Created "Fiona HQ" group with Topics enabled. Bot can send messages successfully but long-polling never picks up incoming messages. IPv6 timeout on startup (`ETIMEDOUT,ENETUNREACH`) may be related. Investigation needed: check OpenClaw docs for forum/topic group support, or file a bug with full logs. Don't assume it's a config issue — may be a platform limitation.

### 2026-04-04–05 — Days Four & Five
- **Lesson: Obsidian vault enrichment at scale works.** Imported 451 books from Goodreads export, added fiction/non-fiction classification, 3–7 topic tags each, summaries, and internal wiki-links. Generated 331 author pages, 37 series pages, 34 topic pages automatically. Navigation and discoverability improve dramatically with structured metadata. This pattern scales well for other knowledge domains (wardrobe, places).

_Format: date, short title, what happened, what to do differently._

## Google Maps Short Links (April 28, 2026)
- `maps.app.goo.gl` short links don't work with `web_fetch` (Google Maps is JS-rendered)
- **Fix:** Use `curl -sIL` to follow redirects and extract the location/address from the `Location:` header
- The redirect URL contains the full address as a `q=` parameter
- Example: `curl -sIL "https://maps.app.goo.gl/XXXX" | grep -i location` → extract address from URL
