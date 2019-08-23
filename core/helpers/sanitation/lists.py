def dedup_list(list):
    """
    deduplicate list
    """
    new_list = []
    for item in list:
        if item not in new_list:
            new_list.append(item)

    return new_list
