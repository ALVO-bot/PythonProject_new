import pytest

from src.masks import get_mask_account, get_mask_card_number


class TestGetMaskCardNumber:
    def test_standard_card_16_digits(self):
        """Стандартный случай: 16 цифр"""
        result = get_mask_card_number("7000792289606361")
        # Логика твоей функции:
        # block_1 = 7000
        # block_2 = 79 + "**" -> "79**"
        # block_3 = "****"
        # block_4 = 6361
        assert result == "7000 79** **** 6361"

    def test_card_with_spaces(self):
        """Функция должна удалять пробелы перед обработкой"""
        result = get_mask_card_number("7000 7922 8960 6361")
        assert result == "7000 79** **** 6361"

    @pytest.mark.parametrize(
        "input_num, expected",
        [
            ("1111222233334444", "1111 22** **** 4444"),
            ("9876543210987654", "9876 54** **** 7654"),
        ],
    )
    def test_parametrized_cards(self, input_num, expected):
        assert get_mask_card_number(input_num) == expected

    def test_short_card_behavior(self):
        """
        Проверка поведения на коротком номере.
        Твоя функция НЕ проверяет длину. Она просто берет срезы.
        Для '1234':
        block_1 = '1234'
        block_2 = ''[5:7] (пусто) + '**' -> '**'
        block_3 = '****'
        block_4 = '1234' (последние 4)
        Результат: '1234 ** **** 1234'
        Тест фиксирует текущее поведение.
        """
        result = get_mask_card_number("1234")
        assert result == "1234 ** **** 1234"

    def test_empty_string(self):
        result = get_mask_card_number("")
        # Срезы пустой строки вернут пустые строки
        assert result == ""
        # Примечание: из-за пробелов в f-строке получится много пробелов.
        # Если это нежелательно, в функцию стоит добавить проверку if not clean_number: return ""

    def test_non_digit_chars(self):
        """Пробелы удаляются, остальные символы остаются в позициях"""
        # Удалится только пробел, 'A' останется на месте среза
        result = get_mask_card_number("123A 4567 8901 2345")
        clean = "123A456789012345"
        # block_1='123A', block_2='45**', block_4='2345'
        assert result == "123A 45** **** 2345"


class TestGetMaskAccount:
    def test_standard_account(self):
        """Стандартная маска счета: последние 4 цифры + ** спереди"""
        result = get_mask_account("73654108430135874305")
        assert result == "**4305"

    @pytest.mark.parametrize(
        "input_acc, expected",
        [
            ("12345678901234567890", "**7890"),
            ("99998888777766665555", "**5555"),
        ],
    )
    def test_parametrized_accounts(self, input_acc, expected):
        assert get_mask_account(input_acc) == expected

    def test_short_account(self):
        """Если номер короче 4 цифр, срез [-4:] вернет всю строку"""
        result = get_mask_account("123")
        assert result == "**123"

    def test_very_short_account(self):
        result = get_mask_account("1")
        assert result == "**1"

    def test_empty_account(self):
        result = get_mask_account("")
        assert result == "**"
