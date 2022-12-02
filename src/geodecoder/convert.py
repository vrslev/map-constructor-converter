import asyncio
import itertools
import random
from functools import cache
from typing import Awaitable

from geodecoder.api import GetCoordinates
from geodecoder.geojson import Feature, FeatureCollection, Point, Properties
from geodecoder.routes import Address, PersonName, Routes, TypeOfChecking


@cache
def _get_color_generator():
    colors = [
        "#93cbfa",
        "#4996f7",
        "#3a79c3",
        "#204675",
        "#f8d44e",
        "#f0983f",
        "#d87c36",
        "#db534b",
        "#7cd859",
        "#51aa31",
        "#99a131",
        "#595959",
        "#b3b3b3",
        "#e378cd",
        "#a62ff6",
        "#71401a",
    ]
    shuffled = colors.copy()
    random.shuffle(shuffled)

    def iterator():
        for color in shuffled:
            yield color

    return itertools.cycle(iterator())


def _get_color():
    return next(_get_color_generator())


def build_type_of_checking(t: TypeOfChecking) -> str:
    match t.lower():
        case "ремонт" | "ремонты":
            return "Р"
        case  "подключение"|"подключения":
            return "П"
        case other:
            return other


def build_caption(
    person_name: PersonName, type_of_checking: TypeOfChecking, address_description: str
) -> str:
    last_name = person_name.partition(" ")[-1] or person_name
    apartment = address_description.split()[-1]
    type = build_type_of_checking(type_of_checking)
    return f"{last_name} {type} {apartment}"


async def _build_feature(
    id: int,
    address: Address,
    person_name: PersonName,
    type_of_checking: TypeOfChecking,
    get_coordinates: GetCoordinates,
    color: str,
):
    return Feature(
        id=id,
        geometry=Point(coordinates=await get_coordinates(address=address.description)),
        properties=Properties(
            description=f"{address.description} \n{address.plan_url}",
            iconCaption=build_caption(
                person_name=person_name,
                type_of_checking=type_of_checking,
                address_description=address.description,
            ),
            marker_color=color,  # pyright: ignore
        ),
    )


async def convert_route_file_content_to_geojson(
    routes: Routes, get_coordinates: GetCoordinates
) -> FeatureCollection:
    id = 0
    coros: list[Awaitable[Feature]] = []

    for person_name, person_routes in routes.items():
        color = _get_color()

        for type_of_checking, addresses in person_routes.items():
            for address in addresses:
                coros.append(
                    _build_feature(
                        id=id,
                        address=address,
                        person_name=person_name,
                        type_of_checking=type_of_checking,
                        get_coordinates=get_coordinates,
                        color=color,
                    )
                )
                id += 1

    features: list[Feature] = await asyncio.gather(*coros)
    return FeatureCollection(features=features)
