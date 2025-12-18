"""Tests for confluence_comments.py."""

import json
import pytest
from unittest.mock import patch, MagicMock

import sys
from pathlib import Path
_base_path = Path(__file__).parent.parent
sys.path.insert(0, str(_base_path / 'atlassian-skills'))
sys.path.insert(0, str(_base_path / 'atlassian-skills' / 'scripts'))

from scripts.confluence_comments import confluence_get_comments, confluence_add_comment


class TestConfluenceGetComments:
    """Tests for confluence_get_comments function."""

    @patch('scripts.confluence_comments.get_confluence_client')
    def test_get_comments_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {
            'results': [
                {
                    'id': '10001',
                    'body': {'storage': {'value': 'Test comment'}},
                    'history': {
                        'createdDate': '2024-01-01T00:00:00.000Z',
                        'createdBy': {'displayName': 'Test User'}
                    }
                }
            ]
        }

        result = confluence_get_comments('12345')
        data = json.loads(result)

        assert len(data['comments']) == 1
        assert data['comments'][0]['content'] == 'Test comment'
        assert data['page_id'] == '12345'

    @patch('scripts.confluence_comments.get_confluence_client')
    def test_get_comments_empty(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {'results': []}

        result = confluence_get_comments('12345')
        data = json.loads(result)

        assert len(data['comments']) == 0
        assert data['count'] == 0

    @patch('scripts.confluence_comments.get_confluence_client')
    def test_get_comments_missing_page_id(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_get_comments('')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestConfluenceAddComment:
    """Tests for confluence_add_comment function."""

    @patch('scripts.confluence_comments.get_confluence_client')
    def test_add_comment_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post.return_value = {
            'id': '10002',
            'body': {'storage': {'value': 'New comment'}},
            'history': {
                'createdDate': '2024-01-02T00:00:00.000Z',
                'createdBy': {'displayName': 'Test User'}
            }
        }

        result = confluence_add_comment('12345', 'New comment')
        data = json.loads(result)

        assert data['id'] == '10002'
        assert data['content'] == 'New comment'

    @patch('scripts.confluence_comments.get_confluence_client')
    def test_add_comment_missing_page_id(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_add_comment('', 'Comment text')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.confluence_comments.get_confluence_client')
    def test_add_comment_missing_content(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_add_comment('12345', '')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'
