import datetime
from typing import Optional

from loguru import logger

from app.database import Database
from app.model.table import User


class UserProvider:

    def __init__(self, db: Database) -> None:
        self.db = db

    async def get_user_by_name(self, user_name: str) -> Optional[User]:
        user = await self.db.user.find_one({"name": user_name})
        if not user:
            user = User(name=user_name)
            res = await self.db.user.insert_one(user.model_dump(by_alias=True))
            user = await self.db.user.find_one({"_id": res.inserted_id})
        logger.debug(f"user: {user}")
        return user
