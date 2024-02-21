from datetime import datetime, timedelta
from tinkoff.invest import Client, InstrumentIdType, OperationState
from schemas import Operation, Assets_type, Asset, Payment_date
from Interfaces import IBrokerDataAdapter


class BrokerDataAdapterTinkoff(IBrokerDataAdapter):
    def __init__(self, broker_token: str) -> None:
        self.broker_token = broker_token
        self.__enter__()
        self.id_list = [
            item.id
            for item in self.client.users.get_accounts().accounts
            if item.name != "Инвесткопилка"
        ]
        self.assets_dict = {
            "share": self.client.instruments.share_by,
            "bond": self.client.instruments.bond_by,
            "currency": self.client.instruments.currency_by,
            "etf": self.client.instruments.etf_by,
            "future": self.client.instruments.future_by,
            "option": self.client.instruments.option_by,
        }

    def __enter__(self):
        self.client = Client(self.broker_token).__enter__()

    def get_total_assets_cost(self) -> float:
        total_amount = 0
        for item in self.id_list:
            try:
                for elem in self.client.operations.get_portfolio(
                    account_id=item
                ).positions:
                    total_amount = (
                        total_amount
                        + (elem.current_price.units + elem.current_price.nano / (10**9))
                        * elem.quantity.units
                    )
            except:
                raise
        return total_amount

    def get_asset_cost(self, figi: str) -> float:
        try:
            asset = self.client.market_data.get_last_prices(figi=[figi]).last_prices[-1]
        except:
            raise
        return asset.price.units + asset.price.nano / (10**9)

    def get_assets(self) -> list[Asset]:
        assets = []
        for item in self.id_list:
            try:
                for elem in self.client.operations.get_portfolio(
                    account_id=item
                ).positions:
                    asset = self.assets_dict[elem.instrument_type](
                        id_type=InstrumentIdType(1), id=elem.figi
                    ).instrument
                    asset_price = self.get_asset_cost(elem.figi)
                    if asset.name == "Российский рубль":
                        asset_price = 1.0
                    assets.append(
                        Asset(
                            figi=asset.figi,
                            name=asset.name,
                            asset_type=elem.instrument_type,
                            price=asset_price,
                            count=elem.quantity_lots.units,
                        )
                    )
            except:
                raise
        return assets

    def get_operations(
        self,
        date_from: datetime | None = datetime.now() - timedelta(days=120),
        date_to: datetime | None = datetime.now(),
    ) -> list[Operation]:
        operations = []
        for item in self.id_list:
            try:
                for elem in self.client.operations.get_operations(
                    account_id=item,
                    from_=date_from,
                    to=date_to,
                    state=OperationState(2),
                ).operations:
                    asset = self.assets_dict[elem.instrument_type](
                        id_type=InstrumentIdType(1), id=elem.figi
                    ).instrument
                    operations.append(
                        Operation(
                            figi=elem.figi,
                            name=asset.name,
                            date=elem.date,
                            count=elem.quantity,
                            price=elem.price.units + elem.price.nano / (10**9),
                            buy=True if elem.operation_type == 15 else False,
                        )
                    )
            except:
                raise
        return operations

    def get_payment_date(
        self, date_from: datetime, date_to: datetime, figi: str
    ) -> Payment_date:
        data = self.client.instruments.get_dividends(
            figi=figi, _from=date_from, to=date_to
        )
        return Payment_date(
            figi=figi,
            date=data.payment_date,
            amount=data.dividend_net.units + data.dividend_net.nano / (10**9),
        )
