"""Tests for confluence_users.py."""

import json
import pytest
from unittest.mock import patch, MagicMock

import sys
from pathlib import Path
_base_path = Path(__file__).parent.parent
sys.path.insert(0, str(_base_path / 'atlassian-skills'))
sys.path.insert(0, str(_base_path / 'atlassian-skills' / 'scripts'))

from scripts.confluence_users import confluence_search_users


class TestConfluenceSearchUsers:
    """Tests for confluence_search_users function."""

    @patch('scripts.confluence_users.get_confluence_client')
    def test_search_users_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {
            'results': [
                {
                    'user': {
                        'accountId': '123456',
                        'displayName': 'Test User',
                        'email': 'test@example.com',
                        'accountType': 'atlassian',
                        'profilePicture': {'path': '/avatar/123456'}
                    }
                }
            ]
        }

        result = confluence_search_users('test')
        data = json.loads(result)

        assert len(data['users']) == 1
        assert data['users'][0]['display_name'] == 'Test User'
        assert data['query'] == 'test'

    @patch('scripts.confluence_users.get_confluence_client')
    def test_search_users_with_limit(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {
            'results': [
                {'user': {'accountId': f'{i}', 'displayName': f'User {i}'}}
                for i in range(5)
            ]
        }

        result = confluence_search_users('user', limit=5)
        data = json.loads(result)

        assert len(data['users']) == 5

    @patch('scripts.confluence_users.get_confluence_client')
    def test_search_users_empty(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {'results': []}

        result = confluence_search_users('nonexistent')
        data = json.loads(result)

        assert len(data['users']) == 0
        assert data['count'] == 0

    @patch('scripts.confluence_users.get_confluence_client')
    def test_search_users_missing_query(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_search_users('')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.confluence_users.get_confluence_client')
    def test_search_users_negative_limit(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_search_users('test', limit=-1)
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'
