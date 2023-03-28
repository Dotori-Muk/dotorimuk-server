from pydantic import BaseModel


class ApplyRequest(BaseModel):
    email: str
    password: str
    apply_type: str


class ApplyListResponse(BaseModel):
    apply_list: list


class ApplyResponse(BaseModel):
    message: str
