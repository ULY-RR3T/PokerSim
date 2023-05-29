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

def are_consecutive(lst):
    sorted_lst = sorted(lst)  # Sort the list in ascending order
    return all(sorted_lst[i] + 1 == sorted_lst[i + 1] for i in range(len(sorted_lst) - 1))

def flatten(lst):
    flattened_list = []
    for item in lst:
        if isinstance(item, list):
            flattened_list.extend(flatten(item))
        else:
            flattened_list.append(item)
    return flattened_list

def colorize(card):
    if '♦' in card or '♥' in card:
        return f"\033[31m{card}\033[0m"  # Red color for diamonds and hearts
    else:
        return f"\033[30m{card}\033[0m"  # Black color for clubs and spades


















