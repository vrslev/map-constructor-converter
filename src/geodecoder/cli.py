import asyncio
import os
from functools import partial
from pathlib import Path
from typing import Any

import httpx
import typer

from geodecoder.main import get_geojson, get_output_path

app = typer.Typer()
client = httpx.AsyncClient()


async def fetch(client: httpx.AsyncClient, *, url: str) -> Any:
    return (await client.get(url)).json()


@app.command()
def main(input: typer.FileText, output: Path = typer.Argument(Path(get_output_path()))):
    geojson = asyncio.run(
        get_geojson(
            routes=input.read(),
            fetch=partial(fetch, client=client),
            api_key=os.environ["API_KEY"],
        )
    )

    if output.exists():
        os.remove(output)
    with output.open("a+") as f:
        f.write(geojson)
    print("All done!")
