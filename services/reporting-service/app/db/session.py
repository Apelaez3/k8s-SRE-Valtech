from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import Config

cfg = Config()

engine = create_engine(
    cfg.db_url,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
