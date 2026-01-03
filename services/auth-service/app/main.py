from fastapi import FastAPI

from app.core.config import Config
from app.db.base import Base
from app.db.session import engine
from app.api.users import router as users_router

app = FastAPI(title=Config().APP_NAME, debug=Config().DEBUG)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "ok", "service": Config().APP_NAME}

app.include_router(users_router, prefix="/api")