from copy import deepcopy


class Group:
    group_id: int
    excursion_id: int
    count_of_people: int
    persons: dict

    def __init__(
        self,
        group_id: int,
        excursion_id: int,
        count_of_people: int,
        persons: int
    ):
        self.group_id = group_id
        self.excursion_id = excursion_id
        self.count_of_people = count_of_people
        self.persons = deepcopy(persons)

    def __str__(self) -> str:
        return (
            f"""
            Id группы: {self.group_id},
            id экскурсии: {self.excursion_id},
            количество участников в группе: {self.count_of_people},
            данные участников: {self.persons}
            """
        )

    def change_excursion_id(self, new_excursion_id: int) -> None:
        self.excursion_id = new_excursion_id

    def change_count_of_people(self, new_count_of_people: int) -> None:
        self.count_of_people = new_count_of_people

    def change_persons(self, new_persons: dict) -> None:
        self.persons = deepcopy(new_persons)

    def to_dict(self) -> dict:
        return {
            "group_id": self.group_id,
            "excursion_id": self.excursion_id,
            "count_of_people": self.count_of_people,
            "persons": self.persons
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Group":
        return cls(
            group_id=data["group_id"],
            excursion_id=data["excursion_id"],
            count_of_people=data["count_of_people"],
            persons=data["persons"]
        )
