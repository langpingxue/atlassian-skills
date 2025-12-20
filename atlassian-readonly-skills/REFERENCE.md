# Atlassian Readonly Skills API Reference

Detailed usage examples and API documentation for read-only Jira, Confluence, and Bitbucket operations.

## Jira Examples

### Search for Issues

```python
from scripts.jira_search import jira_search

# Search using JQL
result = jira_search("project = MYPROJ AND status = 'In Progress'", limit=10)

# Search with specific fields
result = jira_search(
    jql="assignee = currentUser() AND status != Done",
    fields="summary,status,priority",
    limit=20
)
```

### Get Available Fields

```python
from scripts.jira_search import jira_search_fields

# Get all available fields for searching
result = jira_search_fields()
```

### Get Issue Details

```python
from scripts.jira_issues import jira_get_issue

# Get issue by key
result = jira_get_issue("MYPROJ-123")

# Get issue with specific fields
result = jira_get_issue("MYPROJ-123", fields="summary,status,assignee,priority")
```

### Get Available Transitions

```python
from scripts.jira_workflow import jira_get_transitions

# Get available transitions for an issue
transitions = jira_get_transitions("MYPROJ-123")
```

### Get Worklog Entries

```python
from scripts.jira_worklog import jira_get_worklog

# Get worklog for an issue
result = jira_get_worklog("MYPROJ-123")
```

### Get Link Types

```python
from scripts.jira_links import jira_get_link_types

# Get available link types
result = jira_get_link_types()
```

### Get Projects and Versions

```python
from scripts.jira_projects import jira_get_all_projects, jira_get_project_issues, jira_get_project_versions

# Get all projects
projects = jira_get_all_projects()

# Get issues for a project
issues = jira_get_project_issues("MYPROJ", limit=50)

# Get versions for a project
versions = jira_get_project_versions("MYPROJ")
```

### Get User Profile

```python
from scripts.jira_users import jira_get_user_profile

# Get user profile by account ID
result = jira_get_user_profile("5d123abc456def789")

# Get user profile by email
result = jira_get_user_profile(email="user@example.com")
```

### Agile Boards and Sprints

```python
from scripts.jira_agile import (
    jira_get_agile_boards,
    jira_get_board_issues,
    jira_get_sprints_from_board,
    jira_get_sprint_issues
)

# Find boards
boards = jira_get_agile_boards(project_key="MYPROJ")

# Get issues on a board
issues = jira_get_board_issues(board_id="123", limit=50)

# Get sprints from a board
sprints = jira_get_sprints_from_board(board_id="123", state="active")

# Get issues in a sprint
sprint_issues = jira_get_sprint_issues(sprint_id="456", limit=50)
```

## Confluence Examples

### Search for Pages

```python
from scripts.confluence_search import confluence_search

# Search for pages
result = confluence_search("API documentation", limit=10)

# Search in specific space
result = confluence_search("guide", space_key="DEV", limit=20)
```

### Get a Page

```python
from scripts.confluence_pages import confluence_get_page

# Get by ID
result = confluence_get_page(page_id="123456")

# Get by title and space
result = confluence_get_page(title="API Guide", space_key="DEV")
```

### Get Comments

```python
from scripts.confluence_comments import confluence_get_comments

# Get comments for a page
comments = confluence_get_comments(page_id="123456")
```

### Get Labels

```python
from scripts.confluence_labels import confluence_get_labels

# Get labels for a page
labels = confluence_get_labels(page_id="123456")
```

## Bitbucket Examples

### List Projects and Repositories

```python
from scripts.bitbucket_projects import bitbucket_list_projects, bitbucket_list_repositories

# List all projects
projects = bitbucket_list_projects(limit=25)

# List repositories in a project
repos = bitbucket_list_repositories(project_key="PROJ", limit=50)
```

### Get Pull Request Details

```python
from scripts.bitbucket_pull_requests import bitbucket_get_pull_request, bitbucket_get_pr_diff

# Get PR details
result = bitbucket_get_pull_request(
    project_key="PROJ",
    repository_slug="my-repo",
    pr_id=123
)

# Get PR diff
diff = bitbucket_get_pr_diff(
    project_key="PROJ",
    repository_slug="my-repo",
    pr_id=123
)
```

### Get File Content

```python
from scripts.bitbucket_files import bitbucket_get_file_content, bitbucket_search

# Get file content
result = bitbucket_get_file_content(
    project_key="PROJ",
    repository_slug="my-repo",
    file_path="src/main.py",
    branch="master"
)

# Search for code
result = bitbucket_search(
    query="def authenticate",
    project_key="PROJ",
    search_type="code",
    limit=25
)
```

### Get Commits

```python
from scripts.bitbucket_commits import bitbucket_get_commits, bitbucket_get_commit

# Get recent commits from a branch
result = bitbucket_get_commits(
    project_key="PROJ",
    repository_slug="my-repo",
    branch="master",
    limit=10
)

# Get specific commit details
result = bitbucket_get_commit(
    project_key="PROJ",
    repository_slug="my-repo",
    commit_id="1da11eaec25aed8b251de24841885c91493b3173"
)
```

## JQL Query Examples

Common JQL patterns for searching Jira issues:

```
# Issues assigned to current user
assignee = currentUser()

# Open issues in a project
project = MYPROJ AND status != Done

# High priority bugs
project = MYPROJ AND issuetype = Bug AND priority = High

# Issues updated in last 7 days
updated >= -7d

# Issues in current sprint
sprint in openSprints()

# Unassigned issues
assignee is EMPTY

# Issues with specific label
labels = "backend"

# Issues created by specific user
reporter = "user@example.com"

# Combined query
project = MYPROJ AND status = "In Progress" AND assignee = currentUser() ORDER BY priority DESC
```

## CQL Query Examples

Common CQL patterns for searching Confluence:

```
# Search by text
text ~ "API documentation"

# Search in specific space
space = DEV AND text ~ "guide"

# Search by title
title ~ "Getting Started"

# Search by label
label = "api-docs"

# Search by type
type = page AND space = DEV

# Recently modified
lastModified >= now("-7d")

# Created by user
creator = "user@example.com"
```

## Response Format

### Success Response

```json
{
  "key": "MYPROJ-123",
  "summary": "Issue title",
  "status": "In Progress",
  "assignee": "user@example.com"
}
```

### Error Response

```json
{
  "success": false,
  "error": "Issue not found: MYPROJ-999",
  "error_type": "NotFoundError"
}
```

### Paginated Response

```json
{
  "issues": [...],
  "total": 150,
  "start_at": 0,
  "max_results": 10,
  "is_last": false
}
```

## Bitbucket Response Examples

### Commit Response Structure

```json
{
  "project_key": "PROJ",
  "repository": "my-repo",
  "branch": "master",
  "total": 5,
  "is_last_page": false,
  "commits": [
    {
      "id": "1da11eaec25aed8b251de24841885c91493b3173",
      "display_id": "1da11eaec25",
      "message": "Feature: Add new API endpoint",
      "author_name": "John Doe",
      "author_email": "john.doe@company.com",
      "committer_name": "John Doe",
      "committer_email": "john.doe@company.com",
      "timestamp": 1765534577000,
      "parents": ["b97ad25d330e36480b045c5dea36f97999297ff6"]
    }
  ]
}
```

### Pull Request Response Structure

```json
{
  "id": 123,
  "title": "Feature: Add authentication",
  "description": "Implements OAuth2 authentication",
  "state": "OPEN",
  "author": {
    "name": "John Doe",
    "email": "john.doe@company.com"
  },
  "from_ref": {
    "branch": "feature/auth",
    "commit": "abc123"
  },
  "to_ref": {
    "branch": "master",
    "commit": "def456"
  },
  "created_date": 1765534577000,
  "updated_date": 1765534577000
}
```
