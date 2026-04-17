# MEMORY.md - Curated Long-term Memory

_Last updated: 2026-04-12 (session harvester update)_

## Setup & Infrastructure (2026-04-01)

- **Fiona first boot:** April 1, 2026. Bootstrap complete, all identity files created.
- **Model providers:** Anthropic (Opus default) + OpenAI (GPT-5.4). Opus is default for everything.
- **Model routing plan:** Opus → Sonnet → Haiku fallback. Codex for coding. Extended thinking for research/decisions. *Config partially applied — needs verification.*
- **Config issue found:** `openclaw.json` had `model.primary` set to `openai/gpt-5.4` instead of Opus. May still need fixing.
- **Memory search:** Was disabled in config (`memorySearch.enabled: false`). Needs enabling + embedding provider setup.
- **Web search:** Switched from DuckDuckGo to Brave Search (required gateway restart).
- **Git backup:** Private repo at `github.com/jelmerdejong/fiona-openclaw`. PAT auth configured. Auto-push every 6h.
- **Gateway pairing:** Was blocking exec — fixed by approving pending device.

## Automation Stack

| Job | Schedule | Purpose |
|---|---|---|
| Heartbeat | ~10 min (Haiku) | Time-sensitive alerts only |
| Session harvester | Every 2h, 08–22 Amsterdam (Haiku) | Extract facts from transcripts |
| Git backup | Every 6h (Haiku) | Push workspace to GitHub |
| Daily maintenance | 23:00 Amsterdam (Haiku) | Summarize, curate, trim, learn |
| Tax filing reminder | 2026-04-13 09:00 Amsterdam (cron) | STP (personal tax), HLB (corporate filings) | **ISSUE: Failed to deliver**

## Known Issues

- ~~Session harvester broken~~ — **Fixed April 2.** Harvester rewritten to use `exec ls` + `read`. Exec policy fixed: `tools.exec.security: "full"` + `ask: "off"`.
- **Cron reminder delivery failing (April 13)** — Tax filing reminder set for 09:00 Amsterdam but did not deliver to Telegram. Job `f3a0e4a1-ca52-460f-b027-7751620e69ff` created successfully but message never sent. May indicate broader Telegram integration issue.
- ~~MEMORY.md was empty until manual harvest~~ — **Fixed April 2.** Day 1 transcript manually rescued.

## Exec Policy (Important)

Three layers control exec, all must be permissive:
1. **`tools.exec.security`** — master switch (`"full"` = no allowlist). Protected path, CLI only.
2. **`tools.exec.ask`** — approval prompts (`"off"` = never ask)
3. **`exec-approvals.json`** — per-command grants (currently empty, security=full bypasses it)

## Telegram Integration (Active)

- **Group:** "Fiona HQ" (chat_id: -1003856841664) with Topics enabled
- **Topics:** General (id:1), Library 📚 (id:3), Wardrobe 👔 (id:11), Places 📍 (id:13)
- **Status:** Bot can send messages to group, but **NOT receiving messages**
- **Root cause unresolved (April 3):** Long-polling never picks up group messages. IPv6 timeout on startup may be related. Multiple restarts did not fix. May need OpenClaw docs review or bug report.
- **Note (April 13):** Cron announcements to Telegram also failing. Broader delivery issue suspected.
- **TODO:** Debug Telegram forum/topic group support; check per-topic system prompts configuration; debug cron-to-telegram delivery

## X.com (Twitter) Integration (Active — April 17)

- **Status:** ✅ Working! Official X API pay-per-use connected.
- **Skill:** `twitter-x-api` installed at `skills/twitter-x-api/`
- **Auth:** Bearer Token stored in `~/.openclaw/.env`, `~/.config/twitter/credentials.json`, and `~/.bashrc`
- **Capabilities:** Read tweets, user profiles, search, show tweet details, analytics
- **Usage:** `python3 skills/twitter-x-api/scripts/tweet.py <command>` (needs TWITTER_BEARER_TOKEN env)
- **Cost:** $0.005/read, $0.01/profile lookup (pay-per-use, no monthly fee)
- **Note:** Search min count is 10 (API limitation). Write operations need additional OAuth keys (not configured — read-only for now).

## Obsidian Vaults (Initialized April 3)

- **Library vault:** 451 books from Goodreads export. Enhanced with fiction/non-fiction type, 3-7 topic tags, summaries, wiki-links. Created 331 author pages, 37 series pages, 34 topic pages. All committed + pushed.
- **Wardrobe vault:** (Activated April 6) Structure: Items, Outfits, Style, Templates, Stores. Refined heritage casual style (quality, texture, brown over black). 16 items documented: 4 owned (Sugar Cane jeans, Samurai jeans, Real McCoy's M-1943, Faherty sweater), 12 to-buy (focus: NN07 Aden chinos, Proper Cloth OCBD, RRL Chambray, orSlow 107 jeans, Red Wing Weekender chukka). 8 stores across Amsterdam, NYC, London, Stockholm, Zurich with location details and brand notes. Driven by Derek Guy (@dieworkwear) recommendations and heritage menswear exploration.
- **Places vault:** Created but empty — awaiting design discussion
- **GitHub PAT:** Updated to cover all 3 vault repos
