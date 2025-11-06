"""Sentiment analysis helpers for tweets."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from .twitter_client import Tweet


@dataclass
class ScoredTweet:
    tweet: Tweet
    compound: float
    positive: float
    negative: float
    neutral: float


class TweetSentimentAnalyzer:
    """Wrapper around ``vaderSentiment`` specialised for tweets."""

    def __init__(self) -> None:
        self._analyzer = SentimentIntensityAnalyzer()

    def score(self, tweets: Iterable[Tweet]) -> List[ScoredTweet]:
        """Return a list of :class:`ScoredTweet` with sentiment metrics."""

        results: List[ScoredTweet] = []
        for tweet in tweets:
            scores = self._analyzer.polarity_scores(tweet.content)
            results.append(
                ScoredTweet(
                    tweet=tweet,
                    compound=scores["compound"],
                    positive=scores["pos"],
                    negative=scores["neg"],
                    neutral=scores["neu"],
                )
            )
        return results
