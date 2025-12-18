"""Tests for jira_users.py."""

import json
import pytest
from unittest.mock import patch, MagicMock

import sys
from pathlib import Path
_base_path = Path(__file__).parent.parent
sys.path.insert(0, str(_base_path / 'atlassian-skills'))
sys.path.insert(0, str(_base_path / 'atlassian-skills' / 'scripts'))

from scripts.jira_users import jira_get_user_profile
from scripts._common import NotFoundError, APIError


class TestJiraGetUserProfile:
    """Tests for jira_get_user_profile function."""

    @patch('scripts.jira_users.get_jira_client')
    def test_get_user_by_account_id(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        mock_client.get.return_value = {
            'accountId': '123456',
            'displayName': 'Test User',
            'emailAddress': 'test@example.com',
            'active': True,
            'accountType': 'atlassian',
            'timeZone': 'UTC',
            'locale': 'en_US'
        }

        result = jira_get_user_profile('123456')
        data = json.loads(result)

        assert data['account_id'] == '123456'
        assert data['display_name'] == 'Test User'
        assert data['email'] == 'test@example.com'

    @patch('scripts.jira_users.get_jira_client')
    def test_get_user_by_email_search(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        
        # Direct lookup succeeds
        mock_client.get.return_value = {
            'accountId': '123456',
            'displayName': 'Test User',
            'emailAddress': 'test@example.com',
            'active': True,
            'accountType': 'atlassian',
            'timeZone': 'UTC',
            'locale': 'en_US'
        }

        result = jira_get_user_profile('test@example.com')
        data = json.loads(result)

        assert data['email'] == 'test@example.com'

    @patch('scripts.jira_users.get_jira_client')
    def test_get_user_missing_identifier(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = jira_get_user_profile('')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.jira_users.get_jira_client')
    def test_get_user_not_found(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.api_path = lambda x: f'/rest/api/2/{x}'
        # All lookup methods return empty results
        mock_client.get.side_effect = [
            {},  # First lookup returns empty dict
            [],  # Search returns empty list
            {'users': []}  # Picker returns empty users
        ]

        result = jira_get_user_profile('nonexistent')
        data = json.loads(result)

        assert data['success'] is False
