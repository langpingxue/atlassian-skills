"""Tests for jira_issues.py."""

import json
import pytest
from unittest.mock import patch, MagicMock

import sys
from pathlib import Path
_base_path = Path(__file__).parent.parent
sys.path.insert(0, str(_base_path / 'atlassian-skills'))
sys.path.insert(0, str(_base_path / 'atlassian-skills' / 'scripts'))

from scripts.jira_issues import (
    jira_get_issue,
    jira_create_issue,
    jira_update_issue,
    jira_delete_issue,
    jira_add_comment,
)
from scripts._common import ValidationError, NotFoundError


class TestJiraGetIssue:
    """Tests for jira_get_issue function."""

    @patch('scripts.jira_issues.get_jira_client')
    def test_get_issue_success(self, mock_get_client, sample_issue_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.get.return_value = sample_issue_data

        result = jira_get_issue('PROJ-123')
        data = json.loads(result)

        assert data['key'] == 'PROJ-123'
        assert data['summary'] == 'Test Issue'
        mock_client.get.assert_called_once()

    @patch('scripts.jira_issues.get_jira_client')
    def test_get_issue_with_fields(self, mock_get_client, sample_issue_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.get.return_value = sample_issue_data

        result = jira_get_issue('PROJ-123', fields='summary,status')
        data = json.loads(result)

        assert data['key'] == 'PROJ-123'

    @patch('scripts.jira_issues.get_jira_client')
    def test_get_issue_not_found(self, mock_get_client):
        # Mock the client to return an error response directly
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        # Simulate 404 by returning empty/error response
        mock_client.get.return_value = None

        result = jira_get_issue('INVALID-999')
        data = json.loads(result)

        # When get returns None, simplify_issue will fail
        assert data['success'] is False


class TestJiraCreateIssue:
    """Tests for jira_create_issue function."""

    @patch('scripts.jira_issues.get_jira_client')
    def test_create_issue_success(self, mock_get_client, sample_issue_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.post.return_value = {'key': 'PROJ-124'}
        mock_client.get.return_value = sample_issue_data

        result = jira_create_issue(
            project_key='PROJ',
            summary='New Issue',
            issue_type='Task'
        )
        data = json.loads(result)

        assert 'key' in data
        mock_client.post.assert_called_once()

    @patch('scripts.jira_issues.get_jira_client')
    def test_create_issue_with_all_fields(self, mock_get_client, sample_issue_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.post.return_value = {'key': 'PROJ-124'}
        mock_client.get.return_value = sample_issue_data

        result = jira_create_issue(
            project_key='PROJ',
            summary='New Issue',
            issue_type='Task',
            description='Test description',
            assignee='user123',
            priority='High',
            labels=['test', 'urgent']
        )
        data = json.loads(result)

        assert 'key' in data

    @patch('scripts.jira_issues.get_jira_client')
    def test_create_issue_missing_project_key(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_create_issue(
            project_key='',
            summary='New Issue',
            issue_type='Task'
        )
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.jira_issues.get_jira_client')
    def test_create_issue_missing_summary(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_create_issue(
            project_key='PROJ',
            summary='',
            issue_type='Task'
        )
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestJiraUpdateIssue:
    """Tests for jira_update_issue function."""

    @patch('scripts.jira_issues.get_jira_client')
    def test_update_issue_success(self, mock_get_client, sample_issue_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.put.return_value = {}
        mock_client.get.return_value = sample_issue_data

        result = jira_update_issue('PROJ-123', summary='Updated Summary')
        data = json.loads(result)

        assert 'key' in data
        mock_client.put.assert_called_once()

    @patch('scripts.jira_issues.get_jira_client')
    def test_update_issue_missing_key(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_update_issue('')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.jira_issues.get_jira_client')
    def test_update_issue_no_fields(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = jira_update_issue('PROJ-123')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestJiraDeleteIssue:
    """Tests for jira_delete_issue function."""

    @patch('scripts.jira_issues.get_jira_client')
    def test_delete_issue_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.delete.return_value = True

        result = jira_delete_issue('PROJ-123')
        data = json.loads(result)

        assert data['success'] is True
        assert 'deleted' in data['message'].lower()

    @patch('scripts.jira_issues.get_jira_client')
    def test_delete_issue_with_subtasks(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.delete.return_value = True

        result = jira_delete_issue('PROJ-123', delete_subtasks=True)
        data = json.loads(result)

        assert data['success'] is True

    @patch('scripts.jira_issues.get_jira_client')
    def test_delete_issue_missing_key(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_delete_issue('')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestJiraAddComment:
    """Tests for jira_add_comment function."""

    @patch('scripts.jira_issues.get_jira_client')
    def test_add_comment_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.post.return_value = {
            'id': '10001',
            'author': {'emailAddress': 'user@example.com'},
            'body': 'Test comment',
            'created': '2024-01-01T00:00:00.000+0000',
            'updated': '2024-01-01T00:00:00.000+0000'
        }

        result = jira_add_comment('PROJ-123', 'Test comment')
        data = json.loads(result)

        assert data['id'] == '10001'
        assert data['body'] == 'Test comment'

    @patch('scripts.jira_issues.get_jira_client')
    def test_add_comment_missing_key(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_add_comment('', 'Test comment')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.jira_issues.get_jira_client')
    def test_add_comment_missing_text(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_add_comment('PROJ-123', '')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'
