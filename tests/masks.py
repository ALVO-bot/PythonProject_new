def get_mask_card_number(card_number: str) -> str:
    """Функция которая принимает на вход
    номер карты и возвращает ее маску"""
    clean_number = card_number.replace(" ", "")  # Удаляем пробелы
    block_1 = clean_number[:4]
    block_2 = clean_number[5:7] + "**"
    block_3 = "****"
    block_4 = clean_number[-4:]

    return f"{block_1} {block_2} {block_3} {block_4}"


def get_mask_account(account_number: str) -> str:
    """Функция которая принимает на вход
    номер счета и возвращает его маску"""
    first_mask = "**"
    last_mask = account_number[-4:]

    return f"{first_mask}{last_mask}"
