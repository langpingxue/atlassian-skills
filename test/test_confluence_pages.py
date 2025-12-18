"""Tests for confluence_pages.py."""

import json
import pytest
from unittest.mock import patch, MagicMock

import sys
from pathlib import Path
_base_path = Path(__file__).parent.parent
sys.path.insert(0, str(_base_path / 'atlassian-skills'))
sys.path.insert(0, str(_base_path / 'atlassian-skills' / 'scripts'))

from scripts.confluence_pages import (
    confluence_get_page,
    confluence_create_page,
    confluence_update_page,
    confluence_delete_page,
)
from scripts._common import NotFoundError


class TestConfluenceGetPage:
    """Tests for confluence_get_page function."""

    @patch('scripts.confluence_pages.get_confluence_client')
    def test_get_page_by_id(self, mock_get_client, sample_page_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = sample_page_data

        result = confluence_get_page(page_id='12345')
        data = json.loads(result)

        assert data['id'] == '12345'
        assert data['title'] == 'Test Page'

    @patch('scripts.confluence_pages.get_confluence_client')
    def test_get_page_by_title(self, mock_get_client, sample_page_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {'results': [sample_page_data]}

        result = confluence_get_page(title='Test Page', space_key='TEST')
        data = json.loads(result)

        assert data['title'] == 'Test Page'
        assert data['space_key'] == 'TEST'

    @patch('scripts.confluence_pages.get_confluence_client')
    def test_get_page_missing_params(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_get_page()
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.confluence_pages.get_confluence_client')
    def test_get_page_title_without_space(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_get_page(title='Test Page')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.confluence_pages.get_confluence_client')
    def test_get_page_not_found(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {'results': []}

        result = confluence_get_page(title='Nonexistent', space_key='TEST')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'NotFoundError'


class TestConfluenceCreatePage:
    """Tests for confluence_create_page function."""

    @patch('scripts.confluence_pages.get_confluence_client')
    def test_create_page_success(self, mock_get_client, sample_page_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post.return_value = {'id': '12346'}
        mock_client.get.return_value = sample_page_data

        result = confluence_create_page(
            space_key='TEST',
            title='New Page',
            content='<p>Page content</p>'
        )
        data = json.loads(result)

        assert 'id' in data
        mock_client.post.assert_called_once()

    @patch('scripts.confluence_pages.get_confluence_client')
    def test_create_page_with_parent(self, mock_get_client, sample_page_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post.return_value = {'id': '12346'}
        mock_client.get.return_value = sample_page_data

        result = confluence_create_page(
            space_key='TEST',
            title='Child Page',
            content='<p>Child content</p>',
            parent_id='12345'
        )
        data = json.loads(result)

        assert 'id' in data

    @patch('scripts.confluence_pages.get_confluence_client')
    def test_create_page_missing_space_key(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_create_page(
            space_key='',
            title='New Page',
            content='<p>Content</p>'
        )
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.confluence_pages.get_confluence_client')
    def test_create_page_missing_title(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_create_page(
            space_key='TEST',
            title='',
            content='<p>Content</p>'
        )
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.confluence_pages.get_confluence_client')
    def test_create_page_missing_content(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_create_page(
            space_key='TEST',
            title='New Page',
            content=''
        )
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestConfluenceUpdatePage:
    """Tests for confluence_update_page function."""

    @patch('scripts.confluence_pages.get_confluence_client')
    def test_update_page_success(self, mock_get_client, sample_page_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.side_effect = [
            {'version': {'number': 1}},  # Get current version
            sample_page_data  # Get updated page
        ]
        mock_client.put.return_value = {}

        result = confluence_update_page(
            page_id='12345',
            title='Updated Title',
            content='<p>Updated content</p>'
        )
        data = json.loads(result)

        assert 'id' in data
        mock_client.put.assert_called_once()

    @patch('scripts.confluence_pages.get_confluence_client')
    def test_update_page_missing_id(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_update_page(
            page_id='',
            title='Updated Title',
            content='<p>Content</p>'
        )
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.confluence_pages.get_confluence_client')
    def test_update_page_missing_title(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_update_page(
            page_id='12345',
            title='',
            content='<p>Content</p>'
        )
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestConfluenceDeletePage:
    """Tests for confluence_delete_page function."""

    @patch('scripts.confluence_pages.get_confluence_client')
    def test_delete_page_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.delete.return_value = True

        result = confluence_delete_page('12345')
        data = json.loads(result)

        assert data['success'] is True
        assert 'deleted' in data['message'].lower()

    @patch('scripts.confluence_pages.get_confluence_client')
    def test_delete_page_missing_id(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_delete_page('')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'
