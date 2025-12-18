"""Tests for bitbucket_commits.py."""

import json
import pytest
from unittest.mock import patch, MagicMock

import sys
from pathlib import Path
_base_path = Path(__file__).parent.parent
sys.path.insert(0, str(_base_path / 'atlassian-skills'))
sys.path.insert(0, str(_base_path / 'atlassian-skills' / 'scripts'))

from scripts.bitbucket_commits import bitbucket_get_commits, bitbucket_get_commit


class TestBitbucketGetCommits:
    """Tests for bitbucket_get_commits function."""

    @patch('scripts.bitbucket_commits.get_bitbucket_client')
    def test_get_commits_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {
            'values': [
                {
                    'id': 'abc123def456',
                    'displayId': 'abc123d',
                    'message': 'Initial commit',
                    'author': {'name': 'Test User', 'emailAddress': 'test@example.com'},
                    'committer': {'name': 'Test User', 'emailAddress': 'test@example.com'},
                    'committerTimestamp': 1704067200000,
                    'parents': []
                }
            ],
            'size': 1,
            'isLastPage': True
        }

        result = bitbucket_get_commits('PROJ', 'test-repo')
        data = json.loads(result)

        assert len(data['commits']) == 1
        assert data['commits'][0]['message'] == 'Initial commit'
        assert data['project_key'] == 'PROJ'
        assert data['repository'] == 'test-repo'

    @patch('scripts.bitbucket_commits.get_bitbucket_client')
    def test_get_commits_with_branch(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {
            'values': [],
            'size': 0,
            'isLastPage': True
        }

        result = bitbucket_get_commits('PROJ', 'test-repo', branch='develop')
        data = json.loads(result)

        assert data['branch'] == 'develop'

    @patch('scripts.bitbucket_commits.get_bitbucket_client')
    def test_get_commits_with_pagination(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {
            'values': [],
            'size': 100,
            'isLastPage': False
        }

        result = bitbucket_get_commits('PROJ', 'test-repo', limit=10, start=20)
        data = json.loads(result)

        assert 'commits' in data

    def test_get_commits_missing_project_key(self):
        result = bitbucket_get_commits('', 'test-repo')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    def test_get_commits_missing_repo_slug(self):
        result = bitbucket_get_commits('PROJ', '')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestBitbucketGetCommit:
    """Tests for bitbucket_get_commit function."""

    @patch('scripts.bitbucket_commits.get_bitbucket_client')
    def test_get_commit_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {
            'id': 'abc123def456789',
            'displayId': 'abc123d',
            'message': 'Fix bug in feature',
            'author': {'name': 'Test User', 'emailAddress': 'test@example.com'},
            'committer': {'name': 'Test User', 'emailAddress': 'test@example.com'},
            'committerTimestamp': 1704067200000,
            'parents': [{'id': 'parent123'}]
        }

        result = bitbucket_get_commit('PROJ', 'test-repo', 'abc123def456789')
        data = json.loads(result)

        assert data['id'] == 'abc123def456789'
        assert data['message'] == 'Fix bug in feature'
        assert len(data['parents']) == 1

    def test_get_commit_missing_project_key(self):
        result = bitbucket_get_commit('', 'test-repo', 'abc123')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    def test_get_commit_missing_repo_slug(self):
        result = bitbucket_get_commit('PROJ', '', 'abc123')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    def test_get_commit_missing_commit_id(self):
        result = bitbucket_get_commit('PROJ', 'test-repo', '')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'
