import os
from typing import Any

import js  # pyright: ignore[reportMissingImports]

from geodecoder.main import get_geojson, get_output_path

js: Any
js.getGeojson = get_geojson
js.getOutputPath = get_output_path
js.apiKey = "c0d403ab-e5be-4049-908c-8122a58acf23"

