#!/usr/bin/env python3
"""
Fetch recent X (Twitter) posts for fixed motor finance search queries via Apify.
Usage: python3 fetch_x.py
Requires: APIFY_API_KEY environment variable set by caller (Claude reads from CLAUDE.local.md).
Prints a plain text summary of top posts to stdout.
"""
import os
import sys
from apify_client import ApifyClient

SEARCH_QUERIES = [
    "motor finance UK",
    "car finance UK",
    "FCA motor finance",
    "used car market UK",
    "PCP finance UK",
]

ACTOR_ID = "apidojo/tweet-scraper"
MAX_ITEMS_PER_QUERY = 15


def fetch_posts(api_key: str) -> list[dict]:
    client = ApifyClient(api_key)
    all_posts = []
    seen_ids = set()

    for query in SEARCH_QUERIES:
        run_input = {
            "searchTerms": [query],
            "maxItems": MAX_ITEMS_PER_QUERY,
            "queryType": "Latest",
        }
        run = client.actor(ACTOR_ID).call(run_input=run_input)
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            post_id = item.get("id") or item.get("url", "")
            if post_id not in seen_ids:
                seen_ids.add(post_id)
                all_posts.append({
                    "query": query,
                    "text": item.get("text", ""),
                    "author": item.get("author", {}).get("userName", "unknown"),
                    "url": item.get("url", ""),
                    "created_at": item.get("createdAt", ""),
                })

    return all_posts


def format_output(posts: list[dict]) -> str:
    lines = []
    current_query = None
    for post in posts:
        if post["query"] != current_query:
            current_query = post["query"]
            lines.append(f"\n=== Search: {current_query} ===\n")
        lines.append(f"@{post['author']} ({post['created_at'][:10]})")
        lines.append(post["text"])
        lines.append(f"URL: {post['url']}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    api_key = os.environ.get("APIFY_API_KEY")
    if not api_key:
        print("Error: APIFY_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)
    posts = fetch_posts(api_key)
    print(format_output(posts))
    print(f"\n[Total posts fetched: {len(posts)}]", file=sys.stderr)
