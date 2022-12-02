import asyncio
import itertools
import random
from collections import defaultdict
from decimal import Decimal
from typing import Awaitable, ClassVar

from geodecoder.api import GetCoordinates
from geodecoder.geojson import Feature, FeatureCollection, Point, Properties
from geodecoder.routes import Address, PersonName, Routes, TypeOfChecking


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
    return itertools.cycle(shuffled)


def _build_type_of_checking(t: TypeOfChecking) -> str:
    match t.lower():
        case "ремонт" | "ремонты":
            return "Р"
        case "подключение" | "подключения":
            return "П"
        case other:
            return other


def _build_caption(
    person_name: PersonName, type_of_checking: TypeOfChecking, address_description: str
) -> str:
    last_name = person_name.partition(" ")[-1] or person_name
    apartment = address_description.split()[-1]
    type = _build_type_of_checking(type_of_checking)
    return f"{last_name} {type} {apartment}"


class _Offsetter:
    offset: ClassVar[Decimal] = Decimal(0.0001)

    def __init__(self) -> None:
        self.lat_offsets: dict[Decimal, int] = defaultdict(lambda: -1)
        self.lon_offsets: dict[Decimal, int] = defaultdict(lambda: -1)

    def call_with_decimals(self, lat: Decimal, lon: Decimal) -> tuple[Decimal, Decimal]:
        if self.lat_offsets[lat] <= self.lon_offsets[lon]:
            self.lat_offsets[lat] += 1
        else:
            self.lon_offsets[lon] += 1

        return (
            lat + self.lat_offsets[lat] * self.offset,
            lon + self.lon_offsets[lon] * self.offset,
        )

    def __call__(self, lat: str, lon: str) -> tuple[str, str]:
        lat_d, lon_d = self.call_with_decimals(Decimal(lat), Decimal(lon))
        return str(lat_d), str(lon_d)


async def _build_feature(
    id: int,
    address: Address,
    person_name: PersonName,
    type_of_checking: TypeOfChecking,
    color: str,
    get_coordinates: GetCoordinates,
    offset_coordinates: _Offsetter,
) -> Feature:
    coordinates = offset_coordinates(
        *await get_coordinates(address=address.description)
    )
    description = f"{address.description} \n{address.plan_url}"
    caption = _build_caption(
        person_name=person_name,
        type_of_checking=type_of_checking,
        address_description=address.description,
    )
    return Feature(
        id=id,
        geometry=Point(coordinates=coordinates),
        properties=Properties(
            description=description,
            iconCaption=caption,
            marker_color=color,  # pyright: ignore
        ),
    )


async def convert_routes_to_geojson(
    routes: Routes, get_coordinates: GetCoordinates
) -> FeatureCollection:
    offsetter = _Offsetter()
    color_generator = _get_color_generator()
    id = 0
    coros: list[Awaitable[Feature]] = []

    for person_name, person_routes in routes.items():
        color = next(color_generator)

        for type_of_checking, addresses in person_routes.items():
            for address in addresses:
                feature = _build_feature(
                    id=id,
                    address=address,
                    person_name=person_name,
                    type_of_checking=type_of_checking,
                    color=color,
                    get_coordinates=get_coordinates,
                    offset_coordinates=offsetter,
                )
                coros.append(feature)
                id += 1

    features: list[Feature] = await asyncio.gather(*coros)
    return FeatureCollection(features=features)
