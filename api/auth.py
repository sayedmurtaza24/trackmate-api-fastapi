from os import getenv
from firebase_admin import initialize_app
from firebase_admin import credentials, auth
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import UJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.schemas.auth import PostLoginOut, PostLogoutOut

cred = credentials.Certificate("./firebase-admin.json")
initialize_app(cred)

auth_bearer = HTTPBearer(scheme_name="Firebase Session Cookie")

router = APIRouter(prefix="/api/auth", tags=["Login"])


def verifyUser(authorization: HTTPAuthorizationCredentials = Depends(auth_bearer)):
    try:
        session_cookie: str = authorization.credentials
        verified = auth.verify_session_cookie(session_cookie, check_revoked=True)
        
        return verified['email']
    except:
        raise HTTPException(401, "Unauthorized")


@router.post("/login", response_model=PostLoginOut)
def __login(id_token: str):
    try:
        session_cookie = auth.create_session_cookie(id_token, 3 * 24 * 60 * 60)

        message = {'message': 'Login Success'}

        if getenv('DEBUG') == '1':
            response = UJSONResponse({**message, 'token': session_cookie})
        else:
            response = UJSONResponse(message)

        response.set_cookie('Authorization', f'Bearer {session_cookie}')

        return response

    except:
        return UJSONResponse({'message': 'Unauthorized'}, status_code=401)

@router.post("/logout", response_model=PostLogoutOut)
def __logout(authorization: HTTPAuthorizationCredentials = Depends(auth_bearer)):
    try:
        session_cookie = authorization.credentials
        
        verified = auth.verify_session_cookie(session_cookie, check_revoked=True)
        
        auth.revoke_refresh_tokens(verified['uid'])
    
        message = {'message': 'Logout Success'}
        
        response = UJSONResponse(message, 200)

        response.set_cookie('Authorization', '', httponly=True)

        return response

    except:
        return UJSONResponse({'message': 'Unauthorized'}, status_code=401)
