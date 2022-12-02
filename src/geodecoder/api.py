import sys
from collections import defaultdict
from decimal import Decimal
from functools import cache
from typing import Any, Protocol


def _build_url(api_key: str, address: str) -> str:
    address = f"Северодвинск, {address}"
    return f"https://geocode-maps.yandex.ru/1.x/?geocode={address}&lang=ru_RU&result=1&apikey={api_key}&format=json"


_lat_offsets: dict[Decimal, int] = defaultdict(lambda: -1)
_lon_offsets: dict[Decimal, int] = defaultdict(lambda: -1)


def _offset_coordinates(lat: Decimal, lon: Decimal) -> tuple[Decimal, Decimal]:
    if _lat_offsets[lat] <= _lon_offsets[lon]:
        _lat_offsets[lat] += 1
    else:
        _lon_offsets[lon] += 1

    offset = Decimal(0.0001)
    return lat + _lat_offsets[lat] * offset, lon + _lon_offsets[lon] * offset


def _parse_response(response: dict[str, Any]) -> tuple[str, str]:
    if "response" not in response:
        raise Exception(response)
    lat, lon = response["response"]["GeoObjectCollection"]["featureMember"][0][
        "GeoObject"
    ]["Point"]["pos"].split(" ")
    result = _offset_coordinates(Decimal(lat), Decimal(lon))
    return str(result[0]), str(result[1])


@cache
def get_httpx_client():
    import httpx

    return httpx.AsyncClient()


async def fetch(url: str) -> Any:
    if sys.platform == "emscripten":
        from pyodide.http import pyfetch

        return await (await pyfetch(url)).json()
    else:
        return (await get_httpx_client().get(url)).json()


class GetCoordinates(Protocol):
    async def __call__(self, *, address: str) -> tuple[str, str]:
        ...


async def get_coordinates(api_key: str, *, address: str) -> tuple[str, str]:
    return _parse_response(await fetch(_build_url(api_key, address)))
