#!/usr/bin/env python3
"""
Code Review Agent — DEMO MODE
Runs without API keys. Shows realistic output for demonstration.

Usage:
  python demo.py
"""

import time
import sys

MOCK_REVIEW = """
## 1. SUMMARY

This PR introduces a `divide()` function to the calculator module and adds a
guard against division-by-zero by raising a `ValueError`. The change is small,
focused, and addresses a real runtime crash that existed in the original code.

---

## 2. ISSUES

**Issue #1 — Missing type hints**
```python
# Current
def divide(a, b):

# Suggested
def divide(a: float, b: float) -> float:
```
Without type hints, static analysis tools (mypy, Pylance) cannot catch
type mismatches at development time.

**Issue #2 — Exception type could be more specific**
```python
# Current
raise ValueError("Cannot divide by zero")

# Suggested
raise ZeroDivisionError("division by zero")
```
Python has a built-in `ZeroDivisionError` — using it makes the API more
idiomatic and easier for callers to catch specifically.

---

## 3. SUGGESTIONS

- Add a docstring explaining parameters, return value, and raised exceptions.
- Consider returning `float('inf')` instead of raising — depending on use case
  (e.g. scientific computing often prefers infinity over exceptions).
- Add an `__all__` export list to the module if this grows larger.

---

## 4. PRAISE

 Good instinct to raise an exception rather than silently returning `None` or `0`.
 The fix is minimal and doesn't over-engineer the solution.
 PR description clearly explains the intent.

---

## 5. VERDICT

 **REQUEST CHANGES** — Minor fixes needed (type hints + exception type),
but the core logic is correct and the approach is solid.

---

### 🔬 Deep Dive on Issues

**Line 6 — `raise ValueError`**

```python
# calculator.py, line 6
raise ValueError("Cannot divide by zero")
```

**Why it's a problem:** `ValueError` signals "wrong value passed", but
`ZeroDivisionError` is the semantic standard for this case. Code that does
`except ZeroDivisionError` (very common) would silently miss this exception.

**Corrected version:**
```python
def divide(a: float, b: float) -> float:
    \"\"\"Divide a by b. Raises ZeroDivisionError if b is zero.\"\"\"
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b
```

Tokens used this run: 1,842
"""

def typewriter(text: str, delay: float = 0.012):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def spinner(message: str, duration: float = 1.2):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end = time.time() + duration
    i = 0
    while time.time() < end:
        sys.stdout.write(f"\r{frames[i % len(frames)]}  {message}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r  {message}\n")
    sys.stdout.flush()

def main():
    print("\n" + "=" * 60)
    print("  CODE REVIEW AGENT  [DEMO MODE]")
    print("  Repo : facebook/react")
    print("  PR   : #42 — Fix divide by zero bug in calculator")
    print("=" * 60 + "\n")

    spinner("Fetching PR from GitHub...", 1.2)
    time.sleep(0.3)
    print("PR #42: Fix divide by zero bug in calculator")
    print("   by @tester | 1 file changed (calculator.py)\n")

    spinner("Step 1: Initial analysis...", 1.8)
    spinner("Step 2: Deep-dive on issues found...", 1.5)

    print("\n" + "=" * 60)
    print("REVIEW RESULT")
    print("=" * 60)

    typewriter(MOCK_REVIEW, delay=0.008)

    print("=" * 60)
    print("Done!\n")

if __name__ == "__main__":
    main()
