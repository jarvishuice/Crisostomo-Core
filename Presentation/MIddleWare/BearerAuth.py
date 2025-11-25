from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from Infrastructure.Providers.JwtProvider import JwtProvider

bearer_scheme = HTTPBearer(auto_error=True)

async def require_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    """
    Valida que el token Bearer exista y sea correcto.
    Devuelve el payload del JWT.
    """
    token = credentials.credentials

    try:
        payload = JwtProvider.decode_token(token)

        return token

    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido o expirado: {ex}",
        )
