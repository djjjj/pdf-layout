import aioredis
import time


class TokenBucket:

    def __init__(self, redis_uri: str, redis_pool_size: int, bucket_size: int, inc_rate: float):
        self.redis_cli = aioredis.from_url(redis_uri, max_connections=redis_pool_size, decode_responses=True)
        self.bucket_size = bucket_size
        self.inc_rate = inc_rate

    async def get_token(self, user_key: str):
        current_time = time.time()
        bucket_info = await self.redis_cli.hgetall(user_key)
        if len(bucket_info) == 0:
            await self.redis_cli.hset(
                user_key, mapping={
                    "last_update_time": str(current_time), 
                    "token_cnt": str(self.bucket_size - 1)}
            )
            return True
    
        last_update_time = float(bucket_info["last_update_time"])
        time_delta = current_time - last_update_time
        tokens_to_add = int(self.inc_rate * time_delta) 
        token_cnt = int(bucket_info["token_cnt"])
        
        new_token_cnt = min(self.bucket_size, token_cnt + tokens_to_add)
        await self.redis_cli.hset(
                user_key, mapping={
                    "last_update_time": str(current_time), 
                    "token_cnt": str(new_token_cnt - 1 if new_token_cnt > 0 else 0)}
            )
        return True if new_token_cnt > 0 else False


async def test():
    tb = TokenBucket('redis://localhost', 10, 3, 3 / 30.0)
    return await tb.get_token('test')

if __name__ == '__main__':
    import asyncio

    asyncio.run(test())