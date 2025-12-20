# Development Guide

## Overview

This project contains two Atlassian skill variants:

1. **atlassian-skills**: Full-featured skill with both read and write operations
2. **atlassian-readonly-skills**: Read-only variant containing only read operations

The `atlassian-skills` directory is the **source of truth**. Changes should be made there first, then synchronized to `atlassian-readonly-skills` following the process documented below.

## Function Categorization

This table categorizes all 45 functions across Jira, Confluence, and Bitbucket modules as either READ or WRITE operations.

### Jira Functions (25 total)

| Module | Function | Type | Include in Readonly |
|--------|----------|------|---------------------|
| jira_issues | `jira_get_issue` | READ | ✅ |
| jira_issues | `jira_create_issue` | WRITE | ❌ |
| jira_issues | `jira_update_issue` | WRITE | ❌ |
| jira_issues | `jira_delete_issue` | WRITE | ❌ |
| jira_issues | `jira_add_comment` | WRITE | ❌ |
| jira_search | `jira_search` | READ | ✅ |
| jira_search | `jira_search_fields` | READ | ✅ |
| jira_workflow | `jira_get_transitions` | READ | ✅ |
| jira_workflow | `jira_transition_issue` | WRITE | ❌ |
| jira_agile | `jira_get_agile_boards` | READ | ✅ |
| jira_agile | `jira_get_board_issues` | READ | ✅ |
| jira_agile | `jira_get_sprints_from_board` | READ | ✅ |
| jira_agile | `jira_get_sprint_issues` | READ | ✅ |
| jira_agile | `jira_create_sprint` | WRITE | ❌ |
| jira_agile | `jira_update_sprint` | WRITE | ❌ |
| jira_links | `jira_get_link_types` | READ | ✅ |
| jira_links | `jira_create_issue_link` | WRITE | ❌ |
| jira_links | `jira_link_to_epic` | WRITE | ❌ |
| jira_links | `jira_remove_issue_link` | WRITE | ❌ |
| jira_worklog | `jira_get_worklog` | READ | ✅ |
| jira_worklog | `jira_add_worklog` | WRITE | ❌ |
| jira_projects | `jira_get_all_projects` | READ | ✅ |
| jira_projects | `jira_get_project_issues` | READ | ✅ |
| jira_projects | `jira_get_project_versions` | READ | ✅ |
| jira_projects | `jira_create_version` | WRITE | ❌ |
| jira_users | `jira_get_user_profile` | READ | ✅ |

**Jira Summary**: 13 READ operations, 12 WRITE operations

### Confluence Functions (11 total)

| Module | Function | Type | Include in Readonly |
|--------|----------|------|---------------------|
| confluence_pages | `confluence_get_page` | READ | ✅ |
| confluence_pages | `confluence_create_page` | WRITE | ❌ |
| confluence_pages | `confluence_update_page` | WRITE | ❌ |
| confluence_pages | `confluence_delete_page` | WRITE | ❌ |
| confluence_search | `confluence_search` | READ | ✅ |
| confluence_comments | `confluence_get_comments` | READ | ✅ |
| confluence_comments | `confluence_add_comment` | WRITE | ❌ |
| confluence_labels | `confluence_get_labels` | READ | ✅ |
| confluence_labels | `confluence_add_label` | WRITE | ❌ |
| confluence_labels | `confluence_remove_label` | WRITE | ❌ |
| confluence_users | `confluence_search_users` | READ | ✅ |

**Confluence Summary**: 5 READ operations, 6 WRITE operations

### Bitbucket Functions (9 total)

| Module | Function | Type | Include in Readonly |
|--------|----------|------|---------------------|
| bitbucket_projects | `bitbucket_list_projects` | READ | ✅ |
| bitbucket_projects | `bitbucket_list_repositories` | READ | ✅ |
| bitbucket_pull_requests | `bitbucket_get_pull_request` | READ | ✅ |
| bitbucket_pull_requests | `bitbucket_get_pr_diff` | READ | ✅ |
| bitbucket_pull_requests | `bitbucket_create_pull_request` | WRITE | ❌ |
| bitbucket_pull_requests | `bitbucket_merge_pull_request` | WRITE | ❌ |
| bitbucket_pull_requests | `bitbucket_decline_pull_request` | WRITE | ❌ |
| bitbucket_pull_requests | `bitbucket_add_pr_comment` | WRITE | ❌ |
| bitbucket_files | `bitbucket_get_file_content` | READ | ✅ |
| bitbucket_files | `bitbucket_search` | READ | ✅ |
| bitbucket_commits | `bitbucket_get_commits` | READ | ✅ |
| bitbucket_commits | `bitbucket_get_commit` | READ | ✅ |

**Bitbucket Summary**: 9 READ operations, 0 WRITE operations

### Overall Summary

- **Total Functions**: 45
- **Read Operations**: 27 (60%)
- **Write Operations**: 18 (40%)


## Relationship Between Skill Variants

### atlassian-skills (Source of Truth)
- Contains all 45 functions (27 read + 18 write operations)
- All development and bug fixes happen here first
- Complete documentation in SKILL.md and REFERENCE.md
- Full test coverage in the `test/` directory

### atlassian-readonly-skills (Derived)
- Contains only the 27 read operations
- Synchronized from atlassian-skills
- Reduced documentation (read operations only)
- No independent development - changes come from source

### Why Two Variants?

1. **Token Efficiency**: The readonly variant reduces LLM context size by ~40% by excluding write operation documentation
2. **Safety**: Prevents accidental write operations for users who only need read access
3. **Simplicity**: Users with read-only needs see a cleaner, more focused interface

## Sync Process

When changes are made to `atlassian-skills`, follow this process to synchronize to `atlassian-readonly-skills`:

### Step 1: Identify the Change Type

Determine what was changed in `atlassian-skills`:

- **Shared utility change** (`_common.py`, `.env.example`, `requirements.txt`)
- **Read operation change** (function marked as READ in the table above)
- **Write operation change** (function marked as WRITE in the table above)
- **New function added** (needs categorization)

### Step 2: Apply Changes Based on Type

#### For Shared Utility Changes
Copy the entire file from `atlassian-skills` to `atlassian-readonly-skills`:

```bash
# Example: Syncing _common.py
cp atlassian-skills/scripts/_common.py atlassian-readonly-skills/scripts/_common.py

# Example: Syncing requirements.txt
cp atlassian-skills/requirements.txt atlassian-readonly-skills/requirements.txt
```

#### For Read Operation Changes
1. Identify which module file contains the read operation (use the table above)
2. Copy only the read operation function(s) to the corresponding file in `atlassian-readonly-skills`
3. Ensure imports and dependencies are included

**Example**: Updating `jira_get_issue` in `jira_issues.py`
```bash
# Manually copy the jira_get_issue function from:
# atlassian-skills/scripts/jira_issues.py
# to:
# atlassian-readonly-skills/scripts/jira_issues.py
```

#### For Write Operation Changes
No action needed - write operations are not included in the readonly variant.

#### For New Functions
1. Determine if the function is READ or WRITE:
   - **READ**: Uses only GET requests, retrieves data without modification
   - **WRITE**: Uses POST, PUT, DELETE requests, creates/updates/deletes data
2. Add the function to the categorization table in this document
3. If READ: Copy to `atlassian-readonly-skills` following the process above
4. If WRITE: No action needed for readonly variant

### Step 3: Update Documentation

After syncing code changes, update documentation if needed:

#### SKILL.md
If a read operation was added or significantly changed:
1. Update `atlassian-skills/SKILL.md` with full documentation
2. Update `atlassian-readonly-skills/SKILL.md` with the same changes
3. Ensure no write operation documentation appears in the readonly variant

#### REFERENCE.md
If examples or API references changed:
1. Update `atlassian-skills/REFERENCE.md`
2. Update `atlassian-readonly-skills/REFERENCE.md` (read operations only)

### Step 4: Run Tests

After syncing, verify both variants work correctly:

```bash
# Run tests for the main skill
cd test
python -m pytest -v

# Verify readonly scripts don't contain write operations
# (This can be automated with property-based tests)
```

### Step 5: Verify Completeness

Use this checklist to ensure sync is complete:

- [ ] All shared utilities are identical between variants
- [ ] All read operations in the table are present in readonly variant
- [ ] No write operations are present in readonly variant
- [ ] Documentation is updated and consistent
- [ ] Tests pass for both variants
- [ ] Function categorization table is up to date

## Quick Reference: File Sync Matrix

This table shows which files need to be synced and how:

| File | Sync Method | Notes |
|------|-------------|-------|
| `_common.py` | Full copy | Shared utilities |
| `.env.example` | Full copy | Configuration template |
| `requirements.txt` | Full copy | Dependencies |
| `jira_issues.py` | Partial | Only `jira_get_issue` |
| `jira_search.py` | Full copy | All functions are READ |
| `jira_workflow.py` | Partial | Only `jira_get_transitions` |
| `jira_agile.py` | Partial | 4 read functions only |
| `jira_links.py` | Partial | Only `jira_get_link_types` |
| `jira_worklog.py` | Partial | Only `jira_get_worklog` |
| `jira_projects.py` | Partial | 3 read functions only |
| `jira_users.py` | Full copy | All functions are READ |
| `confluence_pages.py` | Partial | Only `confluence_get_page` |
| `confluence_search.py` | Full copy | All functions are READ |
| `confluence_comments.py` | Partial | Only `confluence_get_comments` |
| `confluence_labels.py` | Partial | Only `confluence_get_labels` |
| `confluence_users.py` | Full copy | All functions are READ |
| `bitbucket_projects.py` | Full copy | All functions are READ |
| `bitbucket_pull_requests.py` | Partial | 2 read functions only |
| `bitbucket_files.py` | Full copy | All functions are READ |
| `bitbucket_commits.py` | Full copy | All functions are READ |
| `SKILL.md` | Manual update | Read operations only |
| `REFERENCE.md` | Manual update | Read operations only |

## Adding New Functions

When adding a new function to `atlassian-skills`:

1. **Implement** the function in the appropriate module in `atlassian-skills/scripts/`
2. **Categorize** the function as READ or WRITE
3. **Update** this DEVELOPMENT.md file with the new function in the categorization table
4. **Document** the function in `atlassian-skills/SKILL.md` and `REFERENCE.md`
5. **Test** the function with unit tests in the `test/` directory
6. **Sync** to readonly variant if it's a READ operation:
   - Copy the function to `atlassian-readonly-skills/scripts/`
   - Update `atlassian-readonly-skills/SKILL.md` and `REFERENCE.md`
7. **Verify** the sync using the checklist above

## Troubleshooting

### How do I know if a function is READ or WRITE?

- **READ operations**: Only retrieve data, use GET requests, don't modify state
- **WRITE operations**: Create, update, or delete data, use POST/PUT/DELETE requests

When in doubt, check the HTTP method used in the function implementation.

### What if I accidentally add a write operation to readonly variant?

Remove it immediately and verify with property-based tests that no write operations remain.

### How do I keep documentation in sync?

Always update documentation in both variants when changing read operations. Use the file sync matrix above as a guide.
