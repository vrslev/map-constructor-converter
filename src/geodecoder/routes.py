from typing import Any, NewType, cast

from pydantic import BaseModel, HttpUrl


class Address(BaseModel):
    description: str
    plan_url: HttpUrl


TypeOfChecking = NewType("TypeOfChecking", str)
PersonName = NewType("PersonName", str)
PersonRoutes = dict[TypeOfChecking, list[Address]]
Routes = dict[PersonName, PersonRoutes]


def parse_routes(content: str) -> Routes:
    result: Routes = {}
    cur_name: PersonName | None = None
    cur_type: TypeOfChecking | None = None
    cur_routes: list[Address] = []
    throw_next_line: bool = False
    lines = content.splitlines()

    def save_routes():
        nonlocal cur_name
        nonlocal cur_type
        nonlocal cur_routes

        if cur_name and cur_type and cur_routes:
            result[cur_name][cur_type] = cur_routes
            cur_type = None
            cur_routes = []
        else:
            assert not cur_name
            assert not cur_type
            assert not cur_routes

    for idx, line in enumerate(lines):
        line = line.strip()

        if line == "":
            save_routes()
            cur_name = None

        elif line.endswith(":"):
            line = line[:-1]

            if cur_name:
                if cur_type:
                    save_routes()
                cur_type = TypeOfChecking(line)
            else:
                cur_name = PersonName(line)
                result.setdefault(cur_name, {})

        else:
            if not throw_next_line:
                address = Address(
                    description=line.removeprefix("Ситилинк,").strip(),
                    plan_url=cast(Any, lines[idx + 1]),
                )
                cur_routes.append(address)
            throw_next_line = not throw_next_line

    save_routes()
    return result
