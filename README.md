# Atlassian Skills

A Claude Code skill for integrating with Jira, Confluence, and Bitbucket. Supports both Cloud and Data Center deployments.

## What is a Skill?

Skills are folders containing a `SKILL.md` file that teach Claude Code new capabilities. When you add this skill to your project, Claude can directly interact with your Atlassian products - creating issues, searching pages, managing pull requests, and more.

Learn more: https://docs.anthropic.com/en/docs/claude-code/skills

## Features

- **Jira**: Issue management, search (JQL), workflows, agile boards, sprints, worklogs
- **Confluence**: Page management, search (CQL), comments, labels
- **Bitbucket**: Projects, repositories, pull requests, code search, commit history
- **Dual Authentication**: Cloud (API Token) and Data Center (PAT Token)
- **Unified Response Format**: All functions return flattened JSON structures

## Installation

1. Clone or copy the `atlassian-skills` folder into your project
2. Install dependencies:

```bash
pip install -r atlassian-skills/requirements.txt
```

## Configuration

Create a `.env` file in the `atlassian-skills` folder (copy from `.env.example`):

### Jira

```bash
# Cloud
JIRA_URL=https://your-company.atlassian.net
JIRA_USERNAME=your.email@company.com
JIRA_API_TOKEN=your_api_token

# Data Center / Server
JIRA_URL=https://jira.your-company.com
JIRA_PAT_TOKEN=your_pat_token
```

### Confluence

```bash
# Cloud
CONFLUENCE_URL=https://your-company.atlassian.net/wiki
CONFLUENCE_USERNAME=your.email@company.com
CONFLUENCE_API_TOKEN=your_api_token

# Data Center / Server
CONFLUENCE_URL=https://confluence.your-company.com
CONFLUENCE_PAT_TOKEN=your_pat_token
```

### Bitbucket

```bash
BITBUCKET_URL=https://bitbucket.your-company.com
BITBUCKET_PAT_TOKEN=your_pat_token
```

Get your API tokens:
- **Cloud**: https://id.atlassian.com/manage-profile/security/api-tokens
- **Data Center**: Profile → Personal Access Tokens

## Quick Start

Once configured, simply ask Claude to perform Atlassian operations:

### Jira Examples

```
"Create a bug in project MYPROJ with title 'Login button not working' and high priority"

"Search for all in-progress issues assigned to me"

"Transition MYPROJ-123 to Done with a comment"

"Add 2 hours of work to MYPROJ-456"

"Show me all sprints on board 10"
```

### Confluence Examples

```
"Create a new page in DEV space titled 'API Documentation'"

"Search for pages containing 'deployment guide'"

"Add a comment to page 12345"

"Add label 'reviewed' to the architecture page"
```

### Bitbucket Examples

```
"Create a pull request from feature/auth to master in my-repo"

"Show me the last 10 commits on develop branch"

"Search for code containing 'authenticate' in project PROJ"

"Get the diff for PR #42"
```

## Available Functions

### Jira

**jira_issues**
- `jira_get_issue` - Get issue details
- `jira_create_issue` - Create a new issue
- `jira_update_issue` - Update an existing issue
- `jira_delete_issue` - Delete an issue
- `jira_add_comment` - Add a comment to an issue

**jira_search**
- `jira_search` - Search issues using JQL
- `jira_search_fields` - Search field definitions

**jira_workflow**
- `jira_get_transitions` - Get available status transitions
- `jira_transition_issue` - Transition issue to a new status

**jira_agile**
- `jira_get_agile_boards` - Get agile boards
- `jira_get_board_issues` - Get issues from a board
- `jira_get_sprints_from_board` - Get sprints from a board
- `jira_get_sprint_issues` - Get issues in a sprint
- `jira_create_sprint` - Create a new sprint
- `jira_update_sprint` - Update a sprint

**jira_links**
- `jira_get_link_types` - Get available link types
- `jira_create_issue_link` - Create a link between issues
- `jira_link_to_epic` - Link an issue to an epic
- `jira_remove_issue_link` - Remove a link

**jira_worklog**
- `jira_get_worklog` - Get worklog entries
- `jira_add_worklog` - Add a worklog entry

**jira_projects**
- `jira_get_all_projects` - Get all projects
- `jira_get_project_issues` - Get issues for a project
- `jira_get_project_versions` - Get versions for a project
- `jira_create_version` - Create a new version

**jira_users**
- `jira_get_user_profile` - Get user profile

### Confluence

**confluence_pages**
- `confluence_get_page` - Get a page by ID or title
- `confluence_create_page` - Create a new page
- `confluence_update_page` - Update an existing page
- `confluence_delete_page` - Delete a page

**confluence_search**
- `confluence_search` - Search content using CQL

**confluence_comments**
- `confluence_get_comments` - Get comments for a page
- `confluence_add_comment` - Add a comment to a page

**confluence_labels**
- `confluence_get_labels` - Get labels for a page
- `confluence_add_label` - Add a label to a page
- `confluence_remove_label` - Remove a label from a page

**confluence_users**
- `confluence_search_users` - Search for users

### Bitbucket

**bitbucket_projects**
- `bitbucket_list_projects` - List projects
- `bitbucket_list_repositories` - List repositories

**bitbucket_pull_requests**
- `bitbucket_create_pull_request` - Create a pull request
- `bitbucket_get_pull_request` - Get pull request details
- `bitbucket_merge_pull_request` - Merge a pull request
- `bitbucket_decline_pull_request` - Decline a pull request
- `bitbucket_add_pr_comment` - Add a comment to a pull request
- `bitbucket_get_pr_diff` - Get the diff of a pull request

**bitbucket_files**
- `bitbucket_get_file_content` - Get file content from a repository
- `bitbucket_search` - Search for code or files

**bitbucket_commits**
- `bitbucket_get_commits` - Get commit history
- `bitbucket_get_commit` - Get details of a specific commit

## Error Handling

All functions return JSON with consistent error format:

```json
{
  "success": false,
  "error": "Issue not found: PROJ-999",
  "error_type": "NotFoundError"
}
```

Error types: `ConfigurationError`, `AuthenticationError`, `ValidationError`, `NotFoundError`, `APIError`, `NetworkError`

## Time Format Reference

For worklogs: `1w` (week), `2d` (days), `3h` (hours), `30m` (minutes), or combined like `1d 4h 30m`

## License

MIT License
