import os

from dotenv import load_dotenv
from fastapi_plugin.fast_api_client import Auth0FastAPI
from auth0_api_python import ApiClient, ApiClientOptions
from mcp.server.auth.provider import AccessToken, TokenVerifier
from pydantic import AnyHttpUrl
from mcp.server.auth.settings import AuthSettings

load_dotenv()


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")

RESOURCE = AUTH0_AUDIENCE


auth0 = Auth0FastAPI(
    domain=AUTH0_DOMAIN,
    audience=AUTH0_AUDIENCE,
)

auth_settings = AuthSettings(
    issuer_url=AnyHttpUrl(f"https://{AUTH0_DOMAIN}/"),
    resource_server_url=AnyHttpUrl(RESOURCE),
    required_scopes=[],
    validate_token_resource=True,
)

class OAuthTokenVerifier(TokenVerifier):

    def __init__(self):
        self.api_client = ApiClient(
            ApiClientOptions(
                domain=AUTH0_DOMAIN,
                audience=AUTH0_AUDIENCE,
            )
        )

    async def verify_token(self, token: str) -> AccessToken | None:
        try:
            claims = await self.api_client.verify_request(
                headers={
                    "authorization": f"Bearer {token}",
                },
                http_method="GET",
                http_url=AUTH0_AUDIENCE,
            )

            return AccessToken(
                token=token,
                client_id=claims.get("azp", claims.get("sub", "")),
                scopes=claims.get("scope", "").split(),
                expires_at=claims.get("exp"),
                resource=AUTH0_AUDIENCE,
                subject=claims.get("sub"),
                claims=claims,
            )

        except Exception:
            return None

        RESOURCE = AUTH0_AUDIENCE

