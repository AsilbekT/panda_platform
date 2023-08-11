from fastapi import FastAPI
from app import urls

app = FastAPI()

# Include the URLs from the urls.py module
app.include_router(urls.router)
