from pydantic.errors import EmailError
from pydantic import BaseModel, validator, validate_email


class AuthModel(BaseModel):
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str

    @validator("email")
    def validate_email(cls, email: str):
        try:
            val = validate_email(email)
        except EmailError:
            raise ValueError("invalid_email")
        return val[1]  # Email


class CreateUser(UserBase):
    password: str

    @validator("password")
    def validate_password(cls, password: str):
        special_sym = ["$", "@", "#", "%", "^"]
        if len(password) < 8:
            raise ValueError("invalid_password")
        if len(password) > 20:
            raise ValueError("invalid_password")
        if not any(char.isdigit() for char in password):
            raise ValueError("invalid_password")
        if not any(char.isupper() for char in password):
            raise ValueError("invalid_password")
        if not any(char.islower() for char in password):
            raise ValueError("invalid_password")
        if not any(char in special_sym for char in password):
            raise ValueError("invalid_password")
        return password


class CheckUser(UserBase):
    password: str

    @validator("password")
    def encode_password(cls, password: str):
        return password.encode("utf8")


class CheckToken(BaseModel):
    token: str

    @validator("token")
    def check_token_type(cls, token: str):
        _type, token = token.split(" ")
        if _type != "Bearer":
            raise ValueError("invalid_token")
        return token
