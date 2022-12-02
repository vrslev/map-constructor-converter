from textwrap import dedent

import pytest

from textwrap import dedent
from typing import Any

from geodecoder.routes import (
    Address,
    PersonName,
    Routes,
    TypeOfChecking,
)

def desc(count: int) -> str:
    return f"addr {count}"

def url(count: int) -> Any:
    return f"https://example.com/{count}"

def address(count: int) -> Address:
    return Address(description=desc(count), plan_url=url(count))

# fmt: off
_content = dedent(f"""\
Иван Иванов:
Подключения:
{desc(1)} {url(1)}
{desc(2)} {url(2)}
Ремонты:
Ситилинк, {desc(3)} {url(3)}


Петров:
Подключения:
Ситилинк, {desc(4)} {url(4)}
""")
# fmt: on


@pytest.fixture
def content():
    return _content

@pytest.fixture
def routes() -> Routes:
    return {
        PersonName("Иван Иванов"): {
            TypeOfChecking("Подключения"): [
                address(1), address(2)
            ],
            TypeOfChecking("Ремонты"): [
                address(3)
            ],
        },
        PersonName("Петров"): {
            TypeOfChecking("Подключения"): [
                address(4)
            ]
        },
    }