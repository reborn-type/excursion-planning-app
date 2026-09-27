import json 
import os
from itertools import count
from guides import get_guide_by_id

FILE_PATH = "../data/excursion.json"
id_generator = count(start=1)

def create_excursion(guide_id: int, max_persons: int, min_persons: int, max_age: int, min_age: int, route_length_m: float) -> str: 
    if not guide_id: 
        return "Неверный id путеводителя."
    else: 
        curr_guide = get_guide_by_id(guide_id)
        guide_bonus = 1
        if route_length_m > 1500: 
            bonus = route_length_m // 1500 
            guide_bonus += bonus * 0.15
        new_excursion = {
            "excursion_id": next(id_generator), 
            "max_persons": max_persons,
            "min_persons": min_persons,
            "max_age": max_age,
            "min_age": min_age, 
            "guide_id": guide_id, 
            "route_length_m": route_length_m,
            "guide_salary": (route_length_m/1000) * (curr_guide['bid_for_kilometer'] * guide_bonus),
        }
        
        if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
            with open(FILE_PATH, "r", encoding="utf-8") as file:
                data_list = json.load(file)
        else: 
            data_list = []
            
        data_list.append(new_excursion)
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data_list, file, ensure_ascii=False, indent=4)
        return "Экскурсия создана."
    
def delete_excursion(excursion_id: int) -> str: 
    if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data_list = json.load(file)
    else: 
        data_list = []
    
    id_exists = any(data_list.get("excursion_id") == excursion_id for excursion in data_list)
    
    if id_exists: 
        data_list = [excursion for excursion in data_list if excursion.get("excursion_id") != excursion_id]
        return "Экскурсия успешно удалена."
    else: 
        return "Экскурсия с таким id не найдена."
    
def get_excursion_by_id(excursion_id: int) -> dict: 
    if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data_list = json.load(file)
    else: 
        data_list = []
    
    needed_excursion = None
    for excursion in data_list: 
        if excursion["excursion_id"] == excursion_id: 
            needed_excursion = excursion
    
    if needed_excursion is not None: 
        return needed_excursion
    else: 
        return None
    
