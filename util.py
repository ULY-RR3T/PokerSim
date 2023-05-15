from simulator import *

def validate_card(card):
    assert isinstance(card,Card)
    assert card.validate()

def check_all_equal(lst):
    if not lst:  # If the list is empty, return True
        return True
    first_element = lst[0]
    for element in lst:
        if element != first_element:
            return False
    return True

def pretty_bool(bool):
    if bool:
        return '🟩'
    else:
        return '🟥'