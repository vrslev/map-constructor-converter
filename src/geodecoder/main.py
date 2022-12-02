import json
import os
import sys
from datetime import datetime
from functools import partial
from pathlib import Path

from geodecoder.api import get_coordinates
from geodecoder.convert import convert_route_file_content_to_geojson
from geodecoder.routes import parse_routes


def get_output_path() -> str:
    return f"{datetime.now():%Y-%m-%d_%H:%M:%S}.geojson"


async def get_geojson(api_key: str, content: str) -> str:
    return json.dumps(
        (
            await convert_route_file_content_to_geojson(
                routes=parse_routes(content),
                get_coordinates=partial(get_coordinates, api_key=api_key),
            )
        ).dict(by_alias=True),
        ensure_ascii=False,
    )


if sys.platform != "emscripten":
    import asyncio

    import typer

    app = typer.Typer()

    @app.command()
    def main(
        input: typer.FileText, output: Path = typer.Argument(Path(get_output_path()))
    ):
        geojson = asyncio.run(get_geojson(os.environ["API_KEY"], input.read()))
        if output.exists():
            os.remove(output)
        with output.open("a+") as f:
            f.write(geojson)
        print("All done!")
