from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import Config

db_url = Config().db_url

engine = create_engine(
    db_url,
    connect_args={"check_same_thread": False} if db_url.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)