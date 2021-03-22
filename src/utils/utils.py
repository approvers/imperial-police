def is_empty(target: list):
    if len(target) == 0:
        return True
    return False


def includes(query: str, search_from: list):
    for test_case in search_from:
        if str(test_case) in str(query):
            return True
    return False
