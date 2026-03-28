#!/usr/bin/env python3
"""Read Reddit posts JSON from stdin, summarize deals using Claude API, output HTML to stdout."""

import json
import os
import sys

import anthropic


def main():
    posts_data = json.load(sys.stdin)
    posts = posts_data.get("posts", [])

    if not posts:
        print("<p class='no-deals'>No posts found in the last 24 hours.</p>")
        return

    posts_text = ""
    for i, p in enumerate(posts, 1):
        posts_text += f"\n[{i}] Title: {p['title']}\nURL: {p['url']}\nScore: {p['score']} | Comments: {p['num_comments']}\nBody: {p['body'][:500] if p['body'] else '(no body)'}\n"

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""You are reviewing posts from r/ChaseSapphire from the last 24 hours.
Identify posts that are about deals, offers, bonuses, promotions, limited-time offers, point valuations, or referral bonuses.
Ignore questions, complaints, general discussion, and trip reports.

For each deal post found, output a single HTML block in this exact format (nothing else):
<div class="deal"><a href="POST_URL">Short title</a> — One concise sentence describing the deal.</div>

If no deal posts are found, output exactly:
<p class="no-deals">No notable deals today.</p>

Posts to review:
{posts_text}

Output only the HTML blocks, no explanation."""
        }]
    )

    print(message.content[0].text.strip())


if __name__ == "__main__":
    main()
