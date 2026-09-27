import json 
from pathlib import Path 
from typing import Any

class JsonStorage:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        
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
            
    def load(self) -> Any:
        if not self.file_path.exists():
            return []

        with self.file_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def append(self, item: Any) -> None:
        data = self.load()

        if not isinstance(data, list):
            raise ValueError(
                "JSON должен содержать список"
            )

        data.append(item)
        self.save(data)
            
        