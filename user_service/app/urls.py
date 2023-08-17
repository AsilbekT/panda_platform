# urls.py

from fastapi import APIRouter
from . import views

router = APIRouter()

router.add_api_route(
    path="/users",
    endpoint=views.create_profile,
    methods=['POST']
)

router.add_api_route(
    path="/users",
    endpoint=views.get_profile,
    methods=['GET']
)

router.add_api_route(
    path="/users",
    endpoint=views.update_profile,
    methods=['PUT']
)

router.add_api_route(
    path="/users",
    endpoint=views.delete_profile,
    methods=['DELETE']
)
