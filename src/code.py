def up_first(msg: str) -> str:
    """Делает первую букву строки заглавной."""
    if msg:
        return msg[0].upper() + msg[1:]
    else:
        return msg
