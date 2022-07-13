from pydantic import BaseModel


class Register(BaseModel):
    email: str
    password: str
    apply_type: str
