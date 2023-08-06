import json
import re
from enum import Enum
from typing import Optional

from fastapi import Request, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jwcrypto import jwt, jwk
from pydantic import BaseModel

from .public_key import FAUNA_PUBLIC_KEY

USER_ID_PATTERN = re.compile(r"^[a-z0-9]{48}$")

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


def _parse_token(token: str) -> Optional[Client]:
    try:
        jwt_token = jwt.JWT(
            key=public_key,
            jwt=token,
            check_claims={"exp": None, "iss": "fetch.ai", "sub": None, "iat": None},
        )

        # parse the claims
        claims = json.loads(jwt_token.claims)

        # extract the elements
        subject = str(claims["sub"])
        group = claims.get("grp")

        # ensure that we match the user id pattern
        if USER_ID_PATTERN.match(subject) is None:
            return None

        return Client(
            client_type=ClientType.User,
            client_id=subject,
            group=group,
        )

    except jwt.JWException as e:
        return None


def get_fauna_client(token: Optional[str] = Depends(fauna_auth_scheme)) -> Client:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    if token is None:
        raise credentials_exception

    client = _parse_token(token)
    if client is None:
        raise credentials_exception

    return client


def get_fauna_user(client: Client = Depends(get_fauna_client)) -> Client:
    if client.client_type != ClientType.User:
        raise HTTPException(status_code=401, detail="Invalid token")
    return client
