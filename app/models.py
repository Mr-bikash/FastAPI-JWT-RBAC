from typing import Optional
from sqlmodel import SQLModel, Field
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    role: str  # "admin" or "user"

    def verify_password(self, plain_password: str):
        return pwd_context.verify(plain_password, self.hashed_password)

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")