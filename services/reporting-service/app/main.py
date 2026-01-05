from fastapi import FastAPI

from app.core.config import Config
from app.api.reports import router as reports_router

cfg = Config()

app = FastAPI(
    title=cfg.APP_NAME,
    debug=cfg.DEBUG,
    root_path=cfg.ROOT_PATH,  # /reports
)

@app.get("/")
def root():
    return {"status": "ok", "service": cfg.APP_NAME}

# 👇 SIN prefijo
app.include_router(reports_router)

