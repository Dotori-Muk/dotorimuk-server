import asyncio
import httpx
from datetime import datetime
from threading import Thread
from json import dumps
from core.config import settings
import redis


class BackgroundApply(Thread):
    def __init__(self, apply_type, apply_time):
        self.apply_type = apply_type
        self.apply_time = apply_time
        self.db = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        super().__init__()

    async def request_apply(self, dict):
        url = settings.APPLY_URL[self.apply_type]
        settings.header["authorization"] = dict["access_token"]

        async with httpx.AsyncClient() as client:
            for _ in range(10):
                r = await client.put(url, headers=settings.header)
                if "success" in r.text:
                    print(f"{dict['email']} 성공")
                    return
                else:
                    print(f"{dict['email']} 실패, 응답 : {r.text}")

    async def apply(self):
        apply_db = []

        for i in [i.decode() for i in self.db.lrange(self.apply_type, 0, -1)]:
            apply_db.append({"access_token": self.db.get(i), "email": i})

        await asyncio.gather(*[self.request_apply(i) for i in apply_db])

    def run(self):
        loop = asyncio.new_event_loop()

        while True:
            dt = datetime.now()
            if (dt.hour, dt.minute) == self.apply_time:
                loop.run_until_complete(self.apply())
                break
        loop.close()

        if self.apply_type == "massage":
            self.db.flushall()
