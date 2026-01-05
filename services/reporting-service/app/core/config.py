from pydantic_settings import BaseSettings

class Config(BaseSettings):
    APP_NAME: str = "Reporting Service"
    DEBUG: bool = False

    ROOT_PATH: str = "/reports"

    DB_DIR: str = "/data"
    DB_NAME: str = "expenses.db"

    @property
    def db_url(self) -> str:
        return f"sqlite:///{self.DB_DIR}/{self.DB_NAME}"
