def filter_by_state(transactions: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """ Функция которая возвращает новый список словарей, содержащий только
        те словари,у которых ключ state соответствует указанному значению """
    return [t for t in transactions if t.get('state') == state]


def sort_by_date(transactions: list[dict], reverse: bool = True) -> list[dict]:
    """ Функция которая возвращает новый список, отсортированный по дате"""
    return sorted(transactions, key=lambda x: x.get('date'), reverse=reverse)
