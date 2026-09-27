from models import Excursion
from services import ExcursionService
from storage import JsonStorage


def make_excursion(**overrides) -> Excursion:
    data = dict(
        excursion_id=0,
        excursion_name="Прогулка по городу",
        max_persons=10,
        min_persons=2,
        max_age=60,
        min_age=12,
        route_length_m=5000,
        guide_id=1,
    )
    data.update(overrides)
    return Excursion(**data)


def test_add_assigns_id_1(tmp_path):
    service = ExcursionService(JsonStorage(str(tmp_path / "excursions.json")))

    excursion = service.add(make_excursion())

    assert excursion.excursion_id == 1


def test_add_incrementing_ids(tmp_path):
    service = ExcursionService(JsonStorage(str(tmp_path / "excursions.json")))

    e1 = service.add(make_excursion(excursion_name="A"))
    e2 = service.add(make_excursion(excursion_name="B"))

    assert e1.excursion_id == 1
    assert e2.excursion_id == 2


def test_get_by_id(tmp_path):
    service = ExcursionService(JsonStorage(str(tmp_path / "excursions.json")))
    created = service.add(make_excursion())

    found = service.get_by_id(created.excursion_id)

    assert found is not None
    assert found.excursion_name == "Прогулка по городу"


def test_get_by_id_missing(tmp_path):
    service = ExcursionService(JsonStorage(str(tmp_path / "excursions.json")))

    assert service.get_by_id(999) is None


def test_delete_existing(tmp_path):
    service = ExcursionService(JsonStorage(str(tmp_path / "excursions.json")))
    created = service.add(make_excursion())

    assert service.delete(created.excursion_id) is True


def test_delete_missing(tmp_path):
    service = ExcursionService(JsonStorage(str(tmp_path / "excursions.json")))

    assert service.delete(999) is False


def test_get_by_guide(tmp_path):
    service = ExcursionService(JsonStorage(str(tmp_path / "excursions.json")))
    service.add(make_excursion(guide_id=1))
    service.add(make_excursion(guide_id=2))
    service.add(make_excursion(guide_id=1))

    result = service.get_by_guide(1)

    assert len(result) == 2


def test_find_by_name_case_insensitive(tmp_path):
    service = ExcursionService(JsonStorage(str(tmp_path / "excursions.json")))
    service.add(make_excursion(excursion_name="Прогулка по городу"))
    service.add(make_excursion(excursion_name="Ночная прогулка"))

    result = service.find_by_name("ПРОГУЛКА")

    assert len(result) == 2


def test_persists_between_service_instances(tmp_path):
    path = str(tmp_path / "excursions.json")

    service1 = ExcursionService(JsonStorage(path))
    service1.add(make_excursion(excursion_name="Тестовая"))

    service2 = ExcursionService(JsonStorage(path))
    excursions = service2.get_all()

    assert len(excursions) == 1
    assert excursions[0].excursion_name == "Тестовая"
