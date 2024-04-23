from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_host: str
    mongo_port: str
    mongo_db: str
    mongo_user: str
    mongo_password: str
    redis_host: str 
    redis_port: str
    redis_password: str 
    req_per_day: int 
    req_limit_cnt: int
    req_limit_period: int

    class Config:
        env_file = ".env"