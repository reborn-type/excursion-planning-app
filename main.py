def is_good_age_for_excoursion(age:int , min_age:int, max_age = 100) -> bool: 
    if age < min_age:
        return False
    elif age > max_age:
        return False
    else:
        return True

def calculate_guide_salary(route_len_meters: int, guide_bid_for_kilometer: float, group: list) -> float:
    if len(group) > 10: 
        guide_bid_for_kilometer *= 1.5
    elif len(group) > 20: 
        guide_bid_for_kilometer *= 2 
    return route_len_meters/1000 * guide_bid_for_kilometer

def division_groups(group: list, subgroup_count: int) -> list:
    subgroups = []
    sub = []
    for i in range(len(group) - 1): 
        if i % subgroup_count != 0: 
            sub.append(group[i])
        else: 
            subgroups.append(sub)
            sub = []
    if len(sub) > 0: 
        subgroups.append(sub)
        
    return subgroups