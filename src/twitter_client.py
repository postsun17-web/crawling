"""Utilities for fetching tweets from X (Twitter) via snscrape."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

try:
    from snscrape.modules import twitter as sntwitter
except ImportError as exc:  # pragma: no cover - Import error surfaced to caller
    raise RuntimeError(
        "snscrape is required to crawl X posts. Install it via `pip install snscrape`."
    ) from exc


@dataclass
class Tweet:
    """Lightweight container for tweet data."""

    id: int
    url: str
    content: str
    date: datetime
    username: str


def fetch_tweets(
    query: str,
    *,
    limit: int = 200,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
) -> List[Tweet]:
    """Fetch tweets matching ``query`` using ``snscrape``.

    Parameters
    ----------
    query:
        Keyword(s) used for searching. This is passed directly to the X search
        endpoint, therefore advanced syntax (e.g. ``OR``) can be used.
    limit:
        Maximum number of tweets to retrieve.
    since / until:
        Optional datetime boundaries (inclusive) for the tweet ``date``.

    Returns
    -------
    List[Tweet]
        A list of dataclass instances with tweet metadata.
    """

    search_terms = [query]
    if since is not None:
        search_terms.append(f"since:{since.date().isoformat()}")
    if until is not None:
        search_terms.append(f"until:{until.date().isoformat()}")

    scraper_query = " ".join(search_terms)

    tweets: List[Tweet] = []
    for idx, tweet in enumerate(sntwitter.TwitterSearchScraper(scraper_query).get_items()):
        tweets.append(
            Tweet(
                id=int(tweet.id),
                url=tweet.url,
                content=tweet.content,
                date=tweet.date.replace(tzinfo=None),
                username=tweet.user.username,
            )
        )
        if idx + 1 >= limit:
            break
    return tweets
