# TOOLS.md - Local Notes

## Jelmer's Devices
- **Mac** (primary computer)
- **iPhone** (primary phone)

## Apps & Services

### Calendar
- Calendar is the source of truth — everything lives there
- Jelmer and Naomi put appointments in each other's calendars
- Integration: TBD (need API/CLI access)

### Travel
- **Flighty** — iOS flight tracker
- **KLM** — primary airline, Platinum status, chasing Platinum for Life
- Frequent destinations: New York, London, Stockholm, Zurich

### Fitness
- **Garmin** — fitness/health tracking (integration TBD)
- **CrossFit** — Thursdays (local, Amstelveen/Amsterdam area)
- **Barry's** — when traveling (NYC, London, Stockholm, Zurich)

### Communication
- **Telegram** — primary Fiona channel (active)
  - **Group:** "Fiona HQ" (chat_id: -1003856841664, supergroup with Topics enabled)
  - **Topics:** General (id:1), Library 📚 (id:3), Wardrobe 👔 (id:11), Places 📍 (id:13)
  - **Status:** Group fully functional, all topics receive messages, bot is admin
  - **Config:** BotFather `can_read_all_group_messages: true`, openclaw config has `groupPolicy: "allowlist"` + `requireMention: false`
  - **Note:** Per-topic system prompts supported in OpenClaw config but not yet configured per topic
- **WhatsApp** — personal messaging (monitoring for lingering replies TBD)
- **iMessage** — also uses
- **Email** — TBD integration

### Notes & Knowledge
- **Obsidian** — current notes app
- Planning: shared tracking system for wardrobe, books, house tasks, etc.

### Reading
- No current tracker (wants to replace Goodreads)
- Fiona will serve as book tracker — read, reading, want-to-read

## Infrastructure
- Fiona runs on a **VPS** (no GUI, no direct device access)
- All integrations via CLI/API bridges
- Host: fiona-ubuntu-8gb-hel1-2 (Hetzner, Helsinki)

## TBD Integrations
- [x] Telegram setup (DONE: group + topics working, April 3)
- [ ] Telegram per-topic system prompts (Library, Wardrobe, Places)
- [ ] Email access
- [ ] Calendar API
- [ ] Garmin Connect API
- [ ] Obsidian sync or shared vault
- [ ] WhatsApp monitoring
