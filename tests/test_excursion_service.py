from models import Group
from services import GroupService
from storage import JsonStorage


def make_group(**overrides) -> Group:
    data = dict(
        group_id=0,
        excursion_id=1,
        count_of_people=0,
        persons={},
    )
    data.update(overrides)
    return Group(**data)


def test_add_assigns_id_1(tmp_path):
    service = GroupService(JsonStorage(str(tmp_path / "groups.json")))

    group = service.add(make_group())

    assert group.group_id == 1


def test_add_incrementing_ids(tmp_path):
    service = GroupService(JsonStorage(str(tmp_path / "groups.json")))

    g1 = service.add(make_group(excursion_id=1))
    g2 = service.add(make_group(excursion_id=2))

    assert g1.group_id == 1
    assert g2.group_id == 2


def test_get_by_id(tmp_path):
    service = GroupService(JsonStorage(str(tmp_path / "groups.json")))
    created = service.add(make_group(excursion_id=5))

    found = service.get_by_id(created.group_id)

    assert found is not None
    assert found.excursion_id == 5


def test_delete_existing(tmp_path):
    service = GroupService(JsonStorage(str(tmp_path / "groups.json")))
    created = service.add(make_group())

    assert service.delete(created.group_id) is True


def test_get_by_excursion(tmp_path):
    service = GroupService(JsonStorage(str(tmp_path / "groups.json")))
    service.add(make_group(excursion_id=1))
    service.add(make_group(excursion_id=1))
    service.add(make_group(excursion_id=2))

    result = service.get_by_excursion(1)

    assert len(result) == 2


def test_add_person_updates_count(tmp_path):
    service = GroupService(JsonStorage(str(tmp_path / "groups.json")))
    group = service.add(make_group())

    updated = service.add_person(
        group.group_id,
        user_id=10,
        person_data={"first_name": "Иван"},
    )

    assert updated is not None
    assert updated.count_of_people == 1
    assert "10" in updated.persons


def test_remove_person_updates_count(tmp_path):
    service = GroupService(JsonStorage(str(tmp_path / "groups.json")))
    group = service.add(make_group())
    service.add_person(group.group_id, 10, {"first_name": "Иван"})
    service.add_person(group.group_id, 20, {"first_name": "Пётр"})

    updated = service.remove_person(group.group_id, 10)

    assert updated.count_of_people == 1
    assert "10" not in updated.persons
    assert "20" in updated.persons


def test_persists_between_service_instances(tmp_path):
    path = str(tmp_path / "groups.json")

    service1 = GroupService(JsonStorage(path))
    service1.add(make_group(excursion_id=7))

    service2 = GroupService(JsonStorage(path))
    groups = service2.get_all()

    assert len(groups) == 1
    assert groups[0].excursion_id == 7
