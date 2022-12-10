def all_lower(list, value):
    for item in list:
        if item >= value:
            return False
    return True


def all_higher(list, value):
    for item in list:
        if item <= value:
            return False
    return True
