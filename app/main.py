from fastapi import FastAPI

from app.core.config import settings
from app.core.database import Base, engine
from app.routers import admin, auth, day_scholar, hosteller

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version="1.0.0")

app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(hosteller.router, prefix=settings.api_v1_prefix)
app.include_router(day_scholar.router, prefix=settings.api_v1_prefix)
app.include_router(admin.router, prefix=settings.api_v1_prefix)


@app.get("/")
def root():
    return {"message": "College Mess Management API is running"}
