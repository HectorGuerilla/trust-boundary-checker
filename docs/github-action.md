# GitHub Action example

This repository is intentionally just a small Python heuristic, so the simplest CI use is to download the script and run it against `README.md` when documentation changes.

Copy `.github/workflows/trust-boundary-check.yml` into your own repository:

```yaml
name: Trust boundary README check

on:
  pull_request:
    paths:
      - 'README.md'
      - 'docs/**'
  workflow_dispatch:

jobs:
  trust-boundary-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Download checker
        run: curl -fsSL -o trust_boundary_checker.py https://raw.githubusercontent.com/HectorGuerilla/trust-boundary-checker/main/trust_boundary_checker.py
      - name: Score README
        run: python3 trust_boundary_checker.py README.md
```

The checker currently reports a score; it does not fail builds by default. If you want to enforce a floor, wrap the script output and fail below your chosen threshold.
