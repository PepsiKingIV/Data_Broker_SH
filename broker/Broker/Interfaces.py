import abc
from datetime import datetime

from schemas import Operation, Assets_type, Asset, Payment_date, SuperUser, UsersToken


class IBrokerDataAdapter:
    broker_token: str

    @abc.abstractmethod
    def get_asset_cost(self, figi: str, asset_type: Assets_type) -> float: ...

    @abc.abstractmethod
    def get_assets(self) -> list[Asset]: ...

    @abc.abstractmethod
    def get_operations(
        self, date_from: datetime, date_to: datetime
    ) -> list[Operation]: ...

    @abc.abstractmethod
    def get_payment_date(
        self, date_from: datetime, date_to: datetime, figi: str
    ) -> Payment_date: ...


class IRecorder:
    _users: list[UsersToken]
    _cookies: dict = None
    _authorization_url: str
    _post_operation_url: str
    _post_asset_url: str
    _get_tokens_url: str
    _super_user: SuperUser

    @abc.abstractmethod
    def authorization(self) -> None: ...

    @abc.abstractmethod
    def get_tokens(self) -> list[UsersToken]: ...

    @abc.abstractmethod
    def set_positions(self, user: UsersToken, open_positions: list[Asset]) -> None: ...

    @abc.abstractmethod
    def set_operation(
        self, user: UsersToken, operations_in_last_hour: list[Operation]
    ) -> None: ...
