from pydantic import BaseSettings


class Settings(BaseSettings):
    SIGNIN_URL = "https://server-v2.dotori-gsm.com/v2/auth"
    APPLY_URL = {
        "selfstudy": "https://server-v2.dotori-gsm.com/v2/member/self-study",
        "massage": "https://server-v2.dotori-gsm.com/v2/member/massage",
    }
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        "origin": "https://www.dotori-gsm.com",
        "referer": "https://www.dotori-gsm.com/",
    }

    REDIS_HOST = "redis"
    REDIS_PORT = 6379


settings = Settings()
