import json 
import os
from itertools import count

FILE_PATH = "../data/person.json"
id_generator = count(start=1)

def create_person(first_name: str, last_name: str, age: int, expirience: int, email: str) -> str: 
    if age < 18: 
        return "Пользователь не подходит по возрасту."
    else: 
        new_person = {
            "person_id": next(id_generator),
            "first_name": first_name, 
            "last_name": last_name, 
            "age": age, 
            "expirience": expirience, 
            "email": email
        }
        
        if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
            with open(FILE_PATH, "r", encoding="utf-8") as file:
                data_list = json.load(file)
        else: 
            data_list = []
            
        data_list.append(new_person)
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data_list, file, ensure_ascii=False, indent=4)
        return "Пользователь успешно зарегистрирован."

def update_person(person_id: int, first_name: str, last_name:str, age:int, expirience: int, email: str) -> str:
    if age < 18: 
        return "Пользователь не подходит по возрасту."
    else: 
        if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
            with open(FILE_PATH, "r", encoding="utf-8") as file:
                data_list = json.load(file)
        else: 
            new_person = {
                "person_id": person_id,
                "first_name": first_name, 
                "last_name": last_name, 
                "age": age, 
                "expirience": expirience, 
                "email": email
            }
            data_list = []
            
            is_changed = False
            for person in data_list: 
                if person["person_id"] == person_id: 
                    person = new_person 
                    is_changed = True
                    return "Данные о пользователе успешно обновленны!"
            if not is_changed:
                return "Пользователь с таким id не найден."
            
    
def delete_peron(person_id: int) -> str: 
    if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data_list = json.load(file)
    else: 
        data_list = []
    
    person_id_exists = any(data_list.get("person_id") == person_id for person in data_list)
    
    if person_id_exists: 
        data_list = [person for person in data_list if person.get("person_id") != person_id]
        return f"Пользователь успешно удален."
    else: 
        return "Пользователь с таким id не найден."
    
def get_person_by_id(person_id: int) -> dict: 
    if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data_list = json.load(file)
    else: 
        data_list = []
    
    needed_person = None
    for person in data_list: 
        if person["person_id"] == person_id: 
            needed_person = person
    
    if needed_person is not None: 
        return needed_person
    else: 
        return None