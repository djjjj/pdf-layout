from contextlib import asynccontextmanager

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from .conf import CONFIG
from .models import User, QAMsg
from .token_bucket import TokenBucket


app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # init mongo client
    mongo_uri = "mongodb://{}:{}@{}:{}/".format(
        CONFIG['mongo']['user'],
        CONFIG['mongo']['password'],
        CONFIG['mongo']['host'],
        CONFIG['mongo']['port'],
    )
    mongo_cli = AsyncIOMotorClient(mongo_uri)
    db_inst = getattr(mongo_cli, CONFIG['mongo']['db'])
    await init_beanie(database=db_inst, document_models=[User, QAMsg])
    app.mongo_cli = mongo_cli

    # init token bucket
    redis_uri = 'redis://{}:{}'.format(
        CONFIG['redis']['host'],
        CONFIG['redis']['port'],   
    )
    app.token_bucket = TokenBucket(redis_uri, 10, 3, 3 / 30.0)

    yield

    app.mongo_cli.close()


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Error):
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)}
    )


@app.exception_handler(Error)
async def error_handler(request: Request, exc: Error):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc)}
    )


@app.post("/api/v1/get_ai_chat_response")
async def get_ai_chat_response(request: Request, req: GetAiChatResponseInput) -> GetAiChatResponseOutput:
    pvd = Providers(db=request.app.db)
    user = await pvd.user.get_user_by_name(req.user_name)
    if not user:
        raise UserNotFoundError(req.user_name)
    ctx = Context(user=user)
    svc = Services(ctx, pvd)
    res = await svc.chat.get_ai_chat_response(req)
    return res


@app.get("/api/v1/get_user_chat_history")
async def get_user_chat_history(request: Request, user_name: str, last_n: int) -> GetUserChatHistoryOutput:
    pvd = Providers(db=request.app.db)
    user = await pvd.user.get_user_by_name(user_name)
    if not user:
        raise UserNotFoundError(user_name)
    ctx = Context(user=user)
    svc = Services(ctx, pvd)
    res = await svc.chat.get_user_chat_history(last_n=last_n)
    return res


@app.get("/api/v1/get_chat_status_today")
async def get_chat_status_today(request: Request, user_name: str) -> GetChatStatusTodayOutput:
    pvd = Providers(db=request.app.db)
    user = await pvd.user.get_user_by_name(user_name)
    if not user:
        raise UserNotFoundError(user_name)
    ctx = Context(user=user)
    svc = Services(ctx, pvd)
    res = await svc.chat.get_chat_status_today()
    return res
