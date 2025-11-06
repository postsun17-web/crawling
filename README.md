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

## Resolving "This branch has conflicts" when pushing

If GitHub blocks your push with a message such as **"This branch has conflicts that must be resolved"**, it means that the
branch on GitHub has commits that are not in your local branch. To resolve the conflict:

1. Fetch the latest commits from GitHub:
   ```bash
   git fetch origin
   ```
2. Merge (or rebase) the remote branch into your local branch. For example, if the remote default branch is `main`:
   ```bash
   git merge origin/main
   # or
   git rebase origin/main
   ```
3. Git will pause if there are conflicting files. Open each conflicted file, keep the desired changes, and remove the
   conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
4. Mark the conflicts as resolved and continue:
   ```bash
   git add <resolved-file(s)>
   git merge --continue   # or git rebase --continue
   ```
5. Once the merge/rebase finishes, push the updated branch:
   ```bash
   git push origin <branch-name>
   ```

If you prefer to recreate the branch from scratch, you can also reset to the remote state and re-apply your changes manually:
```bash
git fetch origin
git reset --hard origin/<branch-name>
# reapply changes
git push origin <branch-name>
```
