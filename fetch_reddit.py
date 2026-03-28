#!/usr/bin/env python3
"""Fetch recent posts from r/ChaseSapphire via Arctic Shift API and output them as JSON."""

import json
import sys
import time
from datetime import datetime, timezone

import requests

SUBREDDIT = "ChaseSapphire"
LOOKBACK_HOURS = 24


def fetch_posts():
    cutoff = int(time.time() - LOOKBACK_HOURS * 3600)
    url = f"https://arctic-shift.photon-reddit.com/api/posts/search?subreddit={SUBREDDIT}&limit=50&after={cutoff}"

    try:
        response = requests.get(url, timeout=15)
    except requests.RequestException as e:
        print(f"ERROR: Request failed: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Arctic Shift response: HTTP {response.status_code}", file=sys.stderr)

    if response.status_code != 200:
        print(f"ERROR: {response.text[:300]}", file=sys.stderr)
        sys.exit(1)

    posts = response.json().get("data", [])
    results = []

    for p in posts:
        created_utc = float(p.get("created_utc", 0))
        results.append({
            "title": p.get("title", ""),
            "body": p.get("selftext", "")[:500],
            "score": p.get("score", 0),
            "num_comments": p.get("num_comments", 0),
            "url": f"https://www.reddit.com{p.get('permalink', '')}",
            "created_utc": created_utc,
            "created_human": datetime.fromtimestamp(created_utc, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        })

    print(f"Fetched {len(results)} posts from the last {LOOKBACK_HOURS}h", file=sys.stderr)
    print(json.dumps({"posts": results, "count": len(results), "subreddit": SUBREDDIT}))


if __name__ == "__main__":
    fetch_posts()
