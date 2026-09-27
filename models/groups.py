import json 
import os
from itertools import count

FILE_PATH = "../data/groups.json"
id_generator = count(start=1)

def create_group(excursion_id: int, count_of_people: int, persons: dict) -> str: 
    if persons < 1 or excursion_id < 0: 
        return "Неверное количество людей или номер экскурсии."
    else: 
        new_group = {
            "group_id": next(id_generator), 
            "excursion_id": excursion_id, 
            "count_of_people": count_of_people,
            "persons": persons 
        }
        
        if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
            with open(FILE_PATH, "r", encoding="utf-8") as file:
                data_list = json.load(file)
        else: 
            data_list = []
            
        data_list.append(new_group)
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data_list, file, ensure_ascii=False, indent=4)
        return "Группа успешно сформированна"
    
def delete_group(group_id: int) -> str: 
    if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data_list = json.load(file)
    else: 
        data_list = []
    
    id_exists = any(data_list.get("group_id") == group_id for group in data_list)
    
    if id_exists: 
        data_list = [group for group in data_list if group.get("group_id") != group_id]
        return "Группа успешно удалена."
    else: 
        return "Группа с таким id не найдена."
    
def get_group_by_id(group_id: int) -> dict: 
    if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data_list = json.load(file)
    else: 
        data_list = []
    
    needed_group = None
    for group in data_list: 
        if group["group_id"] == group_id: 
            needed_group = group
    
    if needed_group is not None: 
        return needed_group
    else: 
        return None