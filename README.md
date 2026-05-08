# Code Review Agent

An AI-powered GitHub Pull Request reviewer built with Claude API.

## Features
- Fetches PR diff and metadata from GitHub
- Two-step agent review: initial analysis → deep dive on issues
- Posts review directly as a PR comment (optional)
- Structured output: Summary, Issues, Suggestions, Praise, Verdict

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ANTHROPIC_API_KEY="sk-ant-..."
export GITHUB_TOKEN="ghp_..."
```

## Usage

```bash
# Review a PR (print to terminal)
python server.py <owner> <repo> <pr_number>

# Review and post as GitHub comment
python server.py <owner> <repo> <pr_number> --post
```

**Example:**
```bash
python server.py facebook react 12345
```

## Run Tests

```bash
python test_agent.py
```

## Project Structure

```
codereview/
├── agent.py          # Core review logic (Claude API)
├── github_client.py  # GitHub API wrapper
├── server.py         # CLI entrypoint
├── test_agent.py     # Unit tests
├── requirements.txt
└── README.md
```
