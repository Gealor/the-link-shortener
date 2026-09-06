from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class ResponseSchema(BaseModel):
    msg: str


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nickname: str = Field(examples=["Gealor"])


class UserRead(UserBase):
    id: int
    is_active: bool


class UserRegister(UserBase):
    password: str = Field(min_length=8, examples=["ivan_craft7869"])


class UserRegisterWithRepeatPassword(UserRegister):
    repeat_password: str = Field(examples=["ivan_craft7869"])


class LoginCredentials(BaseModel):
    nickname: str = Field(examples=["Gealor"])
    password: str = Field(examples=["ivan_craft7869"])
