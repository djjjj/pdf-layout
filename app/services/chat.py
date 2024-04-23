from loguru import logger

from app.model.res import UserChatMessage, \
    GetUserChatHistoryOutput
from app.model.entity import Context
from app.model.res import GetAiChatResponseOutput, GetChatStatusTodayOutput
from app.model.req import GetAiChatResponseInput, GetUserChatHistoryInput, GetChatStatusTodayInput
from app.model.table import MessageRoleType, Message
from app.error import MessageLimitedInDailyError, MessageLimitedIn30SecondsError
from app.providers import Providers
from app.services.shared import ServicesShared


class ChatService:
    def __init__(self, context: Context, providers: Providers):
        self.ctx = context
        self.pvd = providers
        self.shared = ServicesShared(context, providers)

    async def get_ai_chat_response(self, req: GetAiChatResponseInput) -> GetAiChatResponseOutput:
        if await self.pvd.chat.check_user_message_limited_in_30_seconds(self.ctx.user.id):
            raise MessageLimitedIn30SecondsError()
        if await self.pvd.chat.check_user_message_limited_in_daily(self.ctx.user.id):
            raise MessageLimitedInDailyError()

        request_content = req.message
        response_content = await self.pvd.openrouter.chat(content=request_content)
        user_message = Message(
            user_id=self.ctx.user.id,
            type=MessageRoleType.User,
            text=request_content,
            created_by=self.ctx.user.id,
        )
        ai_message = Message(
            user_id=self.ctx.user.id,
            type=MessageRoleType.Ai,
            text=response_content,
            created_by=self.ctx.user.id,
        )
        messages = [user_message, ai_message]
        count = await self.pvd.chat.add_chat_message(messages=messages)
        logger.debug(f"Added {count} chat messages")
        res = GetAiChatResponseOutput(response=response_content)
        return res

    async def get_user_chat_history(self, last_n: int) -> GetUserChatHistoryOutput:
        messages = await self.pvd.chat.get_user_chat_messages(user_id=self.ctx.user.id, limit=last_n)
        res = []
        for message in messages:
            res.append(UserChatMessage(type=message.type.value, text=message.text))
        return res

    async def get_chat_status_today(self) -> GetChatStatusTodayOutput:
        count = await self.pvd.chat.get_user_chat_messages_count_today(user_id=self.ctx.user.id)
        res = GetChatStatusTodayOutput(user_name=self.ctx.user.name, chat_cnt=count)
        return res
