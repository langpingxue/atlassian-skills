"""Tests for AtlassianCredentials and parameter-based configuration."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'atlassian-skills' / 'scripts'))

import pytest
from _common import (
    AtlassianCredentials,
    AtlassianConfig,
    check_available_skills,
    ConfigurationError
)


class TestAtlassianCredentials:
    """Test AtlassianCredentials dataclass."""
    
    def test_jira_available_with_pat(self):
        """Test Jira is available with PAT token."""
        creds = AtlassianCredentials(
            jira_url="https://jira.company.com",
            jira_pat_token="token123"
        )
        assert creds.is_jira_available() is True
    
    def test_jira_available_with_basic_auth(self):
        """Test Jira is available with username and API token."""
        creds = AtlassianCredentials(
            jira_url="https://company.atlassian.net",
            jira_username="user@company.com",
            jira_api_token="token123"
        )
        assert creds.is_jira_available() is True
    
    def test_jira_unavailable_missing_url(self):
        """Test Jira is unavailable without URL."""
        creds = AtlassianCredentials(
            jira_username="user@company.com",
            jira_api_token="token123"
        )
        assert creds.is_jira_available() is False
    
    def test_jira_unavailable_missing_auth(self):
        """Test Jira is unavailable without authentication."""
        creds = AtlassianCredentials(
            jira_url="https://company.atlassian.net"
        )
        assert creds.is_jira_available() is False
    
    def test_confluence_available(self):
        """Test Confluence availability check."""
        creds = AtlassianCredentials(
            confluence_url="https://confluence.company.com",
            confluence_pat_token="token123"
        )
        assert creds.is_confluence_available() is True
    
    def test_bitbucket_available(self):
        """Test Bitbucket availability check."""
        creds = AtlassianCredentials(
            bitbucket_url="https://bitbucket.company.com",
            bitbucket_pat_token="token123"
        )
        assert creds.is_bitbucket_available() is True
    
    def test_get_available_services_all(self):
        """Test getting all available services."""
        creds = AtlassianCredentials(
            jira_url="https://jira.company.com",
            jira_pat_token="token1",
            confluence_url="https://confluence.company.com",
            confluence_pat_token="token2",
            bitbucket_url="https://bitbucket.company.com",
            bitbucket_pat_token="token3"
        )
        services = creds.get_available_services()
        assert set(services) == {"jira", "confluence", "bitbucket"}
    
    def test_get_available_services_partial(self):
        """Test getting available services with partial configuration."""
        creds = AtlassianCredentials(
            jira_url="https://jira.company.com",
            jira_pat_token="token1"
        )
        services = creds.get_available_services()
        assert services == ["jira"]
    
    def test_get_unavailable_services(self):
        """Test getting unavailable services with reasons."""
        creds = AtlassianCredentials(
            jira_url="https://jira.company.com",
            jira_pat_token="token1"
        )
        unavailable = creds.get_unavailable_services()
        assert "confluence" in unavailable
        assert "bitbucket" in unavailable
        assert "Missing confluence_url" in unavailable["confluence"]
        assert "Missing bitbucket_url" in unavailable["bitbucket"]


class TestAtlassianConfigFromCredentials:
    """Test AtlassianConfig.from_credentials() method."""
    
    def test_from_credentials_jira_pat(self):
        """Test creating Jira config from credentials with PAT."""
        creds = AtlassianCredentials(
            jira_url="https://jira.company.com",
            jira_pat_token="token123"
        )
        config = AtlassianConfig.from_credentials(creds, "jira")
        assert config.url == "https://jira.company.com"
        assert config.pat_token == "token123"
        assert config.auth_type == "pat"
    
    def test_from_credentials_jira_basic(self):
        """Test creating Jira config from credentials with basic auth."""
        creds = AtlassianCredentials(
            jira_url="https://company.atlassian.net",
            jira_username="user@company.com",
            jira_api_token="token123"
        )
        config = AtlassianConfig.from_credentials(creds, "jira")
        assert config.url == "https://company.atlassian.net"
        assert config.username == "user@company.com"
        assert config.api_token == "token123"
        assert config.auth_type == "basic"
    
    def test_from_credentials_confluence(self):
        """Test creating Confluence config from credentials."""
        creds = AtlassianCredentials(
            confluence_url="https://confluence.company.com",
            confluence_pat_token="token123"
        )
        config = AtlassianConfig.from_credentials(creds, "confluence")
        assert config.url == "https://confluence.company.com"
        assert config.pat_token == "token123"
    
    def test_from_credentials_bitbucket(self):
        """Test creating Bitbucket config from credentials."""
        creds = AtlassianCredentials(
            bitbucket_url="https://bitbucket.company.com",
            bitbucket_pat_token="token123"
        )
        config = AtlassianConfig.from_credentials(creds, "bitbucket")
        assert config.url == "https://bitbucket.company.com"
        assert config.pat_token == "token123"
    
    def test_from_credentials_missing_jira(self):
        """Test error when Jira credentials are missing."""
        creds = AtlassianCredentials()
        with pytest.raises(ConfigurationError) as exc_info:
            AtlassianConfig.from_credentials(creds, "jira")
        assert "Jira credentials not provided" in str(exc_info.value)
    
    def test_from_credentials_missing_confluence(self):
        """Test error when Confluence credentials are missing."""
        creds = AtlassianCredentials()
        with pytest.raises(ConfigurationError) as exc_info:
            AtlassianConfig.from_credentials(creds, "confluence")
        assert "Confluence credentials not provided" in str(exc_info.value)
    
    def test_from_credentials_invalid_service(self):
        """Test error with invalid service name."""
        creds = AtlassianCredentials(
            jira_url="https://jira.company.com",
            jira_pat_token="token123"
        )
        with pytest.raises(ConfigurationError) as exc_info:
            AtlassianConfig.from_credentials(creds, "invalid")
        assert "Unknown service" in str(exc_info.value)
    
    def test_from_credentials_with_ssl_verify(self):
        """Test SSL verify flag is passed through."""
        creds = AtlassianCredentials(
            jira_url="https://jira.company.com",
            jira_pat_token="token123",
            jira_ssl_verify=True
        )
        config = AtlassianConfig.from_credentials(creds, "jira")
        assert config.ssl_verify is True
    
    def test_from_credentials_with_api_version(self):
        """Test API version is passed through."""
        creds = AtlassianCredentials(
            jira_url="https://jira.company.com",
            jira_pat_token="token123",
            jira_api_version="3"
        )
        config = AtlassianConfig.from_credentials(creds, "jira")
        assert config.api_version == "3"


class TestCheckAvailableSkills:
    """Test check_available_skills() helper function."""
    
    def test_all_services_available(self):
        """Test when all services are available."""
        creds = AtlassianCredentials(
            jira_url="https://jira.company.com",
            jira_pat_token="token1",
            confluence_url="https://confluence.company.com",
            confluence_pat_token="token2",
            bitbucket_url="https://bitbucket.company.com",
            bitbucket_pat_token="token3"
        )
        result = check_available_skills(creds)
        assert set(result["available_services"]) == {"jira", "confluence", "bitbucket"}
        assert result["unavailable_services"] == {}
    
    def test_partial_services_available(self):
        """Test when only some services are available."""
        creds = AtlassianCredentials(
            jira_url="https://jira.company.com",
            jira_pat_token="token1"
        )
        result = check_available_skills(creds)
        assert result["available_services"] == ["jira"]
        assert "confluence" in result["unavailable_services"]
        assert "bitbucket" in result["unavailable_services"]
    
    def test_no_services_available(self):
        """Test when no services are available."""
        creds = AtlassianCredentials()
        result = check_available_skills(creds)
        assert result["available_services"] == []
        assert len(result["unavailable_services"]) == 3
