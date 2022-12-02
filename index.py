import os
from functools import partial
from typing import Any

import js  # pyright: ignore[reportMissingImports]
from pyodide.http import pyfetch  # pyright: ignore[reportMissingImports]

from geodecoder.main import get_geojson, get_output_path

js: Any
pyfetch: Any


async def fetch(*, url: str) -> Any:
    return await (await pyfetch(url)).json()


js.getOutputPath = get_output_path
js.getGeojson = partial(get_geojson, fetch=fetch, api_key=os.environ["API_KEY"])
