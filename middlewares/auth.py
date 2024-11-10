from fastapi import (
    HTTPException, Depends, status
)
from fastapi.security import (
    HTTPBearer, HTTPAuthorizationCredentials,
    HTTPBasic, HTTPBasicCredentials
)

from configs.enviroment import get_environment_variables

env = get_environment_variables()


class TokenAuth(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(TokenAuth, self).__init__(auto_error=auto_error)

    async def __call__(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        if credentials.credentials != env.INTEGRATION_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication credentials",
            )


def basic_auth(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    if credentials.username != env.GRAPHQL_USERNAME or credentials.password != env.GRAPHQL_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"}
        )


token_auth = TokenAuth()
