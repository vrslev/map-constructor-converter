import sys
from typing import Any, Protocol


class GetCoordinates(Protocol):
    async def __call__(self, *, address: str) -> tuple[str, str]:
        ...


def _build_url(api_key: str, address: str) -> str:
    address = f"Северодвинск, {address}"
    return f"https://geocode-maps.yandex.ru/1.x/?geocode={address}&lang=ru_RU&result=1&apikey={api_key}&format=json"


def _parse_response(response: dict[str, Any]) -> tuple[str, str]:
    if "response" not in response:
        raise Exception(response)
    return response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
        "Point"
    ]["pos"].split(" ")


if sys.platform == "emscripten":
    from pyodide.http import pyfetch

    async def get_coordinates(api_key: str, *, address: str) -> tuple[str, str]:
        response = await pyfetch(_build_url(api_key, address), method="GET")
        return _parse_response(await response.json())

else:
    import httpx

    client = httpx.AsyncClient()

    async def get_coordinates(api_key: str, *, address: str) -> tuple[str, str]:
        response = await client.get(_build_url(api_key, address))
        return _parse_response(response.json())
