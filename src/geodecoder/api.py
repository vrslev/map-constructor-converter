from typing import Any, Protocol


def _build_url(api_key: str, address: str) -> str:
    address = f"Северодвинск, {address}"
    return f"https://geocode-maps.yandex.ru/1.x/?geocode={address}&lang=ru_RU&result=1&apikey={api_key}&format=json"


def _parse_response(response: dict[str, Any]) -> tuple[str, str]:
    if "response" not in response:
        raise Exception(response)
    return response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
        "Point"
    ]["pos"].split(" ")


class GetCoordinates(Protocol):
    async def __call__(self, *, address: str) -> tuple[str, str]:
        ...


class Fetch(Protocol):
    async def __call__(self, *, url: str) -> Any:
        ...


async def get_coordinates(
    fetch: Fetch, api_key: str, *, address: str
) -> tuple[str, str]:
    return _parse_response(await fetch(url=_build_url(api_key, address)))
