
from mcp.server import MCPServer
from mcp.server.transport_security import TransportSecuritySettings

from .auth0 import OAuthTokenVerifier, auth_settings


# Create MCP server with authentication
mcp = MCPServer(
    "MCP Server",
    token_verifier=OAuthTokenVerifier(),
    auth=auth_settings,
)


# Create MCP HTTP application
mcp_app = mcp.streamable_http_app(
    streamable_http_path="/mcp",

    # Secure HTTP access
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,

        # Allowed hosts
        allowed_hosts=[
            "grumbly-importer-amplify.ngrok-free.dev",
            "localhost",
            "127.0.0.1",
        ],

        # Allowed origin
        allowed_origins=[
            "https://grumbly-importer-amplify.ngrok-free.dev",
        ],
    ),
)

