from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    APP_NAME: str = "Expenses Application"
    DEBUG: bool = False
    db_user: str = ""
    db_password: str = ""
    db_name: str = "expenses.db"

    @property
    def db_url(self) -> str:
        return f"sqlite:///{self.db_name}"

    class Config:
        env_file = ".env"