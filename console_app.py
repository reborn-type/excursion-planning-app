from models import User, Group, Excursion


class ConsoleEntity:
    def __init__(self, service, console):
        self.service = service
        self.console = console

    def run(self) -> None:
        while True:
            self.show_menu()

            command = self.console.read_choice(
                "Выберите действие: ",
                {
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "0",
                }
            )

            if command == "1":
                self.create()

            elif command == "2":
                self.show_all()

            elif command == "3":
                self.show_by_id()

            elif command == "4":
                self.update()

            elif command == "5":
                self.delete()

            elif command == "0":
                break

    def show_menu(self) -> None:
        raise NotImplementedError

    def create(self) -> None:
        raise NotImplementedError

    def show_all(self) -> None:
        raise NotImplementedError

    def show_by_id(self) -> None:
        raise NotImplementedError

    def update(self) -> None:
        raise NotImplementedError

    def delete(self) -> None:
        raise NotImplementedError


class UserConsole(ConsoleEntity):
    def show_menu(self) -> None:
        print("\n--- Пользователи ---")
        print("1. Создать пользователя")
        print("2. Показать всех")
        print("3. Найти по id")
        print("4. Изменить")
        print("5. Удалить")
        print("0. Назад")

    def create(self) -> None:
        user = User(
            user_id=0,
            first_name=self.console.read_string("Имя: "),
            last_name=self.console.read_string("Фамилия: "),
            age=self.console.read_int("Возраст: ", min_value=0, max_value=120),
            experience=self.console.read_int("Опыт: ", min_value=0),
            email=self.console.read_email("Email: "),
            guide_status=self.console.read_bool("Является гидом?"),
        )

        try:
            self.service.add(user)
        except ValueError as error:
            print(f"Ошибка: {error}")
        else:
            print("Пользователь создан.")

    def show_all(self) -> None:
        users = self.service.get_all()

        if not users:
            print("Пользователей нет.")
            return

        for user in users:
            print()
            print(user)
            print("-" * 40)

    def show_by_id(self) -> None:
        user_id = self.console.read_int(
            "Введите id пользователя: ",
            min_value=1,
        )

        user = self.service.get_by_id(user_id)

        if user is None:
            print("Пользователь не найден.")
        else:
            print(user)

    def update(self) -> None:
        user_id = self.console.read_int(
            "Введите id пользователя: ", min_value=1)

        user = self.service.get_by_id(user_id)

        if user is None:
            print("Пользователь не найден.")
            return

        changes = {}

        first_name = input("Новое имя или Enter: ").strip()

        if first_name:
            changes["first_name"] = first_name

        last_name = input("Новая фамилия или Enter: ").strip()

        if last_name:
            changes["last_name"] = last_name

        age_text = input("Новый возраст или Enter: ").strip()

        if age_text:
            try:
                age = int(age_text)
            except ValueError:
                print("Возраст должен быть числом.")
                return

            if age < 0 or age > 120:
                print("Возраст должен быть от 0 до 120.")
                return

            changes["age"] = age

        email = input("Новый email или Enter: ").strip()

        if email:
            changes["email"] = email

        if not changes:
            print("Изменения не указаны.")
            return

        try:
            updated_user = self.service.update(user_id, **changes)
        except ValueError as error:
            print(f"Ошибка: {error}")
        else:
            if updated_user is None:
                print("Пользователь не найден.")
            else:
                print("Пользователь изменён.")

    def delete(self) -> None:
        user_id = self.console.read_int(
            "Введите id пользователя: ",
            min_value=1,
        )

        deleted = self.service.delete(user_id)

        if deleted:
            print("Пользователь удалён.")
        else:
            print("Пользователь не найден.")


class ExcursionConsole(ConsoleEntity):
    def show_menu(self) -> None:
        print("\n--- Экскурсии ---")
        print("1. Создать экскурсию")
        print("2. Показать все")
        print("3. Найти по id")
        print("4. Изменить")
        print("5. Удалить")
        print("0. Назад")

    def create(self) -> None:
        min_persons = self.console.read_int(
            "Минимум участников: ",
            min_value=1,
        )

        max_persons = self.console.read_int(
            "Максимум участников: ",
            min_value=min_persons,
        )

        min_age = self.console.read_int(
            "Минимальный возраст: ",
            min_value=0,
        )

        max_age = self.console.read_int(
            "Максимальный возраст: ",
            min_value=min_age,
        )

        excursion = Excursion(
            excursion_id=self.console.read_int(
                "Id экскурсии: ",
                min_value=1,
            ),
            excursion_name=self.console.read_string(
                "Название экскурсии: "
            ),
            max_persons=max_persons,
            min_persons=min_persons,
            max_age=max_age,
            min_age=min_age,
            route_length_m=self.console.read_int(
                "Длина маршрута в метрах: ",
                min_value=1,
            ),
            guide_id=self.console.read_int(
                "Id экскурсовода: ",
                min_value=1,
            ),
        )

        try:
            self.service.add(excursion)
        except ValueError as error:
            print(f"Ошибка: {error}")
        else:
            print("Экскурсия создана.")

    def show_all(self) -> None:
        excursions = self.service.get_all()

        if not excursions:
            print("Экскурсий нет.")
            return

        for excursion in excursions:
            print()
            print(excursion)
            print("-" * 40)

    def show_by_id(self) -> None:
        excursion_id = self.console.read_int(
            "Введите id экскурсии: ",
            min_value=1,
        )

        excursion = self.service.get_by_id(
            excursion_id
        )

        if excursion is None:
            print("Экскурсия не найдена.")
        else:
            print(excursion)

    def update(self) -> None:
        excursion_id = self.console.read_int(
            "Введите id экскурсии: ",
            min_value=1,
        )

        excursion = self.service.get_by_id(
            excursion_id
        )

        if excursion is None:
            print("Экскурсия не найдена.")
            return

        changes = {}

        name = input("Новое имя или Enter: ", required=False)

        if name:
            changes["excursion_name"] = name

        max_persons = input(
            "Новый максимум участников или Enter: ",
            required=False).strip()

        if max_persons:
            try:
                changes["max_persons"] = int(max_persons)
            except ValueError:
                print("Количество участников должно быть числом.")
                return

        route_length = input(
            "Новая длина маршрута или Enter: ",
            required=False).strip()

        if route_length:
            try:
                changes["route_length_m"] = int(route_length)
            except ValueError:
                print("Длина маршрута должна быть числом.")
                return

        if not changes:
            print("Изменения не указаны.")
            return

        try:
            self.service.update(
                excursion_id,
                **changes,
            )
        except ValueError as error:
            print(f"Ошибка: {error}")
        else:
            print("Экскурсия изменена.")

    def delete(self) -> None:
        excursion_id = self.console.read_int(
            "Введите id экскурсии: ",
            min_value=1,
        )

        deleted = self.service.delete(
            excursion_id
        )

        if deleted:
            print("Экскурсия удалена.")
        else:
            print("Экскурсия не найдена.")


class GroupConsole(ConsoleEntity):
    def show_menu(self) -> None:
        print("\n--- Группы ---")
        print("1. Создать группу")
        print("2. Показать все")
        print("3. Найти по id")
        print("4. Изменить")
        print("5. Удалить")
        print("0. Назад")

    def create(self) -> None:
        group = Group(
            group_id=self.console.read_int(
                "Id группы: ",
                min_value=1,
            ),
            excursion_id=self.console.read_int(
                "Id экскурсии: ",
                min_value=1,
            ),
            count_of_people=0,
            persons={},
        )

        try:
            self.service.add(group)
        except ValueError as error:
            print(f"Ошибка: {error}")
        else:
            print("Группа создана.")

    def show_all(self) -> None:
        groups = self.service.get_all()

        if not groups:
            print("Групп нет.")
            return

        for group in groups:
            print()
            print(group)
            print("-" * 40)

    def show_by_id(self) -> None:
        group_id = self.console.read_int(
            "Введите id группы: ",
            min_value=1,
        )

        group = self.service.get_by_id(group_id)

        if group is None:
            print("Группа не найдена.")
        else:
            print(group)

    def update(self) -> None:
        group_id = self.console.read_int("Введите id группы: ", min_value=1,)

        group = self.service.get_by_id(group_id)

        if group is None:
            print("Группа не найдена.")
            return

        excursion_id = input(
            "Новый id экскурсии или Enter: ",
            required=False).strip()

        changes = {}

        if excursion_id:
            try:
                changes["excursion_id"] = int(
                    excursion_id
                )
            except ValueError:
                print("Id экскурсии должен быть числом.")
                return

        if not changes:
            print("Изменения не указаны.")
            return

        try:
            self.service.update(
                group_id,
                **changes,
            )
        except ValueError as error:
            print(f"Ошибка: {error}")
        else:
            print("Группа изменена.")

    def delete(self) -> None:
        group_id = self.console.read_int(
            "Введите id группы: ",
            min_value=1,
        )

        deleted = self.service.delete(group_id)

        if deleted:
            print("Группа удалена.")
        else:
            print("Группа не найдена.")
