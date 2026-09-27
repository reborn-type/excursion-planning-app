class Excursion:
    excursion_id: int
    excursion_name: str
    max_persons: int
    min_persons: int
    max_age: int
    min_age: int
    route_length_m: int
    guide_id: int

    def __init__(
        self,
        excursion_id: int,
        excursion_name: str,
        max_persons: int,
        min_persons: int,
        max_age: int,
        min_age: int,
        route_length_m: int,
        guide_id: int
    ):
        self.excursion_id = excursion_id
        self.excursion_name = excursion_name
        self.max_persons = max_persons
        self.min_persons = min_persons
        self.max_age = max_age
        self.min_age = min_age
        self.route_length_m = route_length_m
        self.guide_id = guide_id

    def __str__(self) -> str:
        return (
            f"""
            Id экскурсии: {self.excursion_id},
            название экскурсии: {self.excursion_name},
            макс. кол-во людей: {self.max_persons},
            мин. кол-во людей: {self.min_persons},
            макс. возраст: {self.max_age},
            мин. возраст: {self.min_age},
            длина маршрута в м.: {self.route_length_m},
            id экскурсовода: {self.guide_id}
            """
        )

    def change_excursion_name(self, new_excursion_name: str) -> None:
        self.excursion_name = new_excursion_name

    def change_max_persons(self, new_max_persons: int) -> None:
        self.max_persons = new_max_persons

    def change_min_persons(self, new_min_persons: int) -> None:
        self.min_persons = new_min_persons

    def change_max_age(self, new_max_age: int) -> None:
        self.max_age = new_max_age

    def change_min_age(self, new_min_age: int) -> None:
        self.min_age = new_min_age

    def change_route_length(self, new_route_length: int) -> None:
        self.route_length_m = new_route_length

    def change_guide(self, new_guide_id: int) -> None:
        self.guide_id = new_guide_id

    def to_dict(self) -> dict:
        return {
            "excursion_id": self.excursion_id,
            "excursion_name": self.excursion_name,
            "max_persons": self.max_persons,
            "min_persons": self.min_persons,
            "max_age": self.max_age,
            "min_age": self.min_age,
            "route_length_m": self.route_length_m,
            "guide_id": self.guide_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Excursion":
        return cls(
            excursion_id=data["excursion_id"],
            excursion_name=data["excursion_name"],
            max_persons=data["max_persons"],
            min_persons=data["min_persons"],
            max_age=data["max_age"],
            min_age=data["min_age"],
            route_length_m=data["route_length_m"],
            guide_id=data["guide_id"]
        )
