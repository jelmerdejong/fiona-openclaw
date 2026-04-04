# MEMORY.md - Curated Long-term Memory

_Last updated: 2026-04-04_

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

## Known Issues

- ~~Session harvester broken~~ — **Fixed April 2.** Harvester rewritten to use `exec ls` + `read`. Exec policy fixed: `tools.exec.security: "full"` + `ask: "off"`.
- ~~MEMORY.md was empty until manual harvest~~ — **Fixed April 2.** Day 1 transcript manually rescued.

## Exec Policy (Important)

Three layers control exec, all must be permissive:
1. **`tools.exec.security`** — master switch (`"full"` = no allowlist). Protected path, CLI only.
2. **`tools.exec.ask`** — approval prompts (`"off"` = never ask)
3. **`exec-approvals.json`** — per-command grants (currently empty, security=full bypasses it)
