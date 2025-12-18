"""Tests for jira_worklog.py."""

import json
import pytest
from unittest.mock import patch, MagicMock

import sys
from pathlib import Path
_base_path = Path(__file__).parent.parent
sys.path.insert(0, str(_base_path / 'atlassian-skills'))
sys.path.insert(0, str(_base_path / 'atlassian-skills' / 'scripts'))

from scripts.jira_worklog import jira_get_worklog, jira_add_worklog


class TestJiraGetWorklog:
    """Tests for jira_get_worklog function."""

    @patch('scripts.jira_worklog.get_jira_client')
    def test_get_worklog_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.get.return_value = {
            'worklogs': [
                {
                    'id': '10001',
                    'comment': 'Worked on feature',
                    'created': '2024-01-01T10:00:00.000+0000',
                    'updated': '2024-01-01T10:00:00.000+0000',
                    'started': '2024-01-01T09:00:00.000+0000',
                    'timeSpent': '2h',
                    'timeSpentSeconds': 7200,
                    'author': {'displayName': 'Test User', 'emailAddress': 'test@example.com'},
                    'updateAuthor': {'displayName': 'Test User', 'emailAddress': 'test@example.com'}
                }
            ]
        }

        result = jira_get_worklog('PROJ-123')
        data = json.loads(result)

        assert len(data['worklogs']) == 1
        assert data['worklogs'][0]['time_spent'] == '2h'
        assert data['issue_key'] == 'PROJ-123'

    @patch('scripts.jira_worklog.get_jira_client')
    def test_get_worklog_empty(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.get.return_value = {'worklogs': []}

        result = jira_get_worklog('PROJ-123')
        data = json.loads(result)

        assert len(data['worklogs']) == 0
        assert data['count'] == 0

    @patch('scripts.jira_worklog.get_jira_client')
    def test_get_worklog_missing_key(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_get_worklog('')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestJiraAddWorklog:
    """Tests for jira_add_worklog function."""

    @patch('scripts.jira_worklog.get_jira_client')
    def test_add_worklog_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.post.return_value = {
            'id': '10002',
            'comment': 'Completed task',
            'created': '2024-01-02T10:00:00.000+0000',
            'updated': '2024-01-02T10:00:00.000+0000',
            'started': '2024-01-02T08:00:00.000+0000',
            'timeSpent': '1h 30m',
            'timeSpentSeconds': 5400,
            'author': {'displayName': 'Test User'},
            'updateAuthor': {'displayName': 'Test User'}
        }

        result = jira_add_worklog('PROJ-123', '1h 30m', comment='Completed task')
        data = json.loads(result)

        assert data['time_spent'] == '1h 30m'
        assert data['issue_key'] == 'PROJ-123'

    @patch('scripts.jira_worklog.get_jira_client')
    def test_add_worklog_with_started(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.post.return_value = {
            'id': '10002',
            'comment': '',
            'created': '2024-01-02T10:00:00.000+0000',
            'updated': '2024-01-02T10:00:00.000+0000',
            'started': '2024-01-01T08:00:00.000+0000',
            'timeSpent': '2h',
            'timeSpentSeconds': 7200,
            'author': {'displayName': 'Test User'},
            'updateAuthor': {'displayName': 'Test User'}
        }

        result = jira_add_worklog(
            'PROJ-123',
            '2h',
            started='2024-01-01T08:00:00.000+0000'
        )
        data = json.loads(result)

        assert data['time_spent'] == '2h'

    @patch('scripts.jira_worklog.get_jira_client')
    def test_add_worklog_with_remaining_estimate(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.post.return_value = {
            'id': '10002',
            'comment': '',
            'created': '2024-01-02T10:00:00.000+0000',
            'updated': '2024-01-02T10:00:00.000+0000',
            'started': '2024-01-02T08:00:00.000+0000',
            'timeSpent': '2h',
            'timeSpentSeconds': 7200,
            'author': {'displayName': 'Test User'},
            'updateAuthor': {'displayName': 'Test User'}
        }

        result = jira_add_worklog(
            'PROJ-123',
            '2h',
            remaining_estimate='4h'
        )
        data = json.loads(result)

        assert data['remaining_estimate_updated'] is True

    @patch('scripts.jira_worklog.get_jira_client')
    def test_add_worklog_missing_key(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_add_worklog('', '1h')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.jira_worklog.get_jira_client')
    def test_add_worklog_missing_time(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_add_worklog('PROJ-123', '')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.jira_worklog.get_jira_client')
    def test_add_worklog_invalid_time_format(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_add_worklog('PROJ-123', 'invalid')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'
