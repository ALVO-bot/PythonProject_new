from masks import get_mask_card_number, get_mask_account


def mask_account_card(data: str) -> str:
    """ Функция которая умеет обрабатывать информацию как о картах, так и о счетах """
    data = data.strip()
    if not data:
        return ""

    # Разделяем строки без явного разделения на аргументы пользователем
    if data.startswith("Счет "):
        # Выделяем часть "Счет" и остаток (номер)
        account_type = "Счет"
        account_number = data[len(account_type):].strip()

        # Используем существующую функцию маскировки счета
        masked_num = get_mask_account(account_number)

        return f"{account_type} {masked_num}"

    else:
        # Для карт ищем начало цифр, чтобы отделить название счета от номера
        first_indx = None
        for i, char in enumerate(data):
            if char.isdigit():
                first_indx = i
                break

        if first_indx is None:
            return data

        card_type = data[:first_indx].strip()
        card_number = data[first_indx:].strip()


        # Используем существующую функцию маскировки карты
        masked_num = get_mask_card_number(card_number)

        return f"{card_type} {masked_num}"


def get_date(date: str) -> str:
    """
    Преобразует строку в формат "ДД.ММ.ГГГГ"
    """
    return f"{date[8:10]}.{date[5:7]}.{date[0:4]}"
