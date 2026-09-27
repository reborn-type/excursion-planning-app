from __future__ import annotations
from models import User
from storage import JsonStorage
from models import Excursion
from models import Group


class UserService:
    def __init__(self, storage: JsonStorage):
        self.storage = storage

    def _next_id(self) -> int:
        users = self.get_all()
        if not users:
            return 1
        return max(user.user_id for user in users) + 1

    def get_all(self) -> list[User]:
        data = self.storage.load()

        return [User.from_dict(item) for item in data]

    def get_by_id(self, user_id: int,) -> User | None:
        users = self.get_all()

        for user in users:
            if user.user_id == user_id:
                return user

        return None

    def add(self, user: User) -> User:
        users = self.get_all()
        user.user_id = self._next_id()
        if any(u.user_id == user.user_id for u in users):
            raise ValueError(
                f"Пользователь с id={
                    user.user_id} уже существует.")
        users.append(user)
        self.save_users(users)

        return user

    def delete(self, user_id: int) -> bool:
        users = self.get_all()

        filtered_users = [user for user in users if user.user_id != user_id]

        if len(filtered_users) == len(users):
            return False

        self.save_users(filtered_users)

        return True

    def update(self, user_id: int, **kwargs) -> User | None:
        users = self.get_all()

        for user in users:
            if user.user_id == user_id:
                for field_name, new_value in kwargs.items():
                    if not hasattr(user, field_name):
                        raise ValueError(f"Неизвестное поле: {field_name}")

                    setattr(
                        user,
                        field_name,
                        new_value,
                    )

                self.save_users(users)

                return user

        return None

    def save_users(self, users: list[User]) -> None:
        data = [user.to_dict() for user in users]

        self.storage.save(data)

    def _save(self, users: list[User]) -> None:
        self.storage.save([user.to_dict()
                          for user in users], "./data/users.json")


class ExcursionService:
    def __init__(self, storage: JsonStorage):
        self.storage = storage

    def get_all(self) -> list[Excursion]:
        data = self.storage.load()

        return [Excursion.from_dict(item) for item in data]

    def _next_id(self) -> int:
        excursions = self.get_all()
        if not excursions:
            return 1
        return max(excursion.excursion_id for excursion in excursions) + 1

    def get_by_id(self, excursion_id: int) -> Excursion | None:
        excursions = self.get_all()

        return next(
            (excursion for excursion in excursions if excursion.excursion_id == excursion_id),
            None,
        )

    def add(self, excursion: Excursion) -> Excursion:
        excursions = self.get_all()
        excursion.excursion_id = self._next_id()
        if any(e.excursion_id == excursion.excursion_id for e in excursions):
            raise ValueError(
                f"Экскурсия с id={
                    excursion.excursion_id} уже существует.")

        excursions.append(excursion)
        self._validate(excursion=excursion)
        self._save(excursions)

        return excursion

    def update(self, excursion_id: int, **kwargs) -> Excursion | None:
        excursions = self.get_all()

        excursion = next(
            (item for item in excursions if item.excursion_id == excursion_id),
            None,
        )

        if excursion is None:
            return None

        allowed_fields = {
            "excursion_name",
            "max_persons",
            "min_persons",
            "max_age",
            "min_age",
            "route_length_m",
            "guide_id",
        }

        unknown_fields = (
            set(kwargs) - allowed_fields
        )

        if unknown_fields:
            raise ValueError(f"Неизвестные поля: {unknown_fields}")

        for field_name, value in kwargs.items():
            setattr(
                excursion,
                field_name,
                value,
            )

        self._validate(excursion)
        self._save(excursions)

        return excursion

    def delete(self, excursion_id: int) -> bool:
        excursions = self.get_all()

        filtered = [
            excursion for excursion in excursions if excursion.excursion_id != excursion_id]

        if len(filtered) == len(excursions):
            return False

        self._save(filtered)
        return True

    def get_by_guide(self, guide_id: int) -> list[Excursion]:
        excursions = self.get_all()

        return [excursion for excursion in excursions if excursion.guide_id == guide_id]

    def find_by_name(self, name: str) -> list[Excursion]:
        excursions = self.get_all()

        search_name = name.casefold()

        return [
            excursion for excursion in excursions if search_name in excursion.excursion_name.casefold()]

    def _save(self, excursions: list[Excursion]) -> None:
        data = [excursion.to_dict() for excursion in excursions]

        self.storage.save(data)

    def _validate(self, excursion: Excursion) -> None:
        if not excursion.excursion_name.strip():
            raise ValueError("Название экскурсии не может быть пустым")

        if excursion.min_persons <= 0:
            raise ValueError(
                "Минимальное число участников должно быть больше нуля")

        if excursion.max_persons < excursion.min_persons:
            raise ValueError(
                "Максимальное число участников не может быть меньше минимального")

        if excursion.min_age < 0:
            raise ValueError("Минимальный возраст не может быть отрицательным")

        if excursion.max_age < excursion.min_age:
            raise ValueError(
                "Максимальный возраст не может быть меньше минимального")

        if excursion.route_length_m <= 0:
            raise ValueError("Длина маршрута должна быть больше нуля")


class GroupService:
    def __init__(self, storage: JsonStorage):
        self.storage = storage

    def get_all(self) -> list[Group]:
        data = self.storage.load()

        return [Group.from_dict(item) for item in data]

    def get_by_id(self, group_id: int) -> Group | None:
        groups = self.get_all()

        return next(
            (group for group in groups if group.group_id == group_id),
            None,
        )

    def _next_id(self) -> int:
        groups = self.get_all()
        if not groups:
            return 1
        return max(group.group_id for group in groups) + 1

    def add(self, group: Group) -> Group:
        groups = self.get_all()
        group.group_id = self._next_id()
        if any(g.group_id == group.group_id for g in groups):
            raise ValueError(f"Группа с id={group.group_id} уже существует.")
        groups.append(group)
        self._validate(group=group)
        self._save(groups)

        return group

    def update(self, group_id: int, **kwargs,) -> Group | None:
        groups = self.get_all()

        group = next(
            (item for item in groups if item.group_id == group_id),
            None,
        )

        if group is None:
            return None

        allowed_fields = {
            "excursion_id",
            "count_of_people",
            "persons",
        }

        unknown_fields = (
            set(kwargs) - allowed_fields
        )

        if unknown_fields:
            raise ValueError(f"Неизвестные поля: {unknown_fields}")

        for field_name, value in kwargs.items():
            if field_name == "persons":
                group.change_persons(value)
            else:
                setattr(
                    group,
                    field_name,
                    value,
                )

        self._validate(group)
        self._save(groups)

        return group

    def delete(self, group_id: int) -> bool:
        groups = self.get_all()

        filtered = [group for group in groups if group.group_id != group_id]

        if len(filtered) == len(groups):
            return False
        self._save(filtered)
        return True

    def get_by_excursion(self, excursion_id: int) -> list[Group]:
        groups = self.get_all()

        return [group for group in groups if group.excursion_id == excursion_id]

    def add_person(self, group_id: int, user_id: int,
                   person_data: dict) -> Group | None:
        groups = self.get_all()

        group = next(
            (item for item in groups if item.group_id == group_id),
            None,
        )

        if group is None:
            return None

        group.persons[str(user_id)] = person_data
        group.count_of_people = len(group.persons)

        self._validate(group)
        self._save(groups)

        return group

    def remove_person(self, group_id: int, user_id: int) -> Group | None:
        groups = self.get_all()

        group = next(
            (item for item in groups if item.group_id == group_id),
            None,
        )

        if group is None:
            return None

        person_key = str(user_id)

        if person_key not in group.persons:
            return None

        del group.persons[person_key]

        group.count_of_people = len(group.persons)

        self._save(groups)

        return group

    def _save(self, groups: list[Group]) -> None:
        data = [group.to_dict() for group in groups]

        self.storage.save(data)

    def _validate(self, group: Group) -> None:
        if group.count_of_people < 0:
            raise ValueError(
                "Количество участников не может быть отрицательным")

        actual_count = len(group.persons)

        if group.count_of_people != actual_count:
            raise ValueError(
                "count_of_people должен совпадать с количеством persons")
