from fastapi import APIRouter
from .views import get_active_sessions, logout_session, register, login, logout, verify_token

router = APIRouter()

# Added path as the first argument
router.add_api_route(path='/register', endpoint=register, methods=["POST"])
router.add_api_route(path='/login', endpoint=login,
                     methods=["POST"])
router.add_api_route(path='/logout', endpoint=logout,
                     methods=["POST"])
router.add_api_route(path='/verify-token',
                     endpoint=verify_token, methods=["GET"])
router.add_api_route(path='/sessions/logout',
                     endpoint=logout_session, methods=["POST"])
router.add_api_route(path='/sessions',
                     endpoint=get_active_sessions, methods=["GET"])
