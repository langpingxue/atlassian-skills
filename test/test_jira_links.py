"""Tests for jira_links.py."""

import json
import pytest
from unittest.mock import patch, MagicMock

import sys
from pathlib import Path
_base_path = Path(__file__).parent.parent
sys.path.insert(0, str(_base_path / 'atlassian-skills'))
sys.path.insert(0, str(_base_path / 'atlassian-skills' / 'scripts'))

from scripts.jira_links import (
    jira_get_link_types,
    jira_create_issue_link,
    jira_link_to_epic,
    jira_remove_issue_link,
)


class TestJiraGetLinkTypes:
    """Tests for jira_get_link_types function."""

    @patch('scripts.jira_links.get_jira_client')
    def test_get_link_types_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.get.return_value = {
            'issueLinkTypes': [
                {
                    'id': '10000',
                    'name': 'Blocks',
                    'inward': 'is blocked by',
                    'outward': 'blocks'
                },
                {
                    'id': '10001',
                    'name': 'Duplicate',
                    'inward': 'is duplicated by',
                    'outward': 'duplicates'
                }
            ]
        }

        result = jira_get_link_types()
        data = json.loads(result)

        assert len(data['link_types']) == 2
        assert data['link_types'][0]['name'] == 'Blocks'


class TestJiraCreateIssueLink:
    """Tests for jira_create_issue_link function."""

    @patch('scripts.jira_links.get_jira_client')
    def test_create_link_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.post.return_value = {}

        result = jira_create_issue_link(
            link_type='Blocks',
            inward_issue_key='PROJ-123',
            outward_issue_key='PROJ-124'
        )
        data = json.loads(result)

        assert data['success'] is True
        assert 'PROJ-123' in data['message']
        assert 'PROJ-124' in data['message']

    @patch('scripts.jira_links.get_jira_client')
    def test_create_link_with_comment(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.post.return_value = {}

        result = jira_create_issue_link(
            link_type='Blocks',
            inward_issue_key='PROJ-123',
            outward_issue_key='PROJ-124',
            comment='Linking these issues'
        )
        data = json.loads(result)

        assert data['success'] is True

    @patch('scripts.jira_links.get_jira_client')
    def test_create_link_missing_type(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_create_issue_link(
            link_type='',
            inward_issue_key='PROJ-123',
            outward_issue_key='PROJ-124'
        )
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.jira_links.get_jira_client')
    def test_create_link_missing_inward_key(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_create_issue_link(
            link_type='Blocks',
            inward_issue_key='',
            outward_issue_key='PROJ-124'
        )
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestJiraLinkToEpic:
    """Tests for jira_link_to_epic function."""

    @patch('scripts.jira_links.get_jira_client')
    def test_link_to_epic_via_parent(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        
        # Mock epic verification
        mock_client.get.side_effect = [
            {'fields': {'issuetype': {'name': 'Epic'}}},  # Epic check
            {'fields': {}}  # Issue check
        ]
        mock_client.put.return_value = {}

        result = jira_link_to_epic('PROJ-123', 'PROJ-100')
        data = json.loads(result)

        assert data['success'] is True
        assert data['issue_key'] == 'PROJ-123'
        assert data['epic_key'] == 'PROJ-100'

    @patch('scripts.jira_links.get_jira_client')
    def test_link_to_epic_missing_issue_key(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_link_to_epic('', 'PROJ-100')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.jira_links.get_jira_client')
    def test_link_to_epic_missing_epic_key(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_link_to_epic('PROJ-123', '')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.jira_links.get_jira_client')
    def test_link_to_epic_not_an_epic(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.get.return_value = {
            'fields': {'issuetype': {'name': 'Task'}}
        }

        result = jira_link_to_epic('PROJ-123', 'PROJ-100')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestJiraRemoveIssueLink:
    """Tests for jira_remove_issue_link function."""

    @patch('scripts.jira_links.get_jira_client')
    def test_remove_link_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.delete.return_value = True

        result = jira_remove_issue_link('10001')
        data = json.loads(result)

        assert data['success'] is True
        assert data['link_id'] == '10001'

    @patch('scripts.jira_links.get_jira_client')
    def test_remove_link_missing_id(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_remove_issue_link('')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'
