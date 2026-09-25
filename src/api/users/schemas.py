from pydantic import BaseModel, ConfigDict
from uuid import UUID


class CreateUserRequest(BaseModel):
    name: str
    password: str
    scope: str = "products:read"


class UserResponse(BaseModel):
    user_id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    name: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"