from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.api import router
from background_apply import BackgroundApply

app = FastAPI(title="DOTORIMUK")
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    selfstudy_thread = BackgroundApply(apply_type="selfstudy", apply_time=(20, 00))  # 8시 정각에 신청
    massage_thread = BackgroundApply(apply_type="massage", apply_time=(20, 20))  # 8시 20분에 신청
    selfstudy_thread.start()
    massage_thread.start()
