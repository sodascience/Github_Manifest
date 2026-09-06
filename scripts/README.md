## Scripts

This directory contains Python scripts used in CI/CD actions to analyze the adherence of the repositories within the SoDa organization to the established (GitHub guidelines)[https://github.com/sodascience/Github_Manifest].

### Scripts described
- ```inactive-issues/check_inactive_issues.py``` - process that cycles through all repositories and identifies inactive issues. The inactivity threshold that determines the issue to be inactive is set up in inactive-issues/config.yml The INACTIVE_ISSUES_REPORT markdown file is then filled up with the results of the investigation. The frequency of this procedure is configured in the script.

  The generated reports and the run log (`logs.json`) are **not** committed to `main`. The job publishes them to the dedicated `reports` branch so it never has to push to the protected default branch.