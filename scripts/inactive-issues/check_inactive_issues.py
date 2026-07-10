import os
from datetime import datetime, timedelta, UTC
import json
from pathlib import Path
from github import Auth, Github
from github.Issue import Issue
from github.Repository import Repository
import yaml
import re

SCRIPT_RELATIVE_DIR = Path(__file__).parent

with open(SCRIPT_RELATIVE_DIR / "config.yml", "r") as f:
    config = yaml.safe_load(f) or {}

GITHUB_TOKEN        = os.environ.get("GITHUB_TOKEN") 
ORGANIZATION_NAME   = os.environ.get("ORG_NAME") 
INACTIVE_AFTER_DAYS = config.get("issue_inactivity_threshold_days", 180)
CREATE_COMMENTS     = config.get("create_comments", False)
REPORT_TEMPLATE     = SCRIPT_RELATIVE_DIR / config["paths"]["report_markdown_template"]
LOG_FILE_PATH       = SCRIPT_RELATIVE_DIR / 'logs.json'
NEW_REPORT_DIR      = SCRIPT_RELATIVE_DIR / 'reports'

COMMENT_BODY        = config["comment_body"].replace("%amount_of_days%", str(INACTIVE_AFTER_DAYS))
DATETIME_NOW        = datetime.now(UTC)
CURRENT_DATE_STR    = DATETIME_NOW.strftime("%Y-%m-%d")
CUTOFF_DATETIME     = DATETIME_NOW - timedelta(days=INACTIVE_AFTER_DAYS)

if not GITHUB_TOKEN or not ORGANIZATION_NAME:
    print("::error::Please make sure the GITHUB_TOKEN and ORGANIZATION_NAME environment variables are defined.")
    exit(1)  

def load_logged_issues(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        print(f"::warning::{path} is empty or invalid JSON, starting with an empty log.")
        return {}

github          = Github(auth=Auth.Token(GITHUB_TOKEN))
organization    = github.get_organization(ORGANIZATION_NAME)
log_file        = Path(LOG_FILE_PATH)
logged_issues_by_url :dict          = load_logged_issues(log_file)
inactive_issues      :list[Issue]   = []

def get_contact_person(repo: Repository) -> str:
    """
    For the given repository, extracts 2 types of contacts, names linked to github profiles or email adresses
    from the Contact section of the readme.
    Returns "Not found" if no contacts are found for a repo.
    """
    content = repo.get_readme().decoded_content.decode("utf-8")
    last_contact_position = content.lower().rfind("contact")
    if last_contact_position == -1:
        return "Contact section not found"

    contact_content = content[last_contact_position:]
    contact_link_regexp = r'\[([^\]]+)\]\((https?://[^\)]+)\)'
    contact_email_regexp = r'\[[^\]]+\]\(mailto:([^\)]+)\)'

    links = re.findall(contact_link_regexp, contact_content)
    emails = re.findall(contact_email_regexp, contact_content)
    
    links_strings = [f"[{name.replace(chr(10), ' ').strip()}]({url})" for name, url in links]
    contact_persons = links_strings + emails

    if contact_persons:
        return ", ".join(contact_persons)
    
    # Edge case when contact section exists but no contacts detected by the regex,
    # might have information about institution collaboration (e.g. websweep: https://github.com/sodascience/websweep)
    return "Contact person not found" 

def get_assignees_string(issue: Issue) -> str:
    return ", ".join(a.login for a in issue.assignees) if len(issue.assignees) > 0 else "Empty"

def log_issue(issue: Issue, commented: bool = False):
    """
    Updates the logged issues list that is then used by the update_issues_log_file function
    """
    log = {
        "checkedAt": CURRENT_DATE_STR,
        "commentAdded": commented,
        "assignees": get_assignees_string(issue)
    }
    logged_issues_by_url[issue.html_url] = log

def update_issues_log_file():
    """
    Removes from the log file the issues that were logged more than INACTIVE_AFTER_DAYS days ago
    Saves newly checked issues to the log file 
    """
    for url, log in list(logged_issues_by_url.items()):
        checked_at = datetime.strptime(log['checkedAt'], "%Y-%m-%d").replace(tzinfo=UTC)
        if checked_at < DATETIME_NOW - timedelta(days=INACTIVE_AFTER_DAYS):
            del logged_issues_by_url[url]

    log_file.write_text(json.dumps(logged_issues_by_url, indent=2))

def create_markdown_report():
    """
    Generates a new report by filling in the variable names (issues_table, date, amount_of_days)
    in the markdown report template. Saves the newly created report at configured destination
    """
    issues_table_rows = []
    for i in inactive_issues:
        repo_link = f"[{i.repository.full_name.split('/')[-1]}]({i.repository.html_url})" if i.repository is not None else "Unknown Repo Link"
        issue_link = f"[{i.title}]({i.html_url})" if i.html_url is not None else "Unknown Issue Link"
        inactive_since = i.updated_at.strftime("%Y-%m-%d") if i.updated_at is not None else "Unknown Last Updated Date"
        assignees_str = get_assignees_string(i)
        owner_name    = get_contact_person(i.repository)
        repository_contributors = ", ".join([f"[{c.login}]({c.html_url})" for c in i.repository.get_contributors()])
        issues_table_rows.append(f"| {issue_link} | {repo_link} | {inactive_since} | {assignees_str} | {owner_name} | {repository_contributors} |")

    issues_table_rows = "\n".join(issues_table_rows)

    if len(issues_table_rows) == 0:
        print("No inactive issues found, abort generating the report.")
        exit(0)

    # Add the rows to the markdown table
    with open(REPORT_TEMPLATE, "r", encoding="utf-8") as f:
        content = f.read()

        content = content.replace("%date%", CURRENT_DATE_STR)
        content = content.replace("%amount_of_days%", str(INACTIVE_AFTER_DAYS))
        content = content.replace("%table_rows%", issues_table_rows)

    new_report_name = f"{NEW_REPORT_DIR}/INACTIVE_ISSUES_REPORT_{CURRENT_DATE_STR}.md"

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

    # Collect issues that are inactive and not yet in the log file
    for issue in issues:
        if (issue.pull_request is not None 
            or issue.updated_at.replace(tzinfo=UTC) > CUTOFF_DATETIME):
            continue

        # skip issue if it has already been logged
        if issue.html_url in logged_issues_by_url.keys():
            continue

        log_issue(issue)
        inactive_issues.append(issue)

        if CREATE_COMMENTS and len(issue.assignees) > 0:
           issue.create_comment(COMMENT_BODY)
           

update_issues_log_file()
create_markdown_report()