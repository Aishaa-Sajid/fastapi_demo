from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import auth_api, user_api
from src.routes import healthcheck_api


async def lifespan(app: FastAPI):
    # Startup
    yield  # App runs here


# Initialize the FastAPI app
app = FastAPI(title="Blog Post", version="1.0.0", lifespan=lifespan)

# allow cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=healthcheck_api.router, prefix="/health")
app.include_router(router=auth_api.router, prefix="/auth")
app.include_router(router=user_api.router, prefix="/auth")
