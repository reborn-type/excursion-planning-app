from console_app import ExcursionConsole, GroupConsole, UserConsole
from services import UserService, GroupService, ExcursionService
from storage import JsonStorage
from utils import ConsoleUtils


def main() -> None:
    console = ConsoleUtils()

    user_storage = JsonStorage(
        "data/users.json"
    )

    excursion_storage = JsonStorage(
        "data/excursions.json"
    )

    group_storage = JsonStorage(
        "data/groups.json"
    )

    user_service = UserService(
        user_storage
    )

    excursion_service = ExcursionService(
        excursion_storage
    )

    group_service = GroupService(
        group_storage
    )

    user_console = UserConsole(
        user_service,
        console,
    )

    excursion_console = ExcursionConsole(
        excursion_service,
        console,
    )

    group_console = GroupConsole(
        group_service,
        console,
    )

    while True:
        print("\n=== Главное меню ===")
        print("1. Пользователи")
        print("2. Экскурсии")
        print("3. Группы")
        print("0. Выход")

        command = console.read_choice(
            "Выберите раздел: ",
            {"0", "1", "2", "3"}
        )

        if command == "1":
            user_console.run()

        elif command == "2":
            excursion_console.run()

        elif command == "3":
            group_console.run()

        elif command == "0":
            print("Программа завершена.")
            break


if __name__ == "__main__":
    main()
