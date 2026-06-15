import os
from datetime import datetime, timedelta, UTC
from datetime import date
import json
from pathlib import Path
from github import Auth, Github

SCRIPT_DIR = Path(__file__).parent

ORG_NAME = "sodascience"
REPORT_TEMPLATE = SCRIPT_DIR / "STALE_ISSUES_REPORT_TEMPLATE.md"
DRY_RUN = True
STATE_FILE = SCRIPT_DIR / "stale_seen.json"
STALE_DAYS = 180
NEW_REPORT_DIR = SCRIPT_DIR / "reports"
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

auth = Auth.Token(GITHUB_TOKEN)
gh = Github(auth=auth)
org = gh.get_organization(ORG_NAME)
today = date.today().strftime("%Y-%m-%d")
cutoff = datetime.now(UTC) - timedelta(days=STALE_DAYS)
seen_file = Path(STATE_FILE)
seen = json.loads(seen_file.read_text()) if seen_file.exists() else {}
stale_issues = []

for repo in org.get_repos():
    if repo.archived:
        continue

    try:
        issues = repo.get_issues(state="open")
    except Exception as e:
        print(f"Failed to read issues for {repo.name}: {e}")
        continue

    for issue in issues:
        if (issue.pull_request is not None 
            or issue.updated_at.replace(tzinfo=UTC) > cutoff
            or issue.html_url in seen.keys()):
            continue

        print(f"Checking issue: {issue.html_url}")

        seen[issue.html_url] = today
        author = issue.user.login
        stale_issues.append(issue)

# update seen file: delete issues seen more than STALE_DAYS ago, and add new issues to seen
for url, seen_date in list(seen.items()):
    if datetime.strptime(seen_date, "%Y-%m-%d") < datetime.now() - timedelta(days=STALE_DAYS):
        del seen[url]

seen_file.write_text(json.dumps(seen, indent=2))

# Generate rows for each inactive issue to be added to the markdown table
rows = []
for i in stale_issues:
    repo = f"[{i.repository.full_name.split('/')[-1]}]({i.repository_url})" if i.repository_url is not None else "Unknown Repo Link"
    issue_link = f"[{i.title}]({i.html_url})" if i.html_url is not None else "Unknown Issue Link"
    inactive_since = i.updated_at.strftime("%Y-%m-%d") if i.updated_at is not None else "Unknown Last Updated Date"
    rows.append(f"| {issue_link} | {repo} | {inactive_since} | ")

rows = "\n".join(rows)

if len(rows) == 0:
    print("No stale issues found.")
    exit(0)

# Add the rows to the markdown table
with open(REPORT_TEMPLATE, "r", encoding="utf-8") as f:
    content = f.read()

    content = content.replace("%date%", date.today().strftime("%Y-%m-%d"))
    content = content.replace("%amount_of_days%", str(STALE_DAYS))
    content = content.replace("%table_rows%", rows)

new_report_name = f"{NEW_REPORT_DIR}/STALE_ISSUES_REPORT_{date.today().strftime('%Y-%m-%d')}.md"

with open(new_report_name, "w", encoding="utf-8") as f:
    f.write(content)