# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "PyGithub>=2.9.1",
# ]
# ///

import os
from datetime import datetime, timedelta, UTC

# pyrefly: ignore [missing-import]
from github import Github

ORG_NAME = os.environ["ORG_NAME"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

DRY_RUN = True
STALE_DAYS = 180

gh = Github(GITHUB_TOKEN)
org = gh.get_organization(ORG_NAME)

cutoff = datetime.now(UTC) - timedelta(days=STALE_DAYS)

for repo in org.get_repos():
    if repo.archived:
        continue

    print(f"\nRepository: {repo.name}")

    try:
        issues = repo.get_issues(state="open")
    except Exception as e:
        print(f"Failed to read issues for {repo.name}: {e}")
        continue

    for issue in issues:

        if issue.pull_request is not None or issue.updated_at.replace(tzinfo=UTC) > cutoff:
            continue

        existing_labels = {label.name for label in issue.labels}

        author = issue.user.login

        print(
            f"Stale issue found: "
            f"{repo.name}#{issue.number} "
            f"(last updated {issue.updated_at})"
        )

        comment = (
            f"@{author} This issue has not been updated in "
            f"over {STALE_DAYS} days.\n\n"
            "Please review whether it is still relevant, "
            "needs further work, or can be closed."
        )

        try:
            if not DRY_RUN:
                issue.create_comment(comment)
                print(f"Commented on issue {repo.name}#{issue.number}")
            else:
                print(f"DRY RUN: Would have commented on issue {repo.name}#{issue.number}")
                print(f"Comment: {comment}")

        except Exception as e:
            print(
                f"Failed to comment on "
                f"{repo.name}#{issue.number}: {e}"
            )
