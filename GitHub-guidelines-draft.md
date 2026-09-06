# SoDa GitHub Guidelines

> **ODISSEI Social Data Science Team** — GitHub Practices, Standards & Project Management

This document defines the standards, workflows, and expectations for all repositories under the [`sodascience`](https://github.com/sodascience) GitHub organization. Given that existing projects do not yet incorporate these standards, we will work on them iteratively.

---

## Table of Contents

1. [Repository Types & Principles](#1-repository-types--principles)
2. [Folder Structure](#2-folder-structure)
3. [Branching Strategy](#3-branching-strategy)
4. [Commit Message Standard](#4-commit-message-standard)
5. [Pull Requests & Code Review](#5-pull-requests--code-review)
6. [Issue Management](#6-issue-management)
7. [Recommendations for new repositories](#7-recommendations-for-new-repositories)

---

## 1. Repository Types & Principles

### Non-negotiable defaults for every repository

- **No secrets in git** — Secrets can be anything from API keys to passwords. Use Github secrets or `.env` files locally (never committed) 
- **No large or sensitive data in git** — document how to obtain data in `data/README.md`
- **Branch protection on `main`** — direct pushes are never allowed; all changes go via PR
- **Default branch is `main`** — not `master`

---

## 2. Folder Structure

The structure below is the standard. Follow it for new projects; migrate existing ones gradually.

### Python Software Package

```
my-package/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              # Lint + test on every PR
│   │   └── release.yml         # Publish to PyPI on tag
│   ├── ISSUE_TEMPLATE/         # Optional
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── pull_request_template.md
├── docs/
├── src/
│   └── my_package/
├── tests/
├── examples/
├── README.md
└── pyproject.toml
```

### Research / Analysis Project

```
my-research-project/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   ├── raw/                    # Original, immutable — never committed if sensitive
│   ├── processed/
│   └── README.md               # Describe sources, access instructions, and restrictions
├── notebooks/                  # Numbered sequentially: 01_exploration.ipynb
├── src/
│   └── project_name/           # Reusable modules extracted from notebooks
├── results/
│   ├── figures/
│   └── tables/
├── README.md
└── environment.yml             # Pin all dependencies for reproducibility
```

---

NOTE: For this type of project we have a template which follows the recommended project structure and makes the setup a bit easier. It can be found [here](https://github.com/sodascience/research-project-boilerplate).

## 3. Branching Strategy

### Default: GitHub Flow (Recommended for most projects)

Used for **all projects by default** — research, workshops, tools, and early-stage packages.

```
main ──●──────────────────────────●──── (protected, always stable)
        \                        /
         feature/my-feature ────●
```

All work happens in short-lived feature branches that merge into `main` via PR. `main` is always in a state that could be shared or deployed.

> All projects that use GitHub Flow should also use [GitHub Actions](#8-cicd-with-github-actions) to automate the CI/CD process.

### For mature software packages: GitFlow (not recommended)

Use when a package has **versioned releases and a public API** (e.g., `metasyn`) or older projects that already use it.

```
main     ──●────────────────────────●──  (tagged releases only)
            \                      /
develop  ────●────●──────────────●────
              \  /\              /
         feature  \            /
                  release/1.2.0
```

| Branch | Purpose |
|---|---|
| `main` | Tagged, published releases only |
| `develop` | Active development, integration target |
| `feature/<name>` | All new work, branched from `develop` |
| `release/<version>` | Stabilization before tagging |
| `hotfix/<name>` | Urgent fixes applied directly to `main` + `develop` |

### Branch naming

```
feature/42-add-csv-export       # reference issue number when it exists
fix/null-handling-parser
docs/update-contributing
refactor/simplify-api
release/1.3.0
hotfix/security-input-validation
```

> Always prefix with the change type. Reference the issue number when one exists.

---

## 4. Commit Message Standard

All projects must use [Conventional Commits](https://www.conventionalcommits.org/).

### Format

```
<type>(<optional scope>): <short description>

[optional body: explain WHY, not WHAT]

[optional footer: Closes #42, BREAKING CHANGE: ...]
```

### Commit types

| Type | Use for | Version bump |
|---|---|---|
| `feat` | New feature or capability | Minor |
| `fix` | Bug fix | Patch |
| `docs` | Documentation changes only | — |
| `refactor` | Code restructuring, no behavior change | — |
| `test` | Adding or fixing tests | — |
| `chore` | Dependency updates, CI config, build tooling | — |
| `perf` | Performance improvement | Patch |
| `ci` | GitHub Actions / workflow changes | — |
| `revert` | Revert a previous commit | Patch |

### Breaking changes

Append `!` and add a `BREAKING CHANGE:` footer:

```
feat!: remove deprecated fit_dataframe() method

BREAKING CHANGE: fit_dataframe() was removed. Use MetaFrame.fit_dataframe() instead.
```

### Examples

```bash
# Good ✅
feat(parser): add support for reading Parquet files
fix(synthesis): handle missing values in date columns correctly
chore: upgrade pandas to 2.1.0
refactor(api): simplify MetaFrame constructor interface

# Bad ❌
fixed stuff
WIP
update
changes to parser
```

**Rules:**
- Imperative mood: "add feature" — not "added" or "adds"
- Concise header ≤ 72 characters
- One logical change per commit — atomic commits simplify reverting and `git bisect` (command that helps finding a bug in a commit history)
- Reference issues in footer: `Closes #42` where relevant

---

## 5. Pull Requests & Code Review



### PR expectations

- PRs are required for all changes to `main` (and `develop` in GitFlow)
- **No self-merging** — every PR needs at least one reviewer who is not the author for collaborations. This not necessarily required for smaller projects.

### PR title

Follows Conventional Commits format:

```
feat(synthesis): add Gaussian copula for multivariate synthesis
fix(parser): resolve crash on empty input file
```

### PR description template (`.github/pull_request_template.md`)

```markdown
## What does this PR do?

## Why is this change needed?

## How to test it

## Related issues
Closes #
```

Simple and direct. Reviewers shouldn't need to guess context.

### Merge strategy

**Squash commits about similar changes** (Conventional Commits).  
**Merge commit** for release branches — preserve the full commit history of the release.

---

## 6. Issue Management

### Issue templates

Add these to `.github/ISSUE_TEMPLATE/` in every repository. They prevent vague reports and save maintainer time.

**`bug_report.md`:**
```markdown
---
name: Bug report
about: Report unexpected behavior
labels: bug
---

## Expected vs actual behavior

## How to reproduce the bug (please include screenshots or code where possible)

## Environment
- OS:
- Python/R version:
- Package version:
```


### Issue lifecycle

Every issue that is closed without a linked PR **must have a comment** explaining why.

Periodically (every few months) review all open issues and close those that are no longer relevant.

---

## 7. Recommendations for new repositories

### Topics
When on the homepage of your repository you can click on the settings icon in the about section to add topics to a repository. This is useful as people can easily find out what your project is about. For example if you are using an LLM to analyze CBS data in Python you would use the "cbs" "llm" and "python" tags. Please add these as it makes the purpose of a repository much more clear. Standard convention here is to use lowercase and only to use abbreviations when the abbreviation is generally used more than the full version.
### Tests

When developing a tool that others will hopefully use someday it is important to make sure it works as intended. Therefore testing your code to verify this is the case is very useful. It has the additional benefit of being an automatic check whether or not a new change breaks some existing core functionality.

Thus, it is important for all new repositories to have tests that are executed by CI and test the functionality of the code every time there is a PR to the 'main' branch wherever reasonable. If the project is mostly data analysis or is not intended to be reusable this may not apply. This is however a case of author discretion.

Structure of the `tests` directory:

`tests/`
├── `conftest.py`             # Pytest fixtures and shared config
├── `test_example.py`         # Example test file
├── `test_example_feature.py` # Tests for specific feature
└── `data/`                     # Test data files
    └── `test_data.csv`         # Example test data