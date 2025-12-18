"""Tests for jira_search.py."""

import json
import pytest
from unittest.mock import patch, MagicMock

import sys
from pathlib import Path
_base_path = Path(__file__).parent.parent
sys.path.insert(0, str(_base_path / 'atlassian-skills'))
sys.path.insert(0, str(_base_path / 'atlassian-skills' / 'scripts'))

from scripts.jira_search import jira_search, jira_search_fields


class TestJiraSearch:
    """Tests for jira_search function."""

    @patch('scripts.jira_search.get_jira_client')
    def test_search_success(self, mock_get_client, sample_issue_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.get.return_value = {
            'issues': [sample_issue_data],
            'total': 1,
            'startAt': 0,
            'maxResults': 10
        }

        result = jira_search('project = PROJ')
        data = json.loads(result)

        assert len(data['issues']) == 1
        assert data['total'] == 1

    @patch('scripts.jira_search.get_jira_client')
    def test_search_with_pagination(self, mock_get_client, sample_issue_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.get.return_value = {
            'issues': [sample_issue_data],
            'total': 100,
            'startAt': 10,
            'maxResults': 10
        }

        result = jira_search('project = PROJ', limit=10, start_at=10)
        data = json.loads(result)

        assert data['start_at'] == 10
        assert data['total'] == 100

    @patch('scripts.jira_search.get_jira_client')
    def test_search_with_fields(self, mock_get_client, sample_issue_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.get.return_value = {
            'issues': [sample_issue_data],
            'total': 1,
            'startAt': 0,
            'maxResults': 10
        }

        result = jira_search('project = PROJ', fields='summary,status')
        data = json.loads(result)

        assert 'issues' in data

    @patch('scripts.jira_search.get_jira_client')
    def test_search_missing_jql(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_search('')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.jira_search.get_jira_client')
    def test_search_negative_limit(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_search('project = PROJ', limit=-1)
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.jira_search.get_jira_client')
    def test_search_negative_start_at(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_search('project = PROJ', start_at=-1)
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestJiraSearchFields:
    """Tests for jira_search_fields function."""

    @patch('scripts.jira_search.get_jira_client')
    def test_search_fields_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.get.return_value = [
            {
                'id': 'summary',
                'name': 'Summary',
                'description': 'Issue summary',
                'custom': False,
                'schema': {'type': 'string'}
            },
            {
                'id': 'customfield_10001',
                'name': 'Custom Field',
                'description': 'A custom field',
                'custom': True,
                'schema': {'type': 'string'}
            }
        ]

        result = jira_search_fields()
        data = json.loads(result)

        assert len(data['fields']) == 2
        assert data['fields'][0]['name'] == 'Summary'

    @patch('scripts.jira_search.get_jira_client')
    def test_search_fields_with_keyword(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.get.return_value = [
            {
                'id': 'summary',
                'name': 'Summary',
                'description': 'Issue summary',
                'custom': False,
                'schema': {}
            },
            {
                'id': 'description',
                'name': 'Description',
                'description': 'Issue description',
                'custom': False,
                'schema': {}
            }
        ]

        result = jira_search_fields(keyword='summary')
        data = json.loads(result)

        assert len(data['fields']) == 1
        assert data['fields'][0]['name'] == 'Summary'

    @patch('scripts.jira_search.get_jira_client')
    def test_search_fields_with_limit(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.get.return_value = [
            {'id': f'field_{i}', 'name': f'Field {i}', 'description': '', 'custom': False, 'schema': {}}
            for i in range(20)
        ]

        result = jira_search_fields(limit=5)
        data = json.loads(result)

        assert len(data['fields']) == 5
        assert data['total'] == 20

    @patch('scripts.jira_search.get_jira_client')
    def test_search_fields_negative_limit(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_search_fields(limit=-1)
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'
