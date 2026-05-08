import os
import requests
from dataclasses import dataclass
from typing import Optional

GITHUB_API = "https://api.github.com"


@dataclass
class PullRequest:
    number: int
    title: str
    description: str
    author: str
    base_branch: str
    head_branch: str
    diff: str
    files_changed: list[dict]


class GitHubClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN not set. Export it or pass directly.")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def get_pull_request(self, owner: str, repo: str, pr_number: int) -> PullRequest:
        """Fetch PR metadata."""
        url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        data = resp.json()

        diff = self._get_diff(owner, repo, pr_number)
        files = self._get_files(owner, repo, pr_number)

        return PullRequest(
            number=data["number"],
            title=data["title"],
            description=data.get("body") or "(no description)",
            author=data["user"]["login"],
            base_branch=data["base"]["ref"],
            head_branch=data["head"]["ref"],
            diff=diff,
            files_changed=files,
        )

    def _get_diff(self, owner: str, repo: str, pr_number: int) -> str:
        """Fetch raw unified diff of the PR."""
        url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}"
        headers = {**self.headers, "Accept": "application/vnd.github.v3.diff"}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.text

    def _get_files(self, owner: str, repo: str, pr_number: int) -> list[dict]:
        """Fetch list of changed files with stats."""
        url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}/files"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        return [
            {
                "filename": f["filename"],
                "status": f["status"],
                "additions": f["additions"],
                "deletions": f["deletions"],
                "patch": f.get("patch", ""),
            }
            for f in resp.json()
        ]

    def post_review_comment(self, owner: str, repo: str, pr_number: int, body: str):
        """Post the review as a PR comment."""
        url = f"{GITHUB_API}/repos/{owner}/{repo}/issues/{pr_number}/comments"
        resp = requests.post(url, headers=self.headers, json={"body": body})
        resp.raise_for_status()
        print(f"Review posted to PR #{pr_number}")
        return resp.json()