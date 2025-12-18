"""Tests for confluence_search.py."""

import json
import pytest
from unittest.mock import patch, MagicMock

import sys
from pathlib import Path
_base_path = Path(__file__).parent.parent
sys.path.insert(0, str(_base_path / 'atlassian-skills'))
sys.path.insert(0, str(_base_path / 'atlassian-skills' / 'scripts'))

from scripts.confluence_search import confluence_search


class TestConfluenceSearch:
    """Tests for confluence_search function."""

    @patch('scripts.confluence_search.get_confluence_client')
    def test_search_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {
            'results': [
                {
                    'content': {
                        'id': '12345',
                        'title': 'Test Page',
                        'type': 'page',
                        'space': {'key': 'TEST'},
                        '_links': {'webui': '/wiki/spaces/TEST/pages/12345'}
                    },
                    'url': '/wiki/spaces/TEST/pages/12345',
                    'excerpt': 'This is a test page...',
                    'lastModified': '2024-01-01T00:00:00.000Z'
                }
            ],
            'totalSize': 1
        }

        result = confluence_search('test')
        data = json.loads(result)

        assert len(data['results']) == 1
        assert data['results'][0]['title'] == 'Test Page'
        assert data['total'] == 1

    @patch('scripts.confluence_search.get_confluence_client')
    def test_search_with_pagination(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {
            'results': [],
            'totalSize': 100
        }

        result = confluence_search('test', limit=10, start_at=20)
        data = json.loads(result)

        assert data['start_at'] == 20
        assert data['limit'] == 10

    @patch('scripts.confluence_search.get_confluence_client')
    def test_search_with_cql(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {
            'results': [],
            'totalSize': 0
        }

        result = confluence_search('space = TEST AND type = page')
        data = json.loads(result)

        assert 'results' in data

    @patch('scripts.confluence_search.get_confluence_client')
    def test_search_missing_query(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_search('')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.confluence_search.get_confluence_client')
    def test_search_negative_limit(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_search('test', limit=-1)
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.confluence_search.get_confluence_client')
    def test_search_negative_start_at(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_search('test', start_at=-1)
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'
