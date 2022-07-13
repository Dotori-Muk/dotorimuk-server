from fastapi import APIRouter, status, HTTPException
from core.data import db
from core.config import settings
from schemas.register import Register
import httpx
router = APIRouter()


@router.get("")
def read_list(apply_type: str):
    """
    query param : selfstudy, message
    \n
    response : ["s21013@gsm.hs.kr", "s21001@gsm.hs.kr"]
    """
    edb = [i for i in db.users if i["apply_type"] == apply_type]
    res = []
    for i in edb:
        settings.header["authorization"] = i["access_token"]
        r = httpx.get("https://server.dotori-gsm.com/v1/home", headers=settings.header).json()
        res.append(r["data"]["memberName"])
    return res


@router.post("")
async def apply(req: Register):
    """
    apply_type : selfstudy or message
    """
    if req.email in [i["email"] for i in db.users]:
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 신청되었습니다.")

    payload = {"email": req.email, "password": req.password}
    r = httpx.post(url=settings.SIGNIN_URL, json=payload, headers=settings.header)

    if r.status_code != 200:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="아이디 또는 비밀번호가 잘못되었습니다.")

    db.users.append(
        {"email": req.email, "access_token": r.json()["data"]["token"]["accessToken"], "apply_type": req.apply_type}
    )

    return {"message": "Success"}
