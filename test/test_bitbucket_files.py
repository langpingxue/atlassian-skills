"""Tests for bitbucket_files.py."""

import json
import pytest
from unittest.mock import patch, MagicMock

import sys
from pathlib import Path
_base_path = Path(__file__).parent.parent
sys.path.insert(0, str(_base_path / 'atlassian-skills'))
sys.path.insert(0, str(_base_path / 'atlassian-skills' / 'scripts'))

from scripts.bitbucket_files import bitbucket_get_file_content, bitbucket_search


class TestBitbucketGetFileContent:
    """Tests for bitbucket_get_file_content function."""

    @patch('scripts.bitbucket_files.get_bitbucket_client')
    def test_get_file_content_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {
            'lines': [
                {'text': 'line 1'},
                {'text': 'line 2'},
                {'text': 'line 3'}
            ],
            'size': 3,
            'isLastPage': True
        }

        result = bitbucket_get_file_content('PROJ', 'test-repo', 'src/main.py')
        data = json.loads(result)

        assert data['content'] == 'line 1\nline 2\nline 3'
        assert data['path'] == 'src/main.py'

    @patch('scripts.bitbucket_files.get_bitbucket_client')
    def test_get_file_content_with_branch(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {
            'lines': [{'text': 'content'}],
            'size': 1,
            'isLastPage': True
        }

        result = bitbucket_get_file_content(
            'PROJ', 'test-repo', 'README.md', branch='develop'
        )
        data = json.loads(result)

        assert data['branch'] == 'develop'

    def test_get_file_content_missing_project_key(self):
        result = bitbucket_get_file_content('', 'test-repo', 'file.txt')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    def test_get_file_content_missing_repo_slug(self):
        result = bitbucket_get_file_content('PROJ', '', 'file.txt')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    def test_get_file_content_missing_file_path(self):
        result = bitbucket_get_file_content('PROJ', 'test-repo', '')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestBitbucketSearch:
    """Tests for bitbucket_search function."""

    @patch('scripts.bitbucket_files.get_bitbucket_client')
    def test_search_code_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post.return_value = {
            'code': {
                'values': [
                    {
                        'repository': {'slug': 'test-repo', 'project': {'key': 'PROJ'}},
                        'file': {'toString': 'src/main.py', 'path': 'src/main.py'},
                        'hitCount': 3,
                        'hitContexts': [{'text': 'def search_function():'}]
                    }
                ],
                'count': 1
            }
        }

        result = bitbucket_search('search_function')
        data = json.loads(result)

        assert len(data['results']) == 1
        assert data['results'][0]['repository'] == 'test-repo'

    @patch('scripts.bitbucket_files.get_bitbucket_client')
    def test_search_with_project_filter(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post.return_value = {
            'code': {'values': [], 'count': 0}
        }

        result = bitbucket_search('query', project_key='PROJ')
        data = json.loads(result)

        assert 'project:PROJ' in data['query']

    @patch('scripts.bitbucket_files.get_bitbucket_client')
    def test_search_with_repo_filter(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post.return_value = {
            'code': {'values': [], 'count': 0}
        }

        result = bitbucket_search('query', project_key='PROJ', repository_slug='test-repo')
        data = json.loads(result)

        assert 'repo:PROJ/test-repo' in data['query']

    @patch('scripts.bitbucket_files.get_bitbucket_client')
    def test_search_file_type(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post.return_value = {
            'code': {'values': [], 'count': 0}
        }

        result = bitbucket_search('filename', search_type='file')
        data = json.loads(result)

        assert 'results' in data

    def test_search_missing_query(self):
        result = bitbucket_search('')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    def test_search_invalid_type(self):
        result = bitbucket_search('query', search_type='invalid')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'
