from typing import Any

from app.model.entity import Context
from app.providers import Providers
from app.services.chat import ChatService


class Services:
    def __init__(self, context: Context, providers: Providers):
        self.ctx = context
        self.pvd = providers

    @property
    def chat(self):
        return ChatService(self.ctx, self.pvd)
