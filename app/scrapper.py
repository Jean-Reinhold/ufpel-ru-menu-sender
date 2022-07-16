from numpy import str_
import requests
from dataclasses import dataclass

RESTAURANTS = {"SANTA CRUZ": 6}


@dataclass
class Meal:
    meal_type: str
    items: dict[str:str]


@dataclass
class Restaurant:
    name: str
    meals: list[Meal]


def get_request_url(restaurant_id: int, date: str) -> str:
    return f"""https://cobalto.ufpel.edu.br/portal/cardapios/cardapioPublico/listaCardapios?null&txtData={date}&cmbRestaurante={restaurant_id}&_search=false&nd=1657999113370&rows=20&page=1&sidx=refeicao+asc%2C+id&sord=asc"""


def get_restaurant_meals(url: str) -> list[Meal]:
    body = requests.get(url).json()
    raw_meals = {}
    for item in body["rows"]:
        if item["refeicao"] not in raw_meals:
            raw_meals[item["refeicao"]] = {}
        raw_meals[item["refeicao"]].update({item["nome"]: item["descricao"]})

    return [Meal(meal_type=key, items=raw_meals[key]) for key in raw_meals]


def get_ru_menu(date: str_) -> list[Restaurant]:
    restaurants = []
    for name in RESTAURANTS:
        url = get_request_url(restaurant_id=RESTAURANTS[name], date=date)
        restaurants.append(
            Restaurant(name=RESTAURANTS[name], meals=get_restaurant_meals(url=url))
        )
    return restaurants


if __name__ == "__main__":
    print(get_ru_menu("16/07/2022"))
