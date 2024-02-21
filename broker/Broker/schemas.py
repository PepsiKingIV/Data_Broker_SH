from enum import Enum
from pydantic import BaseModel
from datetime import datetime, timedelta


class Assets_type(Enum):
    SHARE = 1
    BOND = 2
    FUTURE = 3
    CURRENCY = 4
    ETF = 5
    OPTION = 6


class Asset(BaseModel):
    figi: str
    name: str
    asset_type: str
    price: float
    count: int


class Operation(BaseModel):
    figi: str
    name: str
    date: datetime
    count: int
    price: float
    buy: bool


class Payment_date(BaseModel):
    figi: str
    date: datetime
    amount: float


class RequestOperationSuper(BaseModel):
    user_id: int
    buy: bool
    price: float
    figi: str
    count: int
    date: datetime
    justification: str | None = None
    expectations: str | None = None


class UsersAsset(Asset):
    user_id = int


class Urls(BaseModel):
    authorization_url: str
    post_operation_url: str
    post_asset_url: str
    get_tokens_url: str
    get_instrument_list: str


class SuperUser(BaseModel):
    password: str
    email: str


class UsersToken(BaseModel):
    id: int
    tinkoff_invest_token: str
    username: str
