import pytest

from models import User
from services import UserService
from storage import JsonStorage


def make_user(**overrides) -> User:
    data = dict(
        user_id=0,
        first_name="Иван",
        last_name="Иванов",
        age=30,
        experience=5,
        email="ivan@example.com",
        guide_status=True,
    )
    data.update(overrides)
    return User(**data)


def test_add_assigns_id_1(tmp_path):
    service = UserService(JsonStorage(str(tmp_path / "users.json")))

    user = service.add(make_user())

    assert user.user_id == 1


def test_add_incrementing_ids(tmp_path):
    service = UserService(JsonStorage(str(tmp_path / "users.json")))

    u1 = service.add(make_user(first_name="A"))
    u2 = service.add(make_user(first_name="B"))

    assert u1.user_id == 1
    assert u2.user_id == 2


def test_get_by_id_returns_added_user(tmp_path):
    service = UserService(JsonStorage(str(tmp_path / "users.json")))
    created = service.add(make_user(first_name="Пётр"))

    found = service.get_by_id(created.user_id)

    assert found is not None
    assert found.first_name == "Пётр"


def test_get_by_id_missing_returns_none(tmp_path):
    service = UserService(JsonStorage(str(tmp_path / "users.json")))

    assert service.get_by_id(999) is None


def test_delete_existing_user(tmp_path):
    service = UserService(JsonStorage(str(tmp_path / "users.json")))
    created = service.add(make_user())

    assert service.delete(created.user_id) is True
    assert service.get_by_id(created.user_id) is None


def test_delete_missing_user_returns_false(tmp_path):
    service = UserService(JsonStorage(str(tmp_path / "users.json")))

    assert service.delete(999) is False


def test_update_changes_first_name(tmp_path):
    service = UserService(JsonStorage(str(tmp_path / "users.json")))
    created = service.add(make_user(first_name="Иван"))

    updated = service.update(created.user_id, first_name="Сергей")

    assert updated is not None
    assert updated.first_name == "Сергей"


def test_update_missing_user_returns_none(tmp_path):
    service = UserService(JsonStorage(str(tmp_path / "users.json")))

    assert service.update(999, first_name="X") is None


def test_persists_between_service_instances(tmp_path):
    path = str(tmp_path / "users.json")

    service1 = UserService(JsonStorage(path))
    service1.add(make_user(first_name="Пётр"))

    service2 = UserService(JsonStorage(path))
    users = service2.get_all()

    assert len(users) == 1
    assert users[0].first_name == "Пётр"
