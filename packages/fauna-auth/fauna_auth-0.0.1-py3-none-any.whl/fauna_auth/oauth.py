import json
from enum import Enum
from typing import Optional

from fastapi import Request, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jwcrypto import jwt, jwk
from pydantic import BaseModel

from .public_key import FAUNA_PUBLIC_KEY

public_key = jwk.JWK.from_pem(FAUNA_PUBLIC_KEY.encode())


class ClientType(str, Enum):
    User = "user"  # An active user session
    Delegate = "delegate"  # a delegated user session
    App = "app"  # an app session


class Client(BaseModel):
    client_type: ClientType
    client_id: str
    group: Optional[str] = None


class FaunaAuthorizationScheme(OAuth2AuthorizationCodeBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        fauna = request.cookies.get("fauna")
        if fauna is not None:
            return fauna
        return await super().__call__(request)


fauna_auth_scheme = FaunaAuthorizationScheme(authorizationUrl="", tokenUrl="token")


def parse_user_token(token: str) -> Optional[str]:
    try:
        jwt_token = jwt.JWT(
            key=public_key,
            jwt=token,
            check_claims={"exp": None, "iss": "fetch.ai", "sub": None, "iat": None},
        )

        claims = json.loads(jwt_token.claims)
        print('CLAIMS', claims)

        return claims["sub"]

    except jwt.JWException as e:
        return None


def get_fauna_client(token: Optional[str] = Depends(fauna_auth_scheme)) -> Client:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    if token is None:
        raise credentials_exception

    user_id = parse_user_token(token)
    if user_id is None:
        raise credentials_exception

    return Client(
        client_type=ClientType.User,
        client_id=str(user_id),
        group=None,
    )


def get_fauna_user(client: Client = Depends(get_fauna_client)) -> Client:
    if client.client_type != ClientType.User:
        raise HTTPException(status_code=401, detail="Invalid token")
    return client
