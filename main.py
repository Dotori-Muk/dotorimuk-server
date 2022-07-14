from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.api import router
from background_apply import BackgroundApply
from core.data import db

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
    sst = BackgroundApply(db.users, "selfstudy", (20, 00))
    mt = BackgroundApply(db.users, "massage", (20, 20))
    sst.start()
    mt.start()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
