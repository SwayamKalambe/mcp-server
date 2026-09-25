import os
import jwt
from dotenv import load_dotenv
from pydantic import AnyHttpUrl
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
RESOURCE = "http://127.0.0.1:8001/mcp"


class JWTTokenVerifier(TokenVerifier):

    async def verify_token(self, token: str) -> AccessToken | None:
        try:
            payload = jwt.decode(
                token,
                JWT_SECRET,
                algorithms=["HS256"],
            )
        except jwt.InvalidTokenError:
            return None

        return AccessToken(
            token=token,
            client_id=payload["sub"],
            scopes=payload.get("scope", "").split(),
            resource=RESOURCE,
        )


auth_settings = AuthSettings(
    issuer_url=AnyHttpUrl("https://auth.example.com"),
    resource_server_url=AnyHttpUrl(RESOURCE),
    required_scopes=[],
    validate_token_resource=True,
)