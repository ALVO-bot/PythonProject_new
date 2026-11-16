import pytest

from src.widget import get_date, mask_account_card


@pytest.fixture
def card_input() -> str:
    return "Visa Platinum 7000792289606361"


@pytest.fixture
def account_input() -> str:
    return "Счет 73654108430135874305"


class TestMaskAccountCard:
    def test_masks_card(self, card_input: str) -> None:
        assert mask_account_card(card_input) == "Visa Platinum 7000 79** **** 6361"

    def test_masks_account(self, account_input: str) -> None:
        assert mask_account_card(account_input) == "Счет **4305"

    def test_empty_string(self) -> None:
        # по реализации: пустая строка -> пустая строка, без исключения
        assert mask_account_card("") == ""
        assert mask_account_card("   ") == ""

    def test_no_digits_returns_original(self) -> None:
        # по реализации: если цифр нет — строка возвращается как есть
        assert mask_account_card("Visa Platinum") == "Visa Platinum"
        assert mask_account_card("абвгд") == "абвгд"

    @pytest.mark.parametrize(
        "input_str, expected",
        [
            ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
            ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
            ("Счет 35383033474444918558", "Счет **8558"),
            ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
            # только номер без названия — card_type будет пустым
            ("7000792289606361", " 7000 79** **** 6361"),
        ],
        ids=["maestro", "mastercard", "account", "visa", "number_only"],
    )
    def test_parametrized(self, input_str: str, expected: str) -> None:
        assert mask_account_card(input_str) == expected

    @pytest.mark.parametrize(
        "input_str",
        ["Счет 1234", "Visa 123", "Карта 12"],
        ids=["short_account", "short_card", "very_short_card"],
    )
    def test_short_numbers_no_crash(self, input_str: str) -> None:
        # граничные случаи: номер короче ожидаемой длины — функция не должна падать
        result = mask_account_card(input_str)
        assert isinstance(result, str)

    def test_mixed_content(self) -> None:
        # цифры в названии — берётся первая цифра как начало номера
        result = mask_account_card("Карта 2200 1234 5678 9012")
        assert result == "Карта 2200 12** **** 9012"


class TestGetDate:
    def test_correct_conversion(self) -> None:
        assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"

    @pytest.mark.parametrize(
        "date_str, expected",
        [
            ("2024-03-11T02:26:18.671407", "11.03.2024"),
            ("2023-01-01T00:00:00.000000", "01.01.2023"),
            ("1999-12-31T23:59:59", "31.12.1999"),
        ],
    )
    def test_formats(self, date_str: str, expected: str) -> None:
        assert get_date(date_str) == expected

    @pytest.mark.parametrize(
        "date_str",
        ["", "не дата", "abc", "2024-13-45T99:99:99"],
        ids=["empty", "garbage", "short", "impossible_date"],
    )
    def test_no_crash_on_bad_input(self, date_str: str) -> None:
        # get_date не валидирует дату: на некорректном вводе
        # она не должна падать, но и корректную дату не вернёт
        result = get_date(date_str)
        assert isinstance(result, str)
