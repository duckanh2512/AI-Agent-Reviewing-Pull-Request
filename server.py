#!/usr/bin/env python3
"""
Code Review Agent — CLI
Usage:
  python server.py <owner> <repo> <pr_number> [--post]

Examples:
  python server.py microsoft vscode 12345
  python server.py microsoft vscode 12345 --post
"""

import sys
import argparse
from github_client import GitHubClient
from agent import review_pr


def parse_args():
    parser = argparse.ArgumentParser(
        description="AI-powered GitHub PR reviewer"
    )
    parser.add_argument("owner", help="GitHub repo owner (e.g. microsoft)")
    parser.add_argument("repo", help="GitHub repo name (e.g. vscode)")
    parser.add_argument("pr_number", type=int, help="Pull Request number")
    parser.add_argument(
        "--post",
        action="store_true",
        help="Post the review as a comment on the PR",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print("\n" + "=" * 60)
    print(f"  CODE REVIEW AGENT")
    print(f"  Repo : {args.owner}/{args.repo}")
    print(f"  PR   : #{args.pr_number}")
    print("=" * 60 + "\n")

    # Fetch PR
    print("📡 Fetching PR from GitHub...")
    gh = GitHubClient()
    pr = gh.get_pull_request(args.owner, args.repo, args.pr_number)

    print(f"📋 PR #{pr.number}: {pr.title}")
    print(f"   by @{pr.author} | {len(pr.files_changed)} file(s) changed\n")

    # Run agent
    review = review_pr(pr)

    # Print to terminal
    print("\n" + "=" * 60)
    print("REVIEW RESULT")
    print("=" * 60)
    print(review)

    # Optionally post to GitHub
    if args.post:
        print("\n Posting review to GitHub...")
        header = f"## AI Code Review — PR #{pr.number}\n\n"
        gh.post_review_comment(args.owner, args.repo, args.pr_number, header + review)

    print("\n Done!\n")


if __name__ == "__main__":
    main()
