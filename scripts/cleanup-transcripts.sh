#!/bin/bash
# Weekly transcript cleanup — compress old, delete ancient
# Run via system cron (e.g. Sunday midnight)

# Compress transcripts older than 30 days
find ~/.openclaw/agents/*/sessions/ -name "*.jsonl" -mtime +30 -exec gzip {} \;

# Delete compressed transcripts older than 365 days
find ~/.openclaw/agents/*/sessions/ -name "*.jsonl.gz" -mtime +365 -delete
