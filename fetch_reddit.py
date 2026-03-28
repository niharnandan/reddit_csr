#!/usr/bin/env python3
"""Fetch recent posts from r/ChaseSapphire and output them as JSON."""

import json
import sys
import time
from datetime import datetime, timezone

import requests

SUBREDDIT = "ChaseSapphire"
URL = f"https://www.reddit.com/r/{SUBREDDIT}/new.json?limit=50"
HEADERS = {"User-Agent": "reddit-csr-digest/1.0 (daily deal digest)"}
LOOKBACK_HOURS = 24


def fetch_posts():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
    except requests.RequestException as e:
        print(f"ERROR: Request failed: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Reddit response: HTTP {response.status_code}", file=sys.stderr)

    if response.status_code == 429:
        print("ERROR: Rate limited by Reddit (HTTP 429)", file=sys.stderr)
        sys.exit(1)

    if response.status_code != 200:
        print(f"ERROR: Unexpected status code: {response.status_code}", file=sys.stderr)
        print(f"Response body: {response.text[:500]}", file=sys.stderr)
        sys.exit(1)

    data = response.json()
    posts = data.get("data", {}).get("children", [])

    cutoff = time.time() - LOOKBACK_HOURS * 3600
    results = []

    for post in posts:
        p = post.get("data", {})
        created = p.get("created_utc", 0)
        if created < cutoff:
            continue

        results.append({
            "title": p.get("title", ""),
            "body": p.get("selftext", ""),
            "score": p.get("score", 0),
            "num_comments": p.get("num_comments", 0),
            "url": f"https://www.reddit.com{p.get('permalink', '')}",
            "created_utc": created,
            "created_human": datetime.fromtimestamp(created, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        })

    print(f"Fetched {len(results)} posts from the last {LOOKBACK_HOURS}h", file=sys.stderr)
    print(json.dumps({"posts": results, "count": len(results), "subreddit": SUBREDDIT}))


if __name__ == "__main__":
    fetch_posts()
