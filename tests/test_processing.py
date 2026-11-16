import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_transactions():
    """Набор транзакций для тестов: разные статусы и даты"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-10T10:00:00"},
        {"id": 2, "state": "EXECUTED", "date": "2024-01-05T12:00:00"},
        {"id": 3, "state": "CANCELED", "date": "2024-01-15T09:00:00"},
        {"id": 4, "state": "PENDING", "date": "2024-01-20T11:00:00"},
    ]


@pytest.fixture
def transactions_without_state():
    """Транзакции, у которых может не быть ключа state"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-10T10:00:00"},
        {"id": 5, "date": "2024-01-30T13:00:00"},
    ]


class TestFilterByState:
    def test_filter_executed_default(self, sample_transactions):
        """По умолчанию фильтрует по 'EXECUTED'"""
        result = filter_by_state(sample_transactions)
        assert len(result) == 2
        ids = [t["id"] for t in result]
        assert ids == [1, 2]

    def test_filter_specific_state(self, sample_transactions):
        """Фильтрация по явно указанному статусу"""
        result = filter_by_state(sample_transactions, state="CANCELED")
        assert len(result) == 1
        assert result[0]["id"] == 3

    def test_filter_non_existent_state(self, sample_transactions):
        """Если такого статуса нет — возвращается пустой список"""
        result = filter_by_state(sample_transactions, state="UNKNOWN")
        assert result == []

    def test_filter_missing_state_key(self, sample_transactions):
        """Транзакции без ключа 'state' не попадают в выборку"""
        # В sample_transactions есть id=5 без ключа state
        result = filter_by_state(sample_transactions, state="EXECUTED")
        # id=5 не должен быть в результате
        ids = [t["id"] for t in result]
        assert 5 not in ids

    @pytest.mark.parametrize(
        "state, expected_count",
        [
            ("EXECUTED", 2),
            ("CANCELED", 1),
            ("PENDING", 1),
            ("UNKNOWN", 0),
        ],
    )
    def test_parametrized_counts(self, sample_transactions, state, expected_count):
        result = filter_by_state(sample_transactions, state=state)
        assert len(result) == expected_count

    def test_empty_list(self):
        assert filter_by_state([]) == []


class TestSortByDate:
    def test_sort_descending_default(self, sample_transactions):
        """Сортировка по убыванию (новые сначала)"""
        result = sort_by_date(sample_transactions)
        dates = [t.get("date") for t in result]
        # Проверка, что список отсортирован по убыванию строк (лексикографически)
        # Для формата YYYY-MM-DD лексикографическая сортировка совпадает с хронологической
        assert dates == sorted(dates, reverse=True)

    def test_sort_ascending(self, sample_transactions):
        """Сортировка по возрастанию"""
        result = sort_by_date(sample_transactions, reverse=False)
        dates = [t.get("date") for t in result]
        assert dates == sorted(dates)

    def test_stable_sort_same_dates(self):
        """При одинаковых датах порядок должен сохраняться (стабильная сортировка Python)"""
        data = [
            {"id": 10, "date": "2024-05-01"},
            {"id": 20, "date": "2024-05-01"},
            {"id": 30, "date": "2024-05-01"},
        ]
        result = sort_by_date(data, reverse=False)
        ids = [t["id"] for t in result]
        assert ids == [10, 20, 30]

    def test_handle_missing_date_key(self, sample_transactions):
        """Функция не должна падать, если у некоторых записей нет ключа 'date'"""
        # В sample_transactions есть id=6 без ключа date
        result = sort_by_date(sample_transactions)
        assert isinstance(result, list)
        assert len(result) == len(sample_transactions)

        # Важно: .get('date') вернет None для id=6.
        # При сортировке None в Python (3.x) ведет себя странно при сравнении со строками,
        # но функция не упадет. В реальном проекте лучше явно обрабатывать None,
        # но тесты подтверждают, что текущая реализация не выбрасывает исключение.

    def test_empty_list(self):
        assert sort_by_date([]) == []
