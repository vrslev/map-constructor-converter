import pytest

from geodecoder.convert import build_caption
from geodecoder.routes import PersonName, TypeOfChecking


@pytest.mark.parametrize(
    "person_name,type_of_checking,address_description,result",
    [
        ["Иван Иванов", "Подключения", "Первомайская, 1, 10", "Иванов П 10"],
        ["Иван Иванов", "Подключение", "Первомайская, 1, 10", "Иванов П 10"],
        ["Иванов", "Ремонты", "Первомайская, 1, 0", "Иванов Р 0"],
        ["Иванов", "Ремонт", "Первомайская, 1, 0", "Иванов Р 0"],
        ["Иванов", "Другое", "Первомайская, 1, 0", "Иванов другое 0"],
    ],
)
def test_build_caption(
    person_name: PersonName,
    type_of_checking: TypeOfChecking,
    address_description: str,
    result: str,
):
    assert build_caption(person_name, type_of_checking, address_description) == result
