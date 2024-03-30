from fastapi import APIRouter, FastAPI

from app.models.database import Base, engine
from app.http.controllers.account_summary import account_summary_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
api_router = APIRouter()

api_router.include_router(account_summary_router)

app.include_router(api_router, prefix="/api/v1")
