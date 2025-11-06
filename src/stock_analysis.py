"""Utilities for combining sentiment data with historical prices."""
from __future__ import annotations

from datetime import datetime
from typing import Iterable, Optional

import pandas as pd
import yfinance as yf

from .sentiment import ScoredTweet


def aggregate_daily_sentiment(tweets: Iterable[ScoredTweet]) -> pd.DataFrame:
    """Aggregate scored tweets into a per-day sentiment DataFrame."""

    rows = [
        {
            "date": scored.tweet.date.date(),
            "compound": scored.compound,
        }
        for scored in tweets
    ]
    if not rows:
        return pd.DataFrame(columns=["date", "compound_mean", "count"])

    df = pd.DataFrame(rows)
    grouped = df.groupby("date").agg(compound_mean=("compound", "mean"), count=("compound", "size"))
    return grouped.reset_index()


def fetch_price_history(
    ticker: str,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
) -> pd.DataFrame:
    """Fetch historical OHLC data for ``ticker`` using ``yfinance``."""

    price_df = yf.download(ticker, start=start, end=end, progress=False)
    if price_df.empty:
        raise ValueError(f"No price data returned for ticker '{ticker}'.")
    price_df.index = price_df.index.tz_localize(None)
    return price_df


def compute_sentiment_return_frame(
    sentiment_df: pd.DataFrame, price_df: pd.DataFrame
) -> pd.DataFrame:
    """Merge daily sentiment with close-to-close returns."""

    if sentiment_df.empty:
        raise ValueError("No sentiment data available to merge with prices.")

    closes = price_df[["Close"]].copy()
    closes["return_next"] = closes["Close"].pct_change().shift(-1)
    closes = closes.reset_index()
    if "Date" in closes:
        closes["date"] = closes["Date"].dt.date
        closes = closes.drop(columns=["Date"])
    else:
        closes = closes.rename(columns={"index": "date"})
        closes["date"] = closes["date"].dt.date

    merged = pd.merge(sentiment_df, closes, on="date", how="left")
    merged = merged.dropna(subset=["return_next"])
    return merged


def predict_direction(merged_df: pd.DataFrame) -> str:
    """Predict the next price move using a simple sentiment heuristic."""

    latest = merged_df.sort_values("date").iloc[-1]
    recent_sentiment = latest["compound_mean"]

    positive_returns = merged_df.loc[merged_df["compound_mean"] > 0, "return_next"]
    negative_returns = merged_df.loc[merged_df["compound_mean"] <= 0, "return_next"]

    positive_mean = positive_returns.mean() if not positive_returns.empty else 0.0
    negative_mean = negative_returns.mean() if not negative_returns.empty else 0.0

    expected_return = positive_mean if recent_sentiment > 0 else negative_mean
    direction = "bullish" if expected_return >= 0 else "bearish"
    return direction
