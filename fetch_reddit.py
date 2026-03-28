#!/usr/bin/env python3
"""Fetch recent posts from r/ChaseSapphire via Reddit OAuth API and output them as JSON."""

import json
import os
import sys
import time
from datetime import datetime, timezone

import praw

SUBREDDIT = "ChaseSapphire"
LOOKBACK_HOURS = 24


def fetch_posts():
    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent="reddit-csr-digest/1.0 (daily deal digest by /u/niharnandan)",
    )

    cutoff = time.time() - LOOKBACK_HOURS * 3600
    results = []

    for post in reddit.subreddit(SUBREDDIT).new(limit=50):
        if post.created_utc < cutoff:
            continue
        results.append({
            "title": post.title,
            "body": post.selftext[:500] if post.selftext else "",
            "score": post.score,
            "num_comments": post.num_comments,
            "url": f"https://www.reddit.com{post.permalink}",
            "created_utc": post.created_utc,
            "created_human": datetime.fromtimestamp(post.created_utc, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        })

    print(f"Fetched {len(results)} posts from the last {LOOKBACK_HOURS}h", file=sys.stderr)
    print(json.dumps({"posts": results, "count": len(results), "subreddit": SUBREDDIT}))


if __name__ == "__main__":
    fetch_posts()
