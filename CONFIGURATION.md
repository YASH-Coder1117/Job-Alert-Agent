# Configuration Guide

This document outlines all configurable aspects of the Job Alert Agent.

## 1. Environment Variables (`config/.env`)

You must create a `.env` file in the `config/` directory. Use `config/.env.example` as a template.

### PostgreSQL Credentials
*Required for storing jobs and vector embeddings.*
- `DB_HOST`: Database host IP/URL (e.g., `127.0.0.1` or AWS RDS endpoint).
- `DB_PORT`: Database port (Default: `5432`).
- `DB_NAME`: Database name.
- `DB_USER`: Database user.
- `DB_PASSWORD`: Database password.

### MegaLLM Configuration
*Required for the final agentic relevancy evaluation.*
- `MEGALLM_API_KEY`: Your MegaLLM API Key. Get it from the [MegaLLM Dashboard](https://ai.megallm.io/).
- `MEGALLM_BASE_URL`: Must be `https://ai.megallm.io/v1`.
- `LLM_MODEL`: The MegaLLM model to use. Default is `gpt-5`.

### Email Settings
*Required for receiving alerts.*
- `EMAIL_FROM`: The sender email (e.g., your Gmail).
- `EMAIL_TO`: Where to send alerts.
- `EMAIL_PASSWORD`: Your App Password (not your normal password). For Gmail, generate this in "Security > App Passwords".

## 2. User Preferences (`config/config.yaml`)

This file determines what the agent searches for.

```yaml
preferences:
  role: "AI Engineer"           # Base job title to search
  location: "New York"          # Base location
  experience: "fresher"         # Used in LLM prompt
  skills:                       # Used in LLM prompt
    - python
    - machine learning
  keywords:
    include: ["AI", "Python"]   # Jobs MUST contain at least one of these
    exclude: ["Senior", "Lead"] # Jobs with these words will be dropped instantly
```

## Security Best Practices
- **NEVER** commit your `.env` file to version control. It is already included in the `.gitignore`.
- Keep your `config.yaml` free of sensitive data; it is safe to commit.
