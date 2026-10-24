#!/usr/bin/env python3
"""Heuristic trust-boundary checker for README / launch-page copy.

Usage:
    python3 trust_boundary_checker.py README.md
    cat README.md | python3 trust_boundary_checker.py -
"""
import re, sys, pathlib

CHECKS = [
    ("Audience and job-to-be-done", [r"for (developers|teams|founders|security|engineers|maintainers)", r"use case", r"problem", r"helps? ", r"built for"], "Say exactly who this is for and what painful job it finishes."),
    ("Trust boundary clarity", [r"runs? (locally|in your|on-prem|self-hosted)", r"cloud", r"browser", r"server", r"agent", r"permission", r"token", r"credential", r"read-only", r"write access"], "Name what runs locally vs remotely, and what permissions/tokens are required."),
    ("Data handling", [r"data", r"privacy", r"log", r"retain", r"store", r"delete", r"pii", r"telemetry", r"encrypted"], "State what data is read, sent, stored, logged, retained, and how to delete it."),
    ("Setup and verification", [r"install", r"quickstart", r"docker", r"npm", r"pip", r"curl", r"example", r"screenshot", r"demo"], "Give a fast path from install to verified success, with expected output."),
    ("Failure modes and limits", [r"limit", r"known issue", r"risk", r"threat", r"fail", r"fallback", r"unsupported", r"false positive", r"false negative"], "List the cases where users should not trust the tool yet."),
    ("Next action", [r"star", r"try", r"sign up", r"contact", r"docs", r"pricing", r"issue", r"contribute", r"get started"], "Make the next useful action obvious above the fold."),
]

def score_text(text):
    low = text.lower()
    rows = []
    total = 0
    for name, patterns, advice in CHECKS:
        hits = sum(1 for p in patterns if re.search(p, low, flags=re.I))
        score = min(10, int(round((hits / max(2, min(5, len(patterns)))) * 10)))
        total += score
        rows.append((name, score, advice, hits))
    percent = int(round(total / (10 * len(CHECKS)) * 100))
    return percent, rows

def starter_patch():
    return """## Trust boundary quick patch

### What runs where
- Local: TODO: name any CLI, browser extension, app, or self-hosted service that runs on the user's machine.
- Remote: TODO: name any hosted API, model provider, analytics, webhook, or update service this product calls.
- Permissions: TODO: list required tokens/scopes and whether access is read-only or write-capable.

### Data handling
- Reads: TODO: list files, repos, prompts, tickets, recordings, customer data, or metadata read by the tool.
- Sends: TODO: list what leaves the user's device/account and where it goes.
- Stores/logs: TODO: list retention, telemetry, logs, and deletion/export path.

### Limits / not safe for
- TODO: list unsupported inputs, false-positive/false-negative risks, production-readiness limits, or compliance boundaries.

### Verification
- TODO: add the shortest install/demo command and the expected successful output or screenshot.
"""

def main(argv):
    if len(argv) != 2:
        print(__doc__.strip())
        return 2
    if argv[1] == "-":
        text = sys.stdin.read()
    else:
        text = pathlib.Path(argv[1]).read_text(encoding="utf-8", errors="replace")
    percent, rows = score_text(text[:30000])
    print(f"Score: {percent}/100")
    if percent >= 75:
        print("Verdict: strong baseline; sharpen proof and conversion friction.")
    elif percent >= 50:
        print("Verdict: usable, but trust-critical details are probably scattered or implicit.")
    else:
        print("Verdict: high-friction first screen for cautious developers.")
    print()
    for name, score, advice, hits in rows:
        print(f"- {name}: {score}/10 ({hits} signal hits)")
        print(f"  Fix: {advice}")
    weakest = sorted(rows, key=lambda row: row[1])[:3]
    print("\nFix these first:")
    for name, score, advice, _hits in weakest:
        print(f"- {name}: {score}/10 — {advice}")
    print("\nCopy/paste starter patch (replace every TODO before publishing):\n")
    print(starter_patch())
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
