"""Confluence user search tools.

Tools:
    - confluence_search_users: Search for users
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from typing import Any, Dict, Optional

from _common import (
    get_confluence_client,
    format_json_response,
    format_error_response,
    ConfigurationError,
    AuthenticationError,
    ValidationError,
    APIError,
    NetworkError,
)


def _simplify_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Simplify user data to essential fields."""
    return {
        'account_id': user_data.get('accountId', ''),
        'display_name': user_data.get('displayName', ''),
        'email': user_data.get('email', ''),
        'account_type': user_data.get('accountType', ''),
        'profile_picture': user_data.get('profilePicture', {}).get('path', '')
    }


def confluence_search_users(query: str, limit: int = 10) -> str:
    """Search for Confluence users.
    
    Args:
        query: Search query (name or email)
        limit: Maximum number of results (default: 10)
    
    Returns:
        JSON string with list of users or error information
    """
    try:
        client = get_confluence_client()
        
        if not query:
            raise ValidationError('query is required')
        if limit < 0:
            raise ValidationError('limit must be non-negative')
        
        params: Dict[str, Any] = {
            'cql': f'user.fullname ~ "{query}" OR user.email ~ "{query}"',
            'limit': limit
        }
        
        response = client.get('/rest/api/search/user', params=params)
        
        users = response.get('results', [])
        simplified_users = [_simplify_user(u.get('user', u)) for u in users]
        
        result = {
            'users': simplified_users,
            'count': len(simplified_users),
            'query': query
        }
        
        return format_json_response(result)
        
    except ConfigurationError as e:
        return format_error_response('ConfigurationError', str(e))
    except AuthenticationError as e:
        return format_error_response('AuthenticationError', str(e))
    except ValidationError as e:
        return format_error_response('ValidationError', str(e))
    except (APIError, NetworkError) as e:
        return format_error_response(type(e).__name__, str(e))
    except Exception as e:
        return format_error_response('UnexpectedError', f'Unexpected error: {str(e)}')
