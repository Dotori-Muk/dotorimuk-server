from fastapi import APIRouter, status, HTTPException, Depends
from core.config import settings
from schemas.register import ApplyRequest, ApplyListResponse, ApplyResponse
from db.session import get_redis_db
import httpx

router = APIRouter()


@router.get("/", response_model=ApplyListResponse)
def read_list(apply_type: str, db=Depends(get_redis_db)):
    if apply_type not in ["selfstudy", "massage"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="잘못된 신청 타입입니다.")

    return {"apply_list": [i.decode() for i in db.lrange(apply_type, 0, -1)]}


@router.post("/")
async def apply(req: ApplyRequest, db=Depends(get_redis_db)):

    if req.apply_type not in ["selfstudy", "massage"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="잘못된 신청 타입입니다.")

    if req.email in [i.decode() for i in db.lrange(req.apply_type, 0, -1)]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 신청되었습니다.")

    res = httpx.post(
        url=settings.SIGNIN_URL, json={"email": req.email, "password": req.password}, headers=settings.header
    )

    if res.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="아이디 또는 비밀번호가 잘못되었습니다.")

    db.lpush(req.apply_type, req.email)
    db.set(req.email, res.json()["accessToken"])

    return {"message": "Success"}


@router.delete("/")
async def apply(req: ApplyRequest, db=Depends(get_redis_db)):

    if req.apply_type not in ["selfstudy", "massage"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="잘못된 신청 타입입니다.")

    if req.email not in [i.decode() for i in db.lrange(req.apply_type, 0, -1)]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="신청되지 않았습니다.")

    db.lrem(req.apply_type, 0, req.email)

    return {"message": "Success"}
