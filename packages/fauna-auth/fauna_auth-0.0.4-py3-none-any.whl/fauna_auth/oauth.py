import json
import logging
import re
from typing import Optional

from fastapi import Request, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jwcrypto import jwt, jwk

from .public_key import FAUNA_PUBLIC_KEY
from .testing import mocked_auth
from .types import Client, ClientType

USER_ID_PATTERN = re.compile(r"^[a-z0-9]{48}$")

public_key = jwk.JWK.from_pem(FAUNA_PUBLIC_KEY.encode())


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


def _is_authorization_mocked(request: Request) -> bool:
    return request.app.state._state.get("authorization_mocked", False)


def _auth(token: str) -> Client:
    client = _parse_token(token)
    if client is None:
        raise credentials_exception

    return client


def get_fauna_client(
    request: Request, token: Optional[str] = Depends(fauna_auth_scheme)
) -> Client:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    if token is None:
        raise credentials_exception

    if _is_authorization_mocked(request):
        logging.warning("Using mocked authorization")
        return mocked_auth(token)
    else:
        return _auth(token)


def get_fauna_user(client: Client = Depends(get_fauna_client)) -> Client:
    if client.client_type != ClientType.User:
        raise HTTPException(status_code=401, detail="Invalid token")
    return client
