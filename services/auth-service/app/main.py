from fastapi import FastAPI

from app.core.config import Config
from app.db.base import Base
from app.db.session import engine
from app.api.users import router as users_router
from app.api.auth import router as auth_router

cfg = Config()

app = FastAPI(
    title=cfg.APP_NAME,
    debug=cfg.DEBUG,
    root_path=cfg.ROOT_PATH,
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "ok", "service": cfg.APP_NAME}

app.include_router(users_router, prefix="/api")
app.include_router(auth_router, prefix="/api")

