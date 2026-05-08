import os
import anthropic
from github_client import PullRequest

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert code reviewer. When given a GitHub Pull Request diff, you must provide a structured review covering:

1. **SUMMARY** — What does this PR do? (2-3 sentences)
2. **ISSUES** — List bugs, security risks, or logic errors found (if any)
3. **SUGGESTIONS** — Style, performance, or readability improvements
4. **PRAISE** — What was done well (always find something positive)
5. **VERDICT** — One of: APPROVE | REQUEST CHANGES | COMMENT ONLY

Be concise, constructive, and educational — the author may be a student or junior developer.
Format your response in clean Markdown."""


def build_prompt(pr: PullRequest) -> str:
    files_summary = "\n".join(
        f"- `{f['filename']}` ({f['status']}) +{f['additions']} -{f['deletions']}"
        for f in pr.files_changed
    )

    # Truncate diff if too large (keep under ~8000 chars)
    diff = pr.diff
    if len(diff) > 8000:
        diff = diff[:8000] + "\n\n... [diff truncated for length]"

    return f"""## Pull Request: #{pr.number} — {pr.title}
**Author:** {pr.author}
**Branch:** `{pr.head_branch}` → `{pr.base_branch}`

**Description:**
{pr.description}

**Files Changed:**
{files_summary}

**Diff:**
```diff
{diff}
```

Please review this PR thoroughly."""


def review_pr(pr: PullRequest) -> str:
    """Run a two-step agent review on a PR."""

    print("Step 1: Initial analysis...")
    messages = [{"role": "user", "content": build_prompt(pr)}]

    first_pass = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=messages,
    )
    initial_review = first_pass.content[0].text

    print("Step 2: Deep-dive on issues found...")
    messages.append({"role": "assistant", "content": initial_review})
    messages.append({
        "role": "user",
        "content": (
            "Now focus specifically on any ISSUES you found. "
            "For each issue, provide: the exact line or code snippet, "
            "why it's a problem, and a corrected version. "
            "If no issues were found, confirm the code is clean."
        ),
    })

    second_pass = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=messages,
    )
    deep_dive = second_pass.content[0].text

    total_tokens = (
        first_pass.usage.input_tokens
        + first_pass.usage.output_tokens
        + second_pass.usage.input_tokens
        + second_pass.usage.output_tokens
    )

    final_review = f"{initial_review}\n\n---\n\n### 🔬 Deep Dive on Issues\n\n{deep_dive}"
    print(f"Review complete. Tokens used: {total_tokens}")
    return final_review
