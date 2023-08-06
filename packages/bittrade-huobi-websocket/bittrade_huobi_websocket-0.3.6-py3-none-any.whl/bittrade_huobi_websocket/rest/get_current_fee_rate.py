from typing import Callable, cast
from bittrade_huobi_websocket.models import RequestMessage, endpoints
from bittrade_huobi_websocket.rest.http_factory_decorator import http_factory

from returns import maybe


@http_factory
def get_current_fee_rate_http_factory(symbols: list[str] | str):
    return RequestMessage(
        "GET",
        endpoints.HuobiEndpoints.V2_GET_CURRENT_FEE_RATE,
        params={"symbols": symbols if isinstance(symbols, str) else ",".join(symbols)},
    )
