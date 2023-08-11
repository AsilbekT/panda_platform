from fastapi import FastAPI
from auth_app.urls import router
from auth_app.database import engine, Base


def create_tables():
    Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(router, prefix="/auth")

# Base.metadata.create_all(bind=engine)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
