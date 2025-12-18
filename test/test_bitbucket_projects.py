"""Tests for bitbucket_projects.py."""

import json
import pytest
from unittest.mock import patch, MagicMock

import sys
from pathlib import Path
_base_path = Path(__file__).parent.parent
sys.path.insert(0, str(_base_path / 'atlassian-skills'))
sys.path.insert(0, str(_base_path / 'atlassian-skills' / 'scripts'))

from scripts.bitbucket_projects import bitbucket_list_projects, bitbucket_list_repositories


class TestBitbucketListProjects:
    """Tests for bitbucket_list_projects function."""

    @patch('scripts.bitbucket_projects.get_bitbucket_client')
    def test_list_projects_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {
            'values': [
                {
                    'key': 'PROJ',
                    'name': 'Project One',
                    'description': 'First project',
                    'public': False,
                    'type': 'NORMAL'
                },
                {
                    'key': 'TEST',
                    'name': 'Test Project',
                    'description': 'Test project',
                    'public': True,
                    'type': 'NORMAL'
                }
            ],
            'isLastPage': True,
            'nextPageStart': None
        }

        result = bitbucket_list_projects()
        data = json.loads(result)

        assert len(data['projects']) == 2
        assert data['projects'][0]['key'] == 'PROJ'

    @patch('scripts.bitbucket_projects.get_bitbucket_client')
    def test_list_projects_with_pagination(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {
            'values': [],
            'isLastPage': False,
            'nextPageStart': 25
        }

        result = bitbucket_list_projects(limit=25, start=0)
        data = json.loads(result)

        assert data['is_last_page'] is False
        assert data['next_page_start'] == 25


class TestBitbucketListRepositories:
    """Tests for bitbucket_list_repositories function."""

    @patch('scripts.bitbucket_projects.get_bitbucket_client')
    def test_list_repositories_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {
            'values': [
                {
                    'slug': 'repo-one',
                    'name': 'Repository One',
                    'description': 'First repository',
                    'project': {'key': 'PROJ', 'name': 'Project One'},
                    'public': False,
                    'state': 'AVAILABLE',
                    'forkable': True
                }
            ],
            'isLastPage': True,
            'nextPageStart': None
        }

        result = bitbucket_list_repositories()
        data = json.loads(result)

        assert len(data['repositories']) == 1
        assert data['repositories'][0]['slug'] == 'repo-one'

    @patch('scripts.bitbucket_projects.get_bitbucket_client')
    def test_list_repositories_by_project(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {
            'values': [
                {
                    'slug': 'project-repo',
                    'name': 'Project Repository',
                    'description': '',
                    'project': {'key': 'PROJ', 'name': 'Project One'},
                    'public': False,
                    'state': 'AVAILABLE',
                    'forkable': True
                }
            ],
            'isLastPage': True,
            'nextPageStart': None
        }

        result = bitbucket_list_repositories(project_key='PROJ')
        data = json.loads(result)

        assert len(data['repositories']) == 1
        assert data['repositories'][0]['project_key'] == 'PROJ'

    @patch('scripts.bitbucket_projects.get_bitbucket_client')
    def test_list_repositories_with_pagination(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = {
            'values': [],
            'isLastPage': False,
            'nextPageStart': 50
        }

        result = bitbucket_list_repositories(limit=25, start=25)
        data = json.loads(result)

        assert data['is_last_page'] is False
        assert data['next_page_start'] == 50
