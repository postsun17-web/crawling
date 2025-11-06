"""Command line interface for running the crawling + sentiment pipeline."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from typing import Optional

from .sentiment import TweetSentimentAnalyzer
from .stock_analysis import (
    aggregate_daily_sentiment,
    compute_sentiment_return_frame,
    fetch_price_history,
    predict_direction,
)
from .twitter_client import fetch_tweets


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Crawl X posts and predict stock trend")
    parser.add_argument("ticker", help="Ticker symbol used for the price lookup, e.g. AAPL")
    parser.add_argument(
        "query",
        help="Search query used on X (Twitter). You can pass the company name or ticker.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=200,
        help="Maximum number of posts to crawl (default: 200)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="How many recent days to analyze (default: 7)",
    )
    parser.add_argument(
        "--since",
        type=str,
        default=None,
        help="Override the start date (YYYY-MM-DD). Overrides --days.",
    )
    parser.add_argument(
        "--until",
        type=str,
        default=None,
        help="Override the end date (YYYY-MM-DD). Defaults to today.",
    )
    return parser.parse_args()


def _parse_date(value: Optional[str]) -> Optional[datetime]:
    if value is None:
        return None
    return datetime.strptime(value, "%Y-%m-%d")


def main() -> None:
    args = parse_args()

    end_date = _parse_date(args.until) or datetime.utcnow()
    start_date = _parse_date(args.since) or end_date - timedelta(days=args.days)

    tweets = fetch_tweets(args.query, limit=args.limit, since=start_date, until=end_date)
    if not tweets:
        raise SystemExit("No tweets were fetched. Try adjusting the query or timeframe.")

    sentiment_analyzer = TweetSentimentAnalyzer()
    scored_tweets = sentiment_analyzer.score(tweets)

    sentiment_df = aggregate_daily_sentiment(scored_tweets)
    print("Daily sentiment scores:\n", sentiment_df)

    price_df = fetch_price_history(args.ticker, start=start_date, end=end_date + timedelta(days=1))

    merged = compute_sentiment_return_frame(sentiment_df, price_df)
    if merged.empty:
        raise SystemExit("No overlapping price data to evaluate against.")

    direction = predict_direction(merged)
    print("\nMerged sentiment/return data:\n", merged)
    print(f"\nPredicted short-term trend for {args.ticker}: {direction.upper()}")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
