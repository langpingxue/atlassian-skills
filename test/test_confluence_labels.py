"""Tests for confluence_labels.py."""

import json
import pytest
from unittest.mock import patch, MagicMock

import sys
from pathlib import Path
_base_path = Path(__file__).parent.parent
sys.path.insert(0, str(_base_path / 'atlassian-skills'))
sys.path.insert(0, str(_base_path / 'atlassian-skills' / 'scripts'))

from scripts.confluence_labels import (
    confluence_get_labels,
    confluence_add_label,
    confluence_remove_label,
)


class TestConfluenceGetLabels:
    """Tests for confluence_get_labels function."""

    @patch('scripts.confluence_labels.get_confluence_client')
    def test_get_labels_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {
            'results': [
                {'name': 'important', 'prefix': 'global'},
                {'name': 'documentation', 'prefix': 'global'}
            ]
        }

        result = confluence_get_labels('12345')
        data = json.loads(result)

        assert len(data['labels']) == 2
        assert data['labels'][0]['name'] == 'important'
        assert data['page_id'] == '12345'

    @patch('scripts.confluence_labels.get_confluence_client')
    def test_get_labels_empty(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {'results': []}

        result = confluence_get_labels('12345')
        data = json.loads(result)

        assert len(data['labels']) == 0
        assert data['count'] == 0

    @patch('scripts.confluence_labels.get_confluence_client')
    def test_get_labels_missing_page_id(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_get_labels('')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestConfluenceAddLabel:
    """Tests for confluence_add_label function."""

    @patch('scripts.confluence_labels.get_confluence_client')
    def test_add_label_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post.return_value = {}

        result = confluence_add_label('12345', 'new-label')
        data = json.loads(result)

        assert data['success'] is True
        assert data['label'] == 'new-label'
        assert data['page_id'] == '12345'

    @patch('scripts.confluence_labels.get_confluence_client')
    def test_add_label_missing_page_id(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_add_label('', 'label')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.confluence_labels.get_confluence_client')
    def test_add_label_missing_name(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_add_label('12345', '')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestConfluenceRemoveLabel:
    """Tests for confluence_remove_label function."""

    @patch('scripts.confluence_labels.get_confluence_client')
    def test_remove_label_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.delete.return_value = True

        result = confluence_remove_label('12345', 'old-label')
        data = json.loads(result)

        assert data['success'] is True
        assert data['label'] == 'old-label'
        assert data['page_id'] == '12345'

    @patch('scripts.confluence_labels.get_confluence_client')
    def test_remove_label_missing_page_id(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_remove_label('', 'label')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    @patch('scripts.confluence_labels.get_confluence_client')
    def test_remove_label_missing_name(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        result = confluence_remove_label('12345', '')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'
