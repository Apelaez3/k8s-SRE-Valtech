from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    APP_NAME: str = "Auth Service"
    DEBUG: bool = False

    ROOT_PATH: str = "/auth"

    DB_DIR: str = "/data"
    DB_NAME: str = "users.db"
    JWT_SECRET: str = "change-me"
    JWT_ALG: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    @property
    def db_url(self) -> str:
        return f"sqlite:///{self.DB_DIR}/{self.DB_NAME}"

    class Config:
        env_file = ".env"


