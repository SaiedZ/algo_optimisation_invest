def get_all_combinations(list_items):

    if not list_items:
        return [[]]

    first_element = list_items[0]
    combination_without_first_elemt = get_all_combinations(list_items[1:])
    combination_with_first_elemt = [
        [*comb, first_element] for comb in combination_without_first_elemt
    ]

    return [*combination_without_first_elemt, *combination_with_first_elemt]
