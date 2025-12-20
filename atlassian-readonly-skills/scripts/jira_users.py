"""Jira user management tools.

Tools:
    - jira_get_user_profile: Get user profile by identifier
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from typing import Any, Dict

from _common import (
    get_jira_client,
    format_json_response,
    format_error_response,
    ConfigurationError,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    APIError,
    NetworkError,
)


def _simplify_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Simplify user data to essential fields."""
    return {
        'account_id': user_data.get('accountId', ''),
        'display_name': user_data.get('displayName', ''),
        'email': user_data.get('emailAddress', ''),
        'active': user_data.get('active', False),
        'account_type': user_data.get('accountType', ''),
        'timezone': user_data.get('timeZone', ''),
        'locale': user_data.get('locale', '')
    }


def jira_get_user_profile(user_identifier: str) -> str:
    """Get Jira user profile by identifier.
    
    Args:
        user_identifier: User identifier (email, account ID, username, or key)
    
    Returns:
        JSON string with user profile data or error information
    """
    try:
        client = get_jira_client()
        
        if not user_identifier:
            raise ValidationError('user_identifier is required')
        
        # Try different lookup methods
        user_data = None
        
        # Method 1: Try as account ID
        try:
            params = {'accountId': user_identifier}
            user_data = client.get(client.api_path('user'), params=params)
        except (NotFoundError, APIError):
            pass
        
        # Method 2: Try user search by query
        if not user_data:
            try:
                params = {'query': user_identifier, 'maxResults': 1}
                response = client.get(client.api_path('user/search'), params=params)
                if response and len(response) > 0:
                    user_data = response[0]
            except (NotFoundError, APIError):
                pass
        
        # Method 3: Try user picker
        if not user_data:
            try:
                params = {'query': user_identifier, 'maxResults': 1}
                response = client.get(client.api_path('user/picker'), params=params)
                users = response.get('users', [])
                if users:
                    account_id = users[0].get('accountId')
                    if account_id:
                        params = {'accountId': account_id}
                        user_data = client.get(client.api_path('user'), params=params)
            except (NotFoundError, APIError):
                pass
        
        if not user_data:
            raise NotFoundError(f'User not found: {user_identifier}')
        
        simplified = _simplify_user(user_data)
        return format_json_response(simplified)
        
    except ConfigurationError as e:
        return format_error_response('ConfigurationError', str(e))
    except AuthenticationError as e:
        return format_error_response('AuthenticationError', str(e))
    except ValidationError as e:
        return format_error_response('ValidationError', str(e))
    except NotFoundError as e:
        return format_error_response('NotFoundError', str(e))
    except (APIError, NetworkError) as e:
        return format_error_response(type(e).__name__, str(e))
    except Exception as e:
        return format_error_response('UnexpectedError', f'Unexpected error: {str(e)}')
