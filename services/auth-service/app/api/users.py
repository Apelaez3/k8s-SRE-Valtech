from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db=db)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    if user_service.get_user_by_email(email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    if user_service.get_user_by_username(username=user.username):
        raise HTTPException(status_code=400, detail="Username already registered")

    created = user_service.create_user(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=user.hashed_password,
    )
    return created


@router.get("/{username}", response_model=UserRead)
def get_user(username: str, user_service: UserService = Depends(get_user_service)):
    user = user_service.get_user_by_username(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
