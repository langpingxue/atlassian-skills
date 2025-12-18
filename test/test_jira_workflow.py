"""Tests for jira_workflow.py."""

import json
import pytest
from unittest.mock import patch, MagicMock

import sys
from pathlib import Path
_base_path = Path(__file__).parent.parent
sys.path.insert(0, str(_base_path / 'atlassian-skills'))
sys.path.insert(0, str(_base_path / 'atlassian-skills' / 'scripts'))

from scripts.jira_workflow import jira_get_transitions, jira_transition_issue


class TestJiraGetTransitions:
    """Tests for jira_get_transitions function."""

    @patch('scripts.jira_workflow.get_jira_client')
    def test_get_transitions_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.get.return_value = {
            'transitions': [
                {
                    'id': '11',
                    'name': 'Start Progress',
                    'to': {'id': '3', 'name': 'In Progress'},
                    'hasScreen': False,
                    'fields': {}
                },
                {
                    'id': '21',
                    'name': 'Done',
                    'to': {'id': '5', 'name': 'Done'},
                    'hasScreen': True,
                    'fields': {
                        'resolution': {
                            'name': 'Resolution',
                            'required': True,
                            'schema': {'type': 'resolution'}
                        }
                    }
                }
            ]
        }

        result = jira_get_transitions('PROJ-123')
        data = json.loads(result)

        assert len(data['transitions']) == 2
        assert data['transitions'][0]['name'] == 'Start Progress'
        assert data['transitions'][1]['to_status'] == 'Done'

    @patch('scripts.jira_workflow.get_jira_client')
    def test_get_transitions_with_required_fields(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.get.return_value = {
            'transitions': [
                {
                    'id': '21',
                    'name': 'Done',
                    'to': {'id': '5', 'name': 'Done'},
                    'hasScreen': True,
                    'fields': {
                        'resolution': {
                            'name': 'Resolution',
                            'required': True,
                            'schema': {'type': 'resolution'}
                        }
                    }
                }
            ]
        }

        result = jira_get_transitions('PROJ-123')
        data = json.loads(result)

        assert 'required_fields' in data['transitions'][0]
        assert len(data['transitions'][0]['required_fields']) == 1

    @patch('scripts.jira_workflow.get_jira_client')
    def test_get_transitions_missing_key(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_get_transitions('')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestJiraTransitionIssue:
    """Tests for jira_transition_issue function."""

    @patch('scripts.jira_workflow.get_jira_client')
    def test_transition_success(self, mock_get_client, sample_issue_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.post.return_value = {}
        mock_client.get.return_value = sample_issue_data

        result = jira_transition_issue('PROJ-123', '11')
        data = json.loads(result)

        assert data['key'] == 'PROJ-123'
        mock_client.post.assert_called_once()

    @patch('scripts.jira_workflow.get_jira_client')
    def test_transition_with_fields(self, mock_get_client, sample_issue_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.post.return_value = {}
        mock_client.get.return_value = sample_issue_data

        result = jira_transition_issue(
            'PROJ-123',
            '21',
            fields={'resolution': {'name': 'Done'}}
        )
        data = json.loads(result)

        assert data['key'] == 'PROJ-123'

    @patch('scripts.jira_workflow.get_jira_client')
    def test_transition_with_comment(self, mock_get_client, sample_issue_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.post.return_value = {}
        mock_client.get.return_value = sample_issue_data

        result = jira_transition_issue(
            'PROJ-123',
            '11',
            comment='Starting work on this issue'
        )
        data = json.loads(result)

        assert data['key'] == 'PROJ-123'

    @patch('scripts.jira_workflow.get_jira_client')
    def test_transition_missing_key(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_transition_issue('', '11')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.jira_workflow.get_jira_client')
    def test_transition_missing_id(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_transition_issue('PROJ-123', '')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'
