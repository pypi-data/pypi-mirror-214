from typing import Callable
from bittrade_luno_websocket.models.rest.fee import FeeInformation
from bittrade_luno_websocket.connection.http import prepare_request, send_request
from bittrade_luno_websocket.models import RequestMessage
from bittrade_luno_websocket.models import endpoints
import reactivex


def get_fee_info_http_factory(
    add_token: Callable,
) -> Callable[[str], reactivex.Observable[FeeInformation]]:
    def get_fee_info_http(pair: str) -> reactivex.Observable[FeeInformation]:
        return send_request(
            add_token(
                prepare_request(
                    RequestMessage(
                        method="GET",
                        endpoint=endpoints.Endpoints.GET_FEE_INFORMATION,
                        params={"pair": pair},
                    )
                )
            )
        )

    return get_fee_info_http
