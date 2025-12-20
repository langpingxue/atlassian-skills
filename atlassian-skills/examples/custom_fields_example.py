"""Example: Using custom fields with Jira issues.

This example demonstrates how to create and update Jira issues with custom fields.
Custom fields are commonly used for sprint assignments, story points, custom dropdowns, etc.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from jira_issues import jira_create_issue, jira_update_issue
import json


def example_create_with_custom_fields():
    """Create a Jira issue with custom fields."""
    print("Creating issue with custom fields...")
    
    result = jira_create_issue(
        project_key="PROJ",
        summary="Implement user authentication",
        issue_type="Story",
        description="Add OAuth2 authentication to the API",
        priority="High",
        labels=["backend", "security"],
        custom_fields={
            # Sprint field (typically customfield_10001 or similar)
            "customfield_10001": 5,  # Sprint ID
            
            # Story points (typically customfield_10002 or similar)
            "customfield_10002": 8,
            
            # Custom dropdown/select field
            "customfield_10003": {"value": "Backend Team"},
            
            # Custom text field
            "customfield_10004": "Q1 2024 Initiative",
            
            # Custom number field
            "customfield_10005": 3.5
        }
    )
    
    data = json.loads(result)
    if data.get('success', True):
        print(f"✓ Created issue: {data['key']}")
        print(f"  Summary: {data['summary']}")
    else:
        print(f"✗ Error: {data['error']}")
    
    return data


def example_update_with_custom_fields():
    """Update a Jira issue's custom fields."""
    print("\nUpdating issue custom fields...")
    
    result = jira_update_issue(
        issue_key="PROJ-123",
        custom_fields={
            # Update story points
            "customfield_10002": 13,
            
            # Move to different sprint
            "customfield_10001": 6,
            
            # Update custom text field
            "customfield_10004": "Q2 2024 Initiative"
        }
    )
    
    data = json.loads(result)
    if data.get('success', True):
        print(f"✓ Updated issue: {data['key']}")
    else:
        print(f"✗ Error: {data['error']}")
    
    return data


def example_mixed_fields():
    """Create issue with both standard and custom fields."""
    print("\nCreating issue with mixed fields...")
    
    result = jira_create_issue(
        project_key="PROJ",
        summary="Fix login bug",
        issue_type="Bug",
        description="Users cannot login with special characters in password",
        assignee="user@company.com",
        priority="Critical",
        labels=["bug", "urgent"],
        custom_fields={
            "customfield_10002": 5,  # Story points
            "customfield_10006": {"value": "Production"}  # Environment field
        }
    )
    
    data = json.loads(result)
    if data.get('success', True):
        print(f"✓ Created issue: {data['key']}")
    else:
        print(f"✗ Error: {data['error']}")
    
    return data


if __name__ == "__main__":
    print("=" * 60)
    print("Jira Custom Fields Examples")
    print("=" * 60)
    print("\nNote: Make sure to set your environment variables:")
    print("  - JIRA_URL")
    print("  - JIRA_USERNAME and JIRA_API_TOKEN (Cloud)")
    print("  - or JIRA_PAT_TOKEN (Data Center)")
    print("\nAlso update the custom field IDs to match your Jira instance.")
    print("=" * 60)
    
    # Uncomment to run examples:
    # example_create_with_custom_fields()
    # example_update_with_custom_fields()
    # example_mixed_fields()
    
    print("\n✓ Examples ready to run (uncomment in __main__ section)")
