"""Tests for _common.py utilities."""

import json
import os
import pytest
from unittest.mock import patch, MagicMock

import sys
from pathlib import Path
_base_path = Path(__file__).parent.parent
sys.path.insert(0, str(_base_path / 'atlassian-skills'))
sys.path.insert(0, str(_base_path / 'atlassian-skills' / 'scripts'))

from scripts._common import (
    format_error_response,
    format_json_response,
    parse_time_spent,
    simplify_issue,
    AtlassianConfig,
    AtlassianClient,
    ConfigurationError,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    APIError,
    NetworkError,
)


class TestFormatErrorResponse:
    """Tests for format_error_response function."""

    def test_basic_error(self):
        result = format_error_response("TestError", "Test message")
        data = json.loads(result)
        assert data['success'] is False
        assert data['error'] == "Test message"
        assert data['error_type'] == "TestError"

    def test_error_with_details(self):
        result = format_error_response("TestError", "Test message", "Extra details")
        data = json.loads(result)
        assert data['details'] == "Extra details"

    def test_unicode_support(self):
        result = format_error_response("TestError", "测试消息")
        data = json.loads(result)
        assert data['error'] == "测试消息"


class TestFormatJsonResponse:
    """Tests for format_json_response function."""

    def test_dict_response(self):
        result = format_json_response({'key': 'value'})
        data = json.loads(result)
        assert data['key'] == 'value'

    def test_list_response(self):
        result = format_json_response([1, 2, 3])
        data = json.loads(result)
        assert data == [1, 2, 3]

    def test_unicode_support(self):
        result = format_json_response({'message': '中文测试'})
        data = json.loads(result)
        assert data['message'] == '中文测试'


class TestParseTimeSpent:
    """Tests for parse_time_spent function."""

    def test_hours(self):
        assert parse_time_spent('1h') == 3600
        assert parse_time_spent('2h') == 7200

    def test_minutes(self):
        assert parse_time_spent('30m') == 1800
        assert parse_time_spent('45m') == 2700

    def test_days(self):
        assert parse_time_spent('1d') == 86400

    def test_weeks(self):
        assert parse_time_spent('1w') == 604800

    def test_combined(self):
        assert parse_time_spent('1h 30m') == 5400
        assert parse_time_spent('1d 2h') == 93600

    def test_seconds_format(self):
        assert parse_time_spent('3600s') == 3600

    def test_raw_number(self):
        assert parse_time_spent('3600') == 3600

    def test_empty_raises_error(self):
        with pytest.raises(ValidationError):
            parse_time_spent('')

    def test_invalid_format_raises_error(self):
        with pytest.raises(ValidationError):
            parse_time_spent('invalid')


class TestSimplifyIssue:
    """Tests for simplify_issue function."""

    def test_basic_simplification(self, sample_issue_data):
        result = simplify_issue(sample_issue_data)
        assert result['key'] == 'PROJ-123'
        assert result['summary'] == 'Test Issue'
        assert result['status'] == 'Open'
        assert result['issue_type'] == 'Task'

    def test_assignee_extraction(self, sample_issue_data):
        result = simplify_issue(sample_issue_data)
        assert result['assignee'] == 'assignee@example.com'

    def test_missing_assignee(self, sample_issue_data):
        sample_issue_data['fields']['assignee'] = None
        result = simplify_issue(sample_issue_data)
        assert result['assignee'] is None

    def test_components_extraction(self, sample_issue_data):
        result = simplify_issue(sample_issue_data)
        assert 'Backend' in result['components']


class TestAtlassianConfig:
    """Tests for AtlassianConfig class."""

    def test_pat_auth_type(self):
        config = AtlassianConfig(
            url='https://jira.example.com',
            pat_token='test-token'
        )
        assert config.auth_type == 'pat'

    def test_basic_auth_type(self):
        config = AtlassianConfig(
            url='https://jira.example.com',
            username='user',
            api_token='token'
        )
        assert config.auth_type == 'basic'

    def test_url_trailing_slash_removed(self):
        config = AtlassianConfig(
            url='https://jira.example.com/',
            pat_token='test-token'
        )
        assert config.url == 'https://jira.example.com'

    def test_is_cloud_detection(self):
        cloud_config = AtlassianConfig(
            url='https://company.atlassian.net',
            username='user',
            api_token='token'
        )
        assert cloud_config.is_cloud is True

        server_config = AtlassianConfig(
            url='https://jira.company.com',
            pat_token='token'
        )
        assert server_config.is_cloud is False

    def test_api_version_detection(self):
        cloud_config = AtlassianConfig(
            url='https://company.atlassian.net',
            username='user',
            api_token='token'
        )
        assert cloud_config.detect_api_version() == '3'

        server_config = AtlassianConfig(
            url='https://jira.company.com',
            pat_token='token'
        )
        assert server_config.detect_api_version() == '2'

    def test_explicit_api_version(self):
        config = AtlassianConfig(
            url='https://jira.example.com',
            pat_token='token',
            api_version='3'
        )
        assert config.detect_api_version() == '3'

    def test_get_auth_header_pat(self):
        config = AtlassianConfig(
            url='https://jira.example.com',
            pat_token='test-token'
        )
        header = config.get_auth_header()
        assert header['Authorization'] == 'Bearer test-token'

    def test_get_auth_header_basic(self):
        config = AtlassianConfig(
            url='https://jira.example.com',
            username='user',
            api_token='token'
        )
        header = config.get_auth_header()
        assert 'Basic' in header['Authorization']

    @patch.dict(os.environ, {
        'TEST_URL': 'https://test.example.com',
        'TEST_PAT_TOKEN': 'test-pat'
    })
    def test_from_env(self):
        config = AtlassianConfig.from_env('TEST')
        assert config.url == 'https://test.example.com'
        assert config.pat_token == 'test-pat'

    @patch.dict(os.environ, {}, clear=True)
    def test_from_env_missing_url(self):
        with pytest.raises(ConfigurationError):
            AtlassianConfig.from_env('MISSING')


class TestAtlassianClient:
    """Tests for AtlassianClient class."""

    def test_api_path(self):
        config = AtlassianConfig(
            url='https://jira.example.com',
            pat_token='token'
        )
        client = AtlassianClient(config)
        assert client.api_path('issue/TEST-1') == '/rest/api/2/issue/TEST-1'

    def test_api_path_strips_leading_slash(self):
        config = AtlassianConfig(
            url='https://jira.example.com',
            pat_token='token'
        )
        client = AtlassianClient(config)
        assert client.api_path('/issue/TEST-1') == '/rest/api/2/issue/TEST-1'

    @patch('requests.Session')
    def test_get_request(self, mock_session_class):
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'key': 'value'}
        mock_response.content = b'{"key": "value"}'
        mock_session.get.return_value = mock_response

        config = AtlassianConfig(
            url='https://jira.example.com',
            pat_token='token'
        )
        client = AtlassianClient(config)
        result = client.get('/test')
        assert result == {'key': 'value'}

    @patch('requests.Session')
    def test_handle_401_error(self, mock_session_class):
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {'message': 'Unauthorized'}
        mock_session.get.return_value = mock_response

        config = AtlassianConfig(
            url='https://jira.example.com',
            pat_token='token'
        )
        client = AtlassianClient(config)
        with pytest.raises(AuthenticationError):
            client.get('/test')

    @patch('requests.Session')
    def test_handle_404_error(self, mock_session_class):
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'message': 'Not found'}
        mock_session.get.return_value = mock_response

        config = AtlassianConfig(
            url='https://jira.example.com',
            pat_token='token'
        )
        client = AtlassianClient(config)
        with pytest.raises(NotFoundError):
            client.get('/test')
