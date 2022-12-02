import json
from datetime import datetime
from functools import partial

from geodecoder.api import Fetch, get_coordinates
from geodecoder.convert import convert_routes_to_geojson
from geodecoder.routes import parse_routes


def get_output_path() -> str:
    return f"{datetime.now():%Y-%m-%d_%H:%M:%S}.geojson"


async def get_geojson(routes: str, fetch: Fetch, api_key: str) -> str:
    return json.dumps(
        (
            await convert_routes_to_geojson(
                routes=parse_routes(routes),
                get_coordinates=partial(get_coordinates, fetch=fetch, api_key=api_key),
            )
        ).dict(by_alias=True),
        ensure_ascii=False,
    )
