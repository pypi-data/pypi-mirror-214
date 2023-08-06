from dataclasses import dataclass
import dataclasses
from typing import Literal, TypedDict


@dataclass
class TransferRequest:
    amount: str
    currency: str
    address: str
    description: str = ""
    message: str = ""
    external_id: str = ""
    destination_tag: int = 0

    def to_dict(self):
        as_dict = dataclasses.asdict(self)
        if self.destination_tag:
            as_dict["has_destination_tag"] = True
        else:
            del as_dict["destination_tag"]

        return as_dict
