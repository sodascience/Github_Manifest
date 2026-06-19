import os
from datetime import datetime, timedelta, UTC
from datetime import date
import json
from pathlib import Path
from github import Auth, Github
from github.Issue import Issue
import yaml

SCRIPT_RELATIVE_DIR = Path(__file__).parent

with open(SCRIPT_RELATIVE_DIR / "config.yml", "r") as f:
    config = yaml.safe_load(f)

ORGANIZATION_NAME   = os.environ.get("GH_TOKEN") 
GITHUB_TOKEN        = os.environ.get("ORG_NAME") 
STALE_AFTER_DAYS    = config["issue_stale_threshold_days"]
CREATE_COMMENTS     = config["create_comments"]
REPORT_TEMPLATE = SCRIPT_RELATIVE_DIR / config["paths"]["report_markdown_template"]
LOG_FILE        = SCRIPT_RELATIVE_DIR / config["paths"]["log_file"]
NEW_REPORT_DIR  = SCRIPT_RELATIVE_DIR / "reports"

DATETIME_NOW        = datetime.now(UTC)
TODAY_STR           = DATETIME_NOW.strftime("%Y-%m-%d")
CUTOFF_DATE         = DATETIME_NOW - timedelta(days=STALE_AFTER_DAYS)
COMMENT_BODY        = config["comment_body"]

github          = Github(auth=Auth.Token(GITHUB_TOKEN))
user            = github.get_user() # TODO: remove
organization    = github.get_organization(ORGANIZATION_NAME)
log_file        :Path        = Path(LOG_FILE)
logged_issues   :dict        = json.loads(log_file.read_text()) if log_file.exists() else {}
stale_issues    :list[Issue] = []

def get_assignees_string(issue: Issue) -> str:
    return ", ".join(a.login for a in issue.assignees) if len(issue.assignees) > 0 else "Empty"

def log_issue(issue: Issue, commented: bool = False):
    """
    Updates the logged issues list that is then used by the update_issues_log_file function
    """
    log = {
        "checkedAt": TODAY_STR,
        "commentAdded": commented,
        "assignees": get_assignees_string(issue)
    }
    logged_issues[issue.html_url] = log

def update_issues_log_file():
    """
    Deletes the issues that were logged more than STALE_AFTER_DAYS days ago
    Saves newly checked issues to the log file 
    """
    for url, log in list(logged_issues.items()):
        checked_at = datetime.strptime(log['checkedAt'], "%Y-%m-%d").replace(tzinfo=UTC)
        if checked_at < DATETIME_NOW - timedelta(days=STALE_AFTER_DAYS):
            del logged_issues[url]

    log_file.write_text(json.dumps(logged_issues, indent=2))

def create_markdown_report():
    """
    Generates a new report by filling in the variable names (issues_table, date, amount_of_days)
    in the markdown report template. Saves the newly created report at configured destination
    """
    rows = []
    for i in stale_issues:
        repo = f"[{i.repository.full_name.split('/')[-1]}]({i.repository_url})" if i.repository_url is not None else "Unknown Repo Link"
        issue_link = f"[{i.title}]({i.html_url})" if i.html_url is not None else "Unknown Issue Link"
        inactive_since = i.updated_at.strftime("%Y-%m-%d") if i.updated_at is not None else "Unknown Last Updated Date"
        assignees_str = get_assignees_string(i)
        rows.append(f"| {issue_link} | {repo} | {inactive_since} | {assignees_str} |")

    rows = "\n".join(rows)

    if len(rows) == 0:
        print("No stale issues found, abort generating the report.")
        exit(0)

    # Add the rows to the markdown table
    with open(REPORT_TEMPLATE, "r", encoding="utf-8") as f:
        content = f.read()

        content = content.replace("%date%", date.today().strftime("%Y-%m-%d"))
        content = content.replace("%amount_of_days%", str(STALE_AFTER_DAYS))
        content = content.replace("%table_rows%", rows)

    new_report_name = f"{NEW_REPORT_DIR}/STALE_ISSUES_REPORT_{date.today().strftime('%Y-%m-%d')}.md"

    with open(new_report_name, "w", encoding="utf-8") as f:
        f.write(content)

def comment_on_issue(issue: Issue, comment_body:str):
    issue.create_comment(comment_body)

for repo in organization.get_repos():
    if repo.archived:
        continue

    try:
        issues = repo.get_issues(state="open")
    except Exception as e:
        print(f"Failed to read issues for {repo.name}: {e}")
        exit(1)

    # Collect issues that are stale and not yet in the log file
    for issue in issues:
        if (issue.pull_request is not None 
            or issue.updated_at.replace(tzinfo=UTC) > CUTOFF_DATE
            or issue.html_url in logged_issues.keys()):
            continue

        log_issue(issue)
        stale_issues.append(issue)

        if CREATE_COMMENTS and len(issue.assignees) > 0:
           issue.create_comment(COMMENT_BODY) 

update_issues_log_file()
create_markdown_report()