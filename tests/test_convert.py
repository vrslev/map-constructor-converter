import pytest

from geodecoder.convert import build_caption
from geodecoder.routes import PersonName, TypeOfChecking


@pytest.mark.parametrize(
    "person_name,type_of_checking,address_description,result",
    [
        ["Иван Иванов", "Подключения", "Первомайская, 1, 10", "Иванов подключения 10"],
        ["Иванов", "Ремонты", "Первомайская, 1, 0", "Иванов ремонты 0"],
    ],
)
def test_build_caption(
    person_name: PersonName,
    type_of_checking: TypeOfChecking,
    address_description: str,
    result: str,
):
    assert build_caption(person_name, type_of_checking, address_description) == result
