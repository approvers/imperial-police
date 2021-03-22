def includes(query: str, search_from: list):
    for test_case in search_from:
        if str(test_case) in str(query):
            return True
    return False
