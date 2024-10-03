from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError

from typing import Annotated
from .schemas import TokenData 
from . import token

# "login" is the route where it will get the jwt token 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token_str: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token.verify_token(token_str, credentials_exception)



