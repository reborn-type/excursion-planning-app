class ConsoleUtils:
    def read_string(self, question: str, required: bool = True) -> str:
        while True:
            command = input(question).strip()

            if required and not command:
                print("Поле не может быть пустым.")
                continue

            return command

    def read_int(self, question: str, min_value: int | None = None,
                 max_value: int | None = None) -> int:
        while True:
            value = input(question).strip()

            try:
                number = int(value)
            except ValueError:
                print("Введите целое число.")
                continue

            if (min_value is not None and number < min_value):
                print(f"Число не может быть меньше {min_value}.")
                continue

            if (max_value is not None and number > max_value):
                print(f"Число не может быть больше {max_value}.")
                continue

            return number

    def read_bool(self, question: str) -> bool:
        while True:
            value = input(f"{question} (y/n): ").strip().lower()

            if value in {"y", "yes", "д", "да"}:
                return True

            if value in {"n", "no", "н", "нет"}:
                return False

            print("Введите y/n или да/нет.")

    def read_email(self, question: str) -> str:
        while True:
            email = input(question).strip()

            if not email:
                print("Email не может быть пустым.")
                continue

            if "@" not in email:
                print("Введите корректный email.")
                continue

            return email

    def read_choice(self, question: str, choices: set[str]) -> str:
        while True:
            value = input(question).strip()

            if value in choices:
                return value

            print(f"Выберите один из вариантов: {', '.join(sorted(choices))}")

    def show_menu() -> None:
        print("\n--- Меню ---")
        print("1. Создать пользователя")
        print("2. Показать всех пользователей")
        print("3. Найти пользователя по id")
        print("4. Изменить пользователя")
        print("5. Удалить пользователя")
        print("0. Выход")
