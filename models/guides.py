import json 
import os
from itertools import count

FILE_PATH = "../data/guides.json"
id_generator = count(start=1)

def create_guide(first_name: str, last_name: str, age: int, expirience: int, bid_for_kilometer: float, email: str) -> str: 
    if age < 18 or expirience < 1: 
        return "Путеводитель не подходит по возрасту или опыту работы."
    else: 
        new_guide = {
            "guide_id": next(id_generator),
            "first_name": first_name, 
            "last_name": last_name, 
            "age": age, 
            "expirience": expirience, 
            "bid_for_kilometer": bid_for_kilometer,
            "email": email
        }
        
        if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
            with open(FILE_PATH, "r", encoding="utf-8") as file:
                data_list = json.load(file)
        else: 
            data_list = []
            
        data_list.append(new_guide)
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data_list, file, ensure_ascii=False, indent=4)
        return "Путеводитель успешно записан в штаб."
    
def delete_guide(guide_id: int) -> str: 
    if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data_list = json.load(file)
    else: 
        data_list = []
    
    guide_id_exists = any(data_list.get("guide_id") == guide_id for guide in data_list)
    
    if guide_id_exists: 
        data_list = [guide for guide in data_list if guide.get("guide_id") != guide_id]
        return f"Путеводитель успешно удален."
    else: 
        return "Путеводитель с таким id не найден."
    
def get_guide_by_id(guide_id: int) -> dict: 
    if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data_list = json.load(file)
    else: 
        data_list = []
    
    needed_guide = None
    for guide in data_list: 
        if guide["guide_id"] == guide_id: 
            needed_guide = guide
    
    if needed_guide is not None: 
        return needed_guide
    else: 
        return None