# Job Alert Agent

A production-ready, autonomous AI agent that scrapes job boards, evaluates matches using vector search and MegaLLM, and sends email notifications for highly relevant positions.

## Architecture

```text
[ Scraper ] ---> [ Keyword Filter ] ---> [ Deduplication ]
                                                |
                                                v
[ Email Notifier ] <--- [ MegaLLM Eval ] <--- [ pgvector DB ] <--- [ Embeddings Model ]
```

## Features
- **Automated Scraping**: Uses Playwright to extract job listings.
- **Smart Filtering**: Configurable keyword inclusion/exclusion.
- **Vector Search**: Leverages `sentence-transformers` and `pgvector` to find semantic matches.
- **Agentic Evaluation**: Uses MegaLLM (OpenAI compatible) to evaluate job relevance dynamically.
- **Email Alerts**: Sends automated SMTP notifications for matched jobs.

## Directory Structure
- `/agents`: High-level orchestrator and evaluator logic.
- `/tools`: System interactions (database, embeddings, scraper, email).
- `/utils`: Helper logic (deduplication, keyword filtering, logging).
- `/config`: Centralized configuration logic.
- `/tests`: Unit testing.
- `/examples`: Example execution scripts.

## Installation

1. Install PostgreSQL and the `pgvector` extension.
2. Install Python requirements:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```
3. Copy the environment variables:
   ```bash
   cp config/.env.example config/.env
   ```
4. Follow the setup instructions in `CONFIGURATION.md`.

## Usage
Run the pipeline:
```bash
python examples/run_agent.py
```
