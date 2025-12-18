"""Pytest configuration and shared fixtures."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add both atlassian-skills and scripts directories to path for proper imports
_base_path = Path(__file__).parent.parent
sys.path.insert(0, str(_base_path / 'atlassian-skills'))
sys.path.insert(0, str(_base_path / 'atlassian-skills' / 'scripts'))


@pytest.fixture
def mock_jira_client():
    """Create a mock Jira client."""
    with patch('_common.get_jira_client') as mock:
        client = MagicMock()
        mock.return_value = client
        client.api_path = lambda x: f'/rest/api/2/{x}'
        yield client


@pytest.fixture
def mock_confluence_client():
    """Create a mock Confluence client."""
    with patch('_common.get_confluence_client') as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


@pytest.fixture
def mock_bitbucket_client():
    """Create a mock Bitbucket client."""
    with patch('_common.get_bitbucket_client') as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


@pytest.fixture
def sample_issue_data():
    """Sample Jira issue data."""
    return {
        'key': 'PROJ-123',
        'id': '10001',
        'fields': {
            'summary': 'Test Issue',
            'description': 'Test description',
            'status': {'name': 'Open'},
            'issuetype': {'name': 'Task'},
            'priority': {'name': 'Medium'},
            'assignee': {'emailAddress': 'assignee@example.com'},
            'reporter': {'emailAddress': 'reporter@example.com'},
            'created': '2024-01-01T00:00:00.000+0000',
            'updated': '2024-01-02T00:00:00.000+0000',
            'labels': ['test'],
            'components': [{'name': 'Backend'}]
        }
    }


@pytest.fixture
def sample_page_data():
    """Sample Confluence page data."""
    return {
        'id': '12345',
        'title': 'Test Page',
        'space': {'key': 'TEST'},
        'version': {'number': 1, 'when': '2024-01-01T00:00:00.000Z'},
        'body': {'storage': {'value': '<p>Test content</p>'}},
        'history': {'createdDate': '2024-01-01T00:00:00.000Z'},
        '_links': {'webui': '/wiki/spaces/TEST/pages/12345'}
    }


@pytest.fixture
def sample_pr_data():
    """Sample Bitbucket pull request data."""
    return {
        'id': 1,
        'title': 'Test PR',
        'description': 'Test description',
        'state': 'OPEN',
        'version': 0,
        'fromRef': {
            'displayId': 'feature-branch',
            'repository': {
                'slug': 'test-repo',
                'project': {'key': 'PROJ'}
            }
        },
        'toRef': {
            'displayId': 'main',
            'repository': {
                'slug': 'test-repo',
                'project': {'key': 'PROJ'}
            }
        },
        'author': {
            'user': {
                'name': 'testuser',
                'emailAddress': 'test@example.com'
            }
        },
        'reviewers': [],
        'createdDate': 1704067200000,
        'updatedDate': 1704153600000,
        'open': True,
        'closed': False,
        'locked': False
    }
