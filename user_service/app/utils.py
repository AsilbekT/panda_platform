# auth_app/utils.py

from typing import Dict, Union
# import jwt
from fastapi import HTTPException

SECRET_KEY = "VpwI_yUDuQuhA1VEB0c0f9qki8JtLeFWh3lA5kKvyGnHxKrZ-M59cA"
ALGORITHM = "HS256"


# def verify_jwt_token(token: str) -> Dict[str, Union[str, int]]:
#     """Decode and verify a JWT token."""
#     return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
