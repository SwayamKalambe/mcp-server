from contextlib import asynccontextmanager

import httpx
from fastapi import Depends, FastAPI
from mcp.server import MCPServer
from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.transport_security import TransportSecuritySettings

from .auth0 import OAuthTokenVerifier, auth0, auth_settings


API_URL = "http://127.0.0.1:8000"

RESOURCE = "https://grumbly-importer-amplify.ngrok-free.dev/mcp"
AUTH0_DOMAIN = "https://dev-wsqvilqh7i6oipwo.us.auth0.com"


# MCP server

mcp = MCPServer(
    "MCP Server",
    token_verifier=OAuthTokenVerifier(),
    auth=auth_settings,
)


def require_scope(scope: str):
    token = get_access_token()

    if token is None:
        raise PermissionError("Authentication required")

    if scope not in token.scopes:
        raise PermissionError(
            f"Client '{token.client_id}' does not have "
            f"required scope '{scope}'"
        )


# Tools

@mcp.tool()
async def get_products():
    """Get all products."""
    require_scope("products:read")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/retrieve-all-products"
        )

    response.raise_for_status()
    return response.json()


@mcp.tool()
async def get_product(product_id: str):
    """Get a product by ID."""
    require_scope("products:read")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/retrieve-product/{product_id}"
        )

    response.raise_for_status()
    return response.json()


@mcp.tool()
async def create_product(
    product_name: str,
    price: int,
    description: str,
    quantity: int,
):
    """Create a new product."""
    require_scope("products:write")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/create-product",
            json={
                "product_name": product_name,
                "price": price,
                "description": description,
                "quantity": quantity,
            },
        )

    response.raise_for_status()
    return response.json()


# Create MCP HTTP endpoint

mcp_app = mcp.streamable_http_app(
    streamable_http_path="/mcp",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[
            "grumbly-importer-amplify.ngrok-free.dev",
            "localhost",
            "127.0.0.1",
        ],
        allowed_origins=[
            "https://grumbly-importer-amplify.ngrok-free.dev",
        ],
    ),
)


# Start/stop MCP with FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp_app.router.lifespan_context(mcp_app):
        yield

# Create FastAPI app
app = FastAPI(
    title="MCP Server",
    lifespan=lifespan,
)


# Tell client: Auth0 protects this MCP

@app.get("/.well-known/oauth-protected-resource")
async def protected_resource_metadata():
    return {
        "resource": RESOURCE,
        "authorization_servers": [AUTH0_DOMAIN],
        "scopes_supported": [
            "products:read",
            "products:write",
        ],
    }


@app.get("/.well-known/oauth-protected-resource/mcp")
async def protected_resource_metadata_mcp():
    return {
        "resource": RESOURCE,
        "authorization_servers": [AUTH0_DOMAIN],
        "scopes_supported": [
            "products:read",
            "products:write",
        ],
    }

# Tell client how to login and get token
@app.get("/.well-known/oauth-authorization-server")
async def oauth_authorization_server():
    return {
        "issuer": f"{AUTH0_DOMAIN}/",
        # Login
        "authorization_endpoint": (
            f"{AUTH0_DOMAIN}/authorize"
            "?audience=https%3A%2F%2Fgrumbly-importer-amplify.ngrok-free.dev%2Fmcp"
        ),

        # Get token
        "token_endpoint": f"{AUTH0_DOMAIN}/oauth/token",

        # Verify token
        "jwks_uri": f"{AUTH0_DOMAIN}/.well-known/jwks.json",

        # OAuth settings
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


# # Test: is the user authenticated?

# @app.get("/auth-test")
# async def auth_test(user=Depends(auth0.require_auth())):
#     return user


# Connect MCP to FastAPI

app.mount("/", mcp_app)