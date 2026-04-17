#!/bin/bash
# Weekly tweet pull for style research
# Pulls latest tweets from style inspirations and saves to wardrobe vault

VAULT="/home/fiona/.openclaw/workspace/vaults/wardrobe"
TWEET_SCRIPT="/home/fiona/.openclaw/workspace/skills/twitter-x-api/scripts/tweet.py"
DATE=$(date +%Y-%m-%d)

# Pull Derek Guy
echo "Pulling @dieworkwear tweets..."
python3 "$TWEET_SCRIPT" search "from:dieworkwear -is:retweet" --count 100 > "/tmp/dieworkwear_${DATE}.txt" 2>&1

# Pull Rach Corrine  
echo "Pulling @rachcorrine tweets..."
python3 "$TWEET_SCRIPT" search "from:rachcorrine -is:retweet" --count 100 > "/tmp/rachcorrine_${DATE}.txt" 2>&1

echo "Tweets pulled. Ready for processing."
