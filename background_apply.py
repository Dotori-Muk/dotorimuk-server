import asyncio
import httpx
from datetime import datetime
from threading import Thread
from core.config import settings


class BackgroundApply(Thread):
    def __init__(self, db, apply_type, apply_time):
        self.db = db
        self.apply_type = apply_type
        self.apply_time = apply_time
        super().__init__()

    async def request_apply(self, dict):
        url = settings.APPLY_URL[self.apply_type]
        settings.header["authorization"] = dict["access_token"]

        for _ in range(10):
            async with httpx.AsyncClient() as client:
                r = await client.put(url, headers=settings.header).text.json()
                if "success" in r:
                    print(f"{dict['email']} 성공")
                    return

        print(f"{dict['email']} 실패", r["timeStamp"])

    async def apply(self):
        apply_db = [i for i in self.db if i["apply_type"] == self.apply_type]
        await asyncio.gather(*[self.request_apply(i) for i in apply_db])


    def run(self):
        while True:
            dt = datetime.now()
            if (dt.hour, dt.minute) == self.apply_time:
                self.apply()
                break
