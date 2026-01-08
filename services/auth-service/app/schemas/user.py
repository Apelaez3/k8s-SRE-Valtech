from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str

    class Config:
        from_attributes = True 