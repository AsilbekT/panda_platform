# urls.py

from fastapi import APIRouter
from . import views
from .schemas import UserProfileResponse

router = APIRouter()

# router.post("/users", response_model=UserProfileResponse)(views.create_profile)
# router.get("/users/{id}",
#            response_model=UserProfileResponse)(views.get_profile)
# router.put("/users/{id}",
#            response_model=UserProfileResponse)(views.update_profile)
# router.delete("/users/{id}")(views.delete_profile)
router.add_api_route(
    path='/users', endpoint=views.create_profile, methods=["POST"])
