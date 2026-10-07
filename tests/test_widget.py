from masks import get_mask_card_number, get_mask_account


def _mask_card_number(number: str) -> str:
    if len(number) < 4:
        return "*" * len(number)
    prefix = number[:4]
    suffix = number[-4:]
    middle = "*" * (len(number) - 8)
    full = prefix + middle + suffix
    return " ".join(full[i:i + 4] for i in range(0, len(full), 4))


def _mask_account_number(number: str) -> str:
    if len(number) <= 4:
        return number
    return f"**{number[-4:]}"


def mask_account_card(data: str) -> str:
    data = data.strip()
    if not data:
        return ""

    if data.lower().startswith("счет "):
        account_type = "Счет"
        raw_number = data[5:].strip()
        masked_num = _mask_account_number(raw_number)
        return f"{account_type} {masked_num}"

    first_digit_idx = None
    for i, char in enumerate(data):
        if char.isdigit():
            first_digit_idx = i
            break

    if first_digit_idx is None:
        return data

    card_type = data[:first_digit_idx].strip()
    card_number = data[first_digit_idx:].strip()

    masked_num = _mask_card_number(card_number)
    return f"{card_type} {masked_num}"


# --- БЛОК ТЕСТОВ ---
if __name__ == "__main__":
    test_data = [
        "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Счет 35383033474447895560",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
        "Счет 73654108430135874305",
        "  Maestro   159683...  ",  # Грязные данные для проверки strip()
        "NoDigitsHere"  # Проверка защиты от отсутствия цифр
    ]



    for item in test_data:
        result = mask_account_card(item)
        print(result)
