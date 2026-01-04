from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    APP_NAME: str = "Expenses Service"
    DEBUG: bool = False

    DB_DIR: str = "/data"
    DB_NAME: str = "expenses.db"

    @property
    def db_url(self) -> str:
        return f"sqlite:///{self.DB_DIR}/{self.DB_NAME}"

    class Config:
        env_file = ".env"

