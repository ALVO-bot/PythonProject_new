from masks import get_mask_card_number, get_mask_account


def mask_account_card(data: str) -> str:
    data = data.strip()

    # Разделяем строки без явного разделения на аргументы пользователем
    if data.startswith("Счет "):
        # Выделяем часть "Счет" и остаток (номер)
        account_type = "Счет"
        account_number = data[len(account_type):].strip()

        # Используем существующую функцию маскировки счета
        masked_num = get_mask_account(account_number)

        return f"{account_type} {masked_num}"

    else:
        # Для карт ищем начало цифр, чтобы отделить описание (Visa Platinum и т.п.) от номера
        first_digit_idx = None
        for i, char in enumerate(data):
            if char.isdigit():
                first_digit_idx = i
                break

        if first_digit_idx is None:
            return data

        card_type = data[:first_digit_idx].strip()
        card_number = data[first_digit_idx:].strip()

        # Переиспользуем существующую функцию маскировки карты
        masked_num = get_mask_card_number(card_number)

        return f"{card_type} {masked_num}"
