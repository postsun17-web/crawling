# crawling

Command line utility to crawl X (Twitter) posts for a given stock, run sentiment analysis, and use a heuristic to predict the short-term trend of the stock price.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```
python -m src.cli TICKER "QUERY" --limit 200 --days 7
```

- `TICKER`: Stock ticker symbol (e.g., `AAPL`).
- `QUERY`: Search query passed to X, e.g., the ticker or full company name.
- `--limit`: Maximum number of posts to fetch (default: 200).
- `--days`: Number of most recent days to analyze (default: 7). Use `--since`/`--until` to override the date range.

The script prints the aggregated daily sentiment, merges it with the corresponding price returns, and outputs a bullish/bearish prediction based on the most recent sentiment regime.

> **Note:** This repository provides analysis utilities only. To run the crawler successfully you must have network access and valid certificates for accessing X and Yahoo Finance from your environment.
