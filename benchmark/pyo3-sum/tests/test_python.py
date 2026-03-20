#!/usr/bin/env python3
"""
Тесты для Python-интеграции pyo3-sum.

Запуск:
    python -m pytest tests/test_python.py -v
    
Или без pytest:
    python tests/test_python.py
"""

import unittest


class TestSumOfSquares(unittest.TestCase):
    """Тесты функции sum_of_squares."""

    @classmethod
    def setUpClass(cls):
        """Импортируем модуль один раз для всех тестов."""
        try:
            import pyo3_sum
            cls.pyo3_sum = pyo3_sum
        except ImportError as e:
            raise unittest.SkipTest("pyo3_sum module not available") from e

    def test_zero(self):
        """Сумма квадратов для 0."""
        self.assertEqual(self.pyo3_sum.sum_of_squares(0), 0)

    def test_one(self):
        """Сумма квадратов для 1."""
        self.assertEqual(self.pyo3_sum.sum_of_squares(1), 1)

    def test_small(self):
        """Сумма квадратов для небольших чисел."""
        self.assertEqual(self.pyo3_sum.sum_of_squares(2), 5)    # 1 + 4
        self.assertEqual(self.pyo3_sum.sum_of_squares(3), 14)   # 1 + 4 + 9
        self.assertEqual(self.pyo3_sum.sum_of_squares(4), 30)   # 1 + 4 + 9 + 16
        self.assertEqual(self.pyo3_sum.sum_of_squares(5), 55)   # 1 + 4 + 9 + 16 + 25
        self.assertEqual(self.pyo3_sum.sum_of_squares(10), 385)

    def test_medium(self):
        """Сумма квадратов для средних чисел."""
        # Формула: n(n+1)(2n+1)/6
        n = 100
        expected = n * (n + 1) * (2 * n + 1) // 6
        self.assertEqual(self.pyo3_sum.sum_of_squares(n), expected)

    def test_large(self):
        """Сумма квадратов для больших чисел."""
        n = 1_000_000
        expected = n * (n + 1) * (2 * n + 1) // 6
        result = self.pyo3_sum.sum_of_squares(n)
        self.assertEqual(result, expected)

    def test_type(self):
        """Проверка типа возвращаемого значения."""
        result = self.pyo3_sum.sum_of_squares(10)
        self.assertIsInstance(result, int)

    def test_large_type(self):
        """Проверка типа для больших чисел (должен быть int, не float)."""
        result = self.pyo3_sum.sum_of_squares(1_000_000)
        self.assertIsInstance(result, int)
        # Убедимся, что это не float с потерей точности
        self.assertEqual(result, 333333833333500000)


class TestSumOfSquaresFormula(unittest.TestCase):
    """Сравнение с математической формулой."""

    @classmethod
    def setUpClass(cls):
        try:
            import pyo3_sum
            cls.pyo3_sum = pyo3_sum
        except ImportError as e:
            raise unittest.SkipTest("pyo3_sum module not available") from e

    def formula(self, n: int) -> int:
        """Математическая формула суммы квадратов."""
        return n * (n + 1) * (2 * n + 1) // 6

    def test_range_0_to_100(self):
        """Проверка для диапазона 0-100."""
        for n in range(101):
            with self.subTest(n=n):
                self.assertEqual(self.pyo3_sum.sum_of_squares(n), self.formula(n))

    def test_powers_of_10(self):
        """Проверка для степеней 10."""
        for exp in range(7):  # 10^0 до 10^6
            n = 10 ** exp
            with self.subTest(n=n):
                self.assertEqual(self.pyo3_sum.sum_of_squares(n), self.formula(n))


if __name__ == "__main__":
    unittest.main(verbosity=2)
