## Scripts

This directory contains Python scripts used in CI/CD actions to analyze the adherence of the repositories within the SoDa organization to the established GitHub guidelines.

### Scripts described
- ```check_stale_issues.py``` - process that cycles through all repositories and identifies the stale issues. The STALE_ISSUES_REPORT markdown file is then filled up with the results of the investigation. The frequency of this procedure is configured in the script.