from pydantic import BaseSettings


class Settings(BaseSettings):
    SIGNIN_URL = "https://server.dotori-gsm.com/v1/signin"
    APPLY_URL = {
        "selfstudy": "https://server.dotori-gsm.com/v1/member/selfstudy",
        "massage": "https://server.dotori-gsm.com/v1/member/massage",
    }
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }


settings = Settings()
