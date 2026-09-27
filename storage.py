import json
from pathlib import Path
from typing import Any
import os


class JsonStorage:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def __str__(self) -> str:
        return (
            f"""
            Путь файла: {self.file_path}
            """
        )

    def save(self, data: Any) -> None:
        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4,
            )

    def load(self, ):
        if not os.path.exists(self.file_path) or os.path.getsize(
                self.file_path) == 0:
            return []
        with open(self.file_path, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

    def append(self, item: Any) -> None:
        data = self.load()

        if not isinstance(data, list):
            raise ValueError(
                "JSON должен содержать список"
            )

        data.append(item)
        self.save(data)

    def delete_by_id(
        self,
        field_name: str,
        field_value: int
    ) -> bool:
        data = self.load()

        if not isinstance(data, dict):
            raise ValueError(
                "Json должен содержать список."
            )

        for item in data:
            if isinstance(item, dict) and item.get(field_name) == field_value:
                data.remove(item)
                self.save(data)
                return True

        return False
