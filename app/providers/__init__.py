from app.database import Database
from app.providers.chat import ChatProvider
from app.providers.openrouter import OpenRouterProvider
from app.providers.user import UserProvider


class Providers:

    def __init__(self, db: Database) -> None:
        self.db = db

    @property
    def openrouter(self):
        return OpenRouterProvider(db=self.db)

    @property
    def user(self):
        return UserProvider(db=self.db)

    @property
    def chat(self):
        return ChatProvider(db=self.db)
