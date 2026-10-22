def filter_by_state(transactions, state='EXECUTED'):
    return [t for t in transactions if t.get('state') == state]



def sort_by_date(transactions, reverse=True):
    return sorted(transactions, key=lambda x: x.get('date'), reverse=reverse)