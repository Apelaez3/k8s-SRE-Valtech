from typing import Optional
from sqlalchemy.orm import Session

from app.db.models.user import User

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, username: str, email: str, full_name: str, hashed_password: str) -> User:
        new_user = User(
            username=username,
            email=email,
            full_name=full_name,
            hashed_password=hashed_password
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()



    