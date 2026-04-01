# HEARTBEAT.md — Time-Sensitive Checks Only

This runs on Haiku every ~10 minutes. Keep it cheap. No maintenance, no file ops, no verbose output.

## Rules
- **No output if nothing needs attention.** Reply HEARTBEAT_OK if all clear.
- **No maintenance tasks.** No summarizing, curating, trimming, or moving files. That's handled by cron.
- **Brief.** If something needs attention, say it in 1-3 sentences max.

## Checks

1. **Watchlist:** Check for changes to anything on the active watchlist. Report only if something changed.
2. **Unread messages/notifications:** If there are unread messages or notifications that need Jelmer's attention, surface them briefly.
