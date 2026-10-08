from masks import get_mask_card_number, get_mask_account


def mask_account_card(data: str) -> str:
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


# --- БЛОК ТЕСТОВ ---
if __name__ == "__main__":
    test_data = ["Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Счет 35383033474447895560",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
        "Счет 73654108430135874305",
        "  Maestro   159683...  ",
        "NoDigitsHere" ] # Проверка защиты от отсутствия цифр


    for item in test_data:
        result = mask_account_card(item)
        print(result)
