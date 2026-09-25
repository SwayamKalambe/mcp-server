import httpx
from mcp.server import MCPServer
from mcp_server.auth import (
    JWTTokenVerifier,
    auth_settings,
)
from mcp.server.auth.middleware.auth_context import get_access_token
mcp = MCPServer("Mcp Server")


API_URL = "http://127.0.0.1:8000"


def require_scope(scope: str):
    token = get_access_token()

    if token is None:
        raise PermissionError("Authentication required")

    if scope not in token.scopes:
        raise PermissionError(
            f"Client '{token.client_id}' "
            f"does not have required scope '{scope}'"
        )


mcp = MCPServer(
    "MCP Server",
    token_verifier=JWTTokenVerifier(),
    auth=auth_settings,
)

@mcp.tool()
async def get_products():
    """Get all products from the FastAPI API"""
    require_scope("products:read")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/retrieve-all-products"
        )

    response.raise_for_status()
    return response.json()

@mcp.tool()
async def get_product(product_id: str):
    """Get a product by ID"""
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
    """Create a new product"""

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






app = mcp.streamable_http_app()