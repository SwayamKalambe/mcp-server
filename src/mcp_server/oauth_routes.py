from fastapi import APIRouter

from .auth0 import AUTH0_DOMAIN, RESOURCE


router = APIRouter()


# Tell client: How Auth0 protects this MCP
@router.get("/.well-known/oauth-protected-resource")
async def protected_resource_metadata():
    return {
        "resource": RESOURCE,
        "authorization_servers": [f"https://{AUTH0_DOMAIN}/"],
        "scopes_supported": [
            "products:read",
            "products:write",
        ],
    }


# Same OAuth info for /mcp
@router.get("/.well-known/oauth-protected-resource/mcp")
async def protected_resource_metadata_mcp():
    return {
        "resource": RESOURCE,
        "authorization_servers": [f"https://{AUTH0_DOMAIN}/"],
        "scopes_supported": [
            "products:read",
            "products:write",
        ],
    }


# Tell client how to use Auth0
@router.get("/.well-known/oauth-authorization-server")
async def oauth_authorization_server():
    return {
        "issuer": f"https://{AUTH0_DOMAIN}/",

        # User login
        "authorization_endpoint": (
            f"https://{AUTH0_DOMAIN}/authorize"
        ),

        # Get access token
        "token_endpoint": (
            f"https://{AUTH0_DOMAIN}/oauth/token"
        ),

        # Verify token
        "jwks_uri": (
            f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
        ),

        # OAuth flow
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code"],
        "code_challenge_methods_supported": ["S256"],

        # Available permissions
        "scopes_supported": [
            "openid",
            "profile",
            "email",
            "products:read",
            "products:write",
        ],
    }