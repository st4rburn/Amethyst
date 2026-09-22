from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from starlette.requests import Request

from .config import CONFIG

oauth: OAuth = OAuth()

# Set up staff realm
if CONFIG.oidc is not None:
    staff_realm = OAuth()

    # authorize_url = authorization_endpoint
    # access_token_url = token_endpoint
    # = revocation_endpoint
    # = end_session_endpoint
    # = userinfo_endpoint
    oauth.register(
        name="staff",
        client_id=CONFIG.oidc.client_id,
        access_token_url=str(CONFIG.oidc.token_endpoint),
        access_token_params=None,
        authorize_url=str(CONFIG.oidc.authorization_endpoint),
        authorize_params=None,
        api_base_url=str(CONFIG.oidc.issuer),
        client_kwargs={"scope": CONFIG.oidc.scopes},
        server_metadata_url=str(CONFIG.oidc.well_known_url),
    )

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login/staff")
async def staff_login(request: Request):
    redirect_uri = request.url_for("staff_auth")
    return await oauth.staff.authorize_redirect(request, redirect_uri, code_challenge_method="S256")


@router.get("/auth/staff")
async def staff_auth(request: Request):
    _token = await oauth.staff.authorize_access_token(request)
    return RedirectResponse(str(CONFIG.site_root))
