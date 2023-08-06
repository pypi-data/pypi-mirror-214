from typing import TypedDict


class FeeInformation(TypedDict):
    maker_fee: str
    taker_fee: str
    thirty_day_volume: str
