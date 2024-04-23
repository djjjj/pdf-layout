from pydantic import BaseModel

from app.model.table import User


class Context(BaseModel):
    user: User
