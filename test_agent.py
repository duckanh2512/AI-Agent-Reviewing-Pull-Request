"""
Tests for the Code Review Agent.
Run with: python test_agent.py
"""

import unittest
from unittest.mock import patch, MagicMock
from github_client import PullRequest
from agent import build_prompt, review_pr


MOCK_PR = PullRequest(
    number=42,
    title="Fix divide by zero bug in calculator",
    description="Added a check to prevent division by zero.",
    author="test-student",
    base_branch="main",
    head_branch="fix/divide-by-zero",
    diff="""--- a/calculator.py
+++ b/calculator.py
@@ -5,6 +5,8 @@ def divide(a, b):
+    if b == 0:
+        raise ValueError("Cannot divide by zero")
     return a / b""",
    files_changed=[
        {
            "filename": "calculator.py",
            "status": "modified",
            "additions": 2,
            "deletions": 0,
            "patch": "+    if b == 0:\n+        raise ValueError(...)",
        }
    ],
)


class TestBuildPrompt(unittest.TestCase):
    def test_prompt_contains_pr_title(self):
        prompt = build_prompt(MOCK_PR)
        self.assertIn("Fix divide by zero bug", prompt)

    def test_prompt_contains_author(self):
        prompt = build_prompt(MOCK_PR)
        self.assertIn("test-student", prompt)

    def test_prompt_contains_diff(self):
        prompt = build_prompt(MOCK_PR)
        self.assertIn("divide", prompt)

    def test_prompt_truncates_large_diff(self):
        big_pr = MOCK_PR
        big_pr_diff = "x" * 10000
        import dataclasses
        large_pr = dataclasses.replace(MOCK_PR, diff=big_pr_diff)
        prompt = build_prompt(large_pr)
        self.assertIn("truncated", prompt)


class TestReviewAgent(unittest.TestCase):
    @patch("agent.client")
    def test_review_returns_string(self, mock_client):
        # Mock two API calls
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="## SUMMARY\nLooks good!")]
        mock_response.usage.input_tokens = 100
        mock_response.usage.output_tokens = 50
        mock_client.messages.create.return_value = mock_response

        result = review_pr(MOCK_PR)
        self.assertIsInstance(result, str)
        self.assertIn("SUMMARY", result)

    @patch("agent.client")
    def test_review_calls_api_twice(self, mock_client):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Review text")]
        mock_response.usage.input_tokens = 100
        mock_response.usage.output_tokens = 50
        mock_client.messages.create.return_value = mock_response

        review_pr(MOCK_PR)
        self.assertEqual(mock_client.messages.create.call_count, 2)


if __name__ == "__main__":
    print("Running tests...\n")
    unittest.main(verbosity=2)
