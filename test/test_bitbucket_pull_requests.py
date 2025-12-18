"""Tests for bitbucket_pull_requests.py."""

import json
import pytest
from unittest.mock import patch, MagicMock

import sys
from pathlib import Path
_base_path = Path(__file__).parent.parent
sys.path.insert(0, str(_base_path / 'atlassian-skills'))
sys.path.insert(0, str(_base_path / 'atlassian-skills' / 'scripts'))

from scripts.bitbucket_pull_requests import (
    bitbucket_create_pull_request,
    bitbucket_get_pull_request,
    bitbucket_merge_pull_request,
    bitbucket_decline_pull_request,
    bitbucket_add_pr_comment,
    bitbucket_get_pr_diff,
)


class TestBitbucketCreatePullRequest:
    """Tests for bitbucket_create_pull_request function."""

    @patch('scripts.bitbucket_pull_requests.get_bitbucket_client')
    def test_create_pr_success(self, mock_get_client, sample_pr_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post.return_value = sample_pr_data

        result = bitbucket_create_pull_request(
            project_key='PROJ',
            repository_slug='test-repo',
            title='Test PR',
            source_branch='feature-branch',
            target_branch='main'
        )
        data = json.loads(result)

        assert data['success'] is True
        assert data['title'] == 'Test PR'

    @patch('scripts.bitbucket_pull_requests.get_bitbucket_client')
    def test_create_pr_with_description(self, mock_get_client, sample_pr_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post.return_value = sample_pr_data

        result = bitbucket_create_pull_request(
            project_key='PROJ',
            repository_slug='test-repo',
            title='Test PR',
            source_branch='feature-branch',
            target_branch='main',
            description='PR description'
        )
        data = json.loads(result)

        assert data['success'] is True

    @patch('scripts.bitbucket_pull_requests.get_bitbucket_client')
    def test_create_pr_with_reviewers(self, mock_get_client, sample_pr_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post.return_value = sample_pr_data

        result = bitbucket_create_pull_request(
            project_key='PROJ',
            repository_slug='test-repo',
            title='Test PR',
            source_branch='feature-branch',
            target_branch='main',
            reviewers=['user1', 'user2']
        )
        data = json.loads(result)

        assert data['success'] is True

    def test_create_pr_missing_project_key(self):
        result = bitbucket_create_pull_request(
            project_key='',
            repository_slug='test-repo',
            title='Test PR',
            source_branch='feature',
            target_branch='main'
        )
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    def test_create_pr_missing_title(self):
        result = bitbucket_create_pull_request(
            project_key='PROJ',
            repository_slug='test-repo',
            title='',
            source_branch='feature',
            target_branch='main'
        )
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestBitbucketGetPullRequest:
    """Tests for bitbucket_get_pull_request function."""

    @patch('scripts.bitbucket_pull_requests.get_bitbucket_client')
    def test_get_pr_success(self, mock_get_client, sample_pr_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = sample_pr_data

        result = bitbucket_get_pull_request('PROJ', 'test-repo', 1)
        data = json.loads(result)

        assert data['id'] == 1
        assert data['title'] == 'Test PR'

    def test_get_pr_missing_project_key(self):
        result = bitbucket_get_pull_request('', 'test-repo', 1)
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    def test_get_pr_missing_pr_id(self):
        result = bitbucket_get_pull_request('PROJ', 'test-repo', 0)
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestBitbucketMergePullRequest:
    """Tests for bitbucket_merge_pull_request function."""

    @patch('scripts.bitbucket_pull_requests.get_bitbucket_client')
    def test_merge_pr_success(self, mock_get_client, sample_pr_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        merged_pr = sample_pr_data.copy()
        merged_pr['state'] = 'MERGED'
        mock_client.post.return_value = merged_pr

        result = bitbucket_merge_pull_request('PROJ', 'test-repo', 1, version=0)
        data = json.loads(result)

        assert data['success'] is True
        assert 'merged' in data['message'].lower()

    @patch('scripts.bitbucket_pull_requests.get_bitbucket_client')
    def test_merge_pr_with_strategy(self, mock_get_client, sample_pr_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post.return_value = sample_pr_data

        result = bitbucket_merge_pull_request(
            'PROJ', 'test-repo', 1, version=0, strategy='squash'
        )
        data = json.loads(result)

        assert data['success'] is True

    def test_merge_pr_invalid_strategy(self):
        result = bitbucket_merge_pull_request(
            'PROJ', 'test-repo', 1, version=0, strategy='invalid'
        )
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    def test_merge_pr_missing_version(self):
        result = bitbucket_merge_pull_request('PROJ', 'test-repo', 1, version=None)
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestBitbucketDeclinePullRequest:
    """Tests for bitbucket_decline_pull_request function."""

    @patch('scripts.bitbucket_pull_requests.get_bitbucket_client')
    def test_decline_pr_success(self, mock_get_client, sample_pr_data):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        declined_pr = sample_pr_data.copy()
        declined_pr['state'] = 'DECLINED'
        mock_client.post.return_value = declined_pr

        result = bitbucket_decline_pull_request('PROJ', 'test-repo', 1, version=0)
        data = json.loads(result)

        assert data['success'] is True
        assert 'declined' in data['message'].lower()

    def test_decline_pr_missing_version(self):
        result = bitbucket_decline_pull_request('PROJ', 'test-repo', 1, version=None)
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestBitbucketAddPrComment:
    """Tests for bitbucket_add_pr_comment function."""

    @patch('scripts.bitbucket_pull_requests.get_bitbucket_client')
    def test_add_comment_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post.return_value = {
            'id': 10001,
            'text': 'Test comment',
            'author': {'name': 'testuser', 'emailAddress': 'test@example.com'},
            'createdDate': 1704067200000,
            'updatedDate': 1704067200000
        }

        result = bitbucket_add_pr_comment('PROJ', 'test-repo', 1, 'Test comment')
        data = json.loads(result)

        assert data['success'] is True
        assert data['text'] == 'Test comment'

    @patch('scripts.bitbucket_pull_requests.get_bitbucket_client')
    def test_add_reply_comment(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post.return_value = {
            'id': 10002,
            'text': 'Reply comment',
            'author': {'name': 'testuser', 'emailAddress': 'test@example.com'},
            'createdDate': 1704067200000,
            'updatedDate': 1704067200000
        }

        result = bitbucket_add_pr_comment(
            'PROJ', 'test-repo', 1, 'Reply comment', parent_id=10001
        )
        data = json.loads(result)

        assert data['success'] is True

    def test_add_comment_missing_text(self):
        result = bitbucket_add_pr_comment('PROJ', 'test-repo', 1, '')
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'


class TestBitbucketGetPrDiff:
    """Tests for bitbucket_get_pr_diff function."""

    @patch('scripts.bitbucket_pull_requests.get_bitbucket_client')
    def test_get_diff_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {
            'diffs': [
                {
                    'source': {'toString': 'src/old.py'},
                    'destination': {'toString': 'src/new.py'},
                    'hunks': []
                }
            ]
        }

        result = bitbucket_get_pr_diff('PROJ', 'test-repo', 1)
        data = json.loads(result)

        assert 'diffs' in data

    def test_get_diff_missing_project_key(self):
        result = bitbucket_get_pr_diff('', 'test-repo', 1)
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'

    def test_get_diff_missing_pr_id(self):
        result = bitbucket_get_pr_diff('PROJ', 'test-repo', 0)
        data = json.loads(result)

        assert data['success'] is False
        assert data['error_type'] == 'ValidationError'
