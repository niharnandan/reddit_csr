# Reddit Chase Sapphire Deal Digest

This repo powers a daily email digest of deal-related posts from r/ChaseSapphire, sent at 6:00 PM PT via a Claude Code cloud scheduled trigger.

## How It Works

1. `fetch_reddit.py` hits the Reddit JSON API and returns the last 24 hours of posts from r/ChaseSapphire
2. Claude analyzes the posts, identifies deals/offers/bonuses/promotions, and formats a summary
3. `send_email.py` sends the formatted summary as an HTML email via Gmail SMTP

## Scripts

### `fetch_reddit.py`
Fetches recent posts. Outputs JSON to stdout:
```json
{"posts": [...], "count": N, "subreddit": "ChaseSapphire"}
```
Each post: `title`, `body`, `score`, `num_comments`, `url`, `created_utc`, `created_human`

### `send_email.py`
Sends the digest email. Takes one argument: the HTML body content.
```bash
python send_email.py "<div class='deal'>...</div>"
```

## Environment Variables

| Variable | Description |
|---|---|
| `GMAIL_USER` | Gmail address to send from |
| `GMAIL_APP_PASSWORD` | Gmail App Password (not your regular password) |
| `EMAIL_TO` | Email address to send the digest to |

## Gmail App Password Setup

1. Enable 2-Factor Authentication at https://myaccount.google.com/security
2. Generate an App Password at https://myaccount.google.com/apppasswords
3. Use "Mail" as the app type
4. Store the 16-character password as `GMAIL_APP_PASSWORD`

## Cloud Trigger Setup

Set up via `/schedule` in Claude Code:

- **Schedule:** `0 1 * * *` (1:00 AM UTC = 6:00 PM PT)
- **Setup script:** `pip install -r requirements.txt`
- **Prompt:**
  ```
  Run `python fetch_reddit.py` to get today's r/ChaseSapphire posts.
  Analyze the output and identify any posts about deals, offers, bonuses,
  promotions, or point valuations. For each deal found, write a 1-2 sentence
  summary and include the post URL as a link. Format each deal as an HTML
  <div class="deal"> block containing the summary and a link.
  Then run `python send_email.py "<html_body>"` passing all deal divs as the
  argument. If no deals were found, pass a single
  <p class="no-deals">No notable deals today.</p> as the argument.
  ```

## Local Testing

```bash
# Install deps
pip install -r requirements.txt

# Test Reddit fetch
python fetch_reddit.py

# Test email (set env vars first)
export GMAIL_USER="you@gmail.com"
export GMAIL_APP_PASSWORD="your-app-password"
export EMAIL_TO="you@gmail.com"
python send_email.py "<p class='no-deals'>Test email — no deals today.</p>"
```
