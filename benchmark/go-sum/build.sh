#!/bin/bash
# Скрипт сборки Go-модуля для бенчмарка

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🔨 Сборка Go-библиотеки..."

# Сборка shared library
go build -buildmode=c-shared -o libgo_sum.so go_sum.go

# Создание Python-обёртки
cat > go_sum.py << 'EOF'
"""
Python-обёртка для Go-функции sum_of_squares.
Использует ctypes для вызова Cgo-библиотеки.
"""

import ctypes
import os

# Загрузка разделяемой библиотеки
_lib_path = os.path.join(os.path.dirname(__file__), 'libgo_sum.so')
_lib = ctypes.CDLL(_lib_path)

# Настройка сигнатуры функции
_lib.sum_of_squares_c.argtypes = [ctypes.c_uint64]
_lib.sum_of_squares_c.restype = ctypes.c_uint64


def sum_of_squares(n: int) -> int:
    """
    Вычисляет сумму квадратов чисел от 1 до n.

    Args:
        n: Верхняя граница диапазона (включительно)

    Returns:
        Сумма квадратов чисел от 1 до n
    """
    return _lib.sum_of_squares_c(n)


if __name__ == "__main__":
    # Тест функции
    test_n = 10
    result = sum_of_squares(test_n)
    expected = 385  # 1^2 + 2^2 + ... + 10^2 = 385
    print(f"sum_of_squares({test_n}) = {result}")
    print(f"Ожидалось: {expected}")
    print(f"Тест {'пройден' if result == expected else 'НЕ пройден'}!")
EOF

echo "✅ Сборка завершена!"
echo "   Библиотека: libgo_sum.so"
echo "   Python-модуль: go_sum.py"
echo ""
echo "Для запуска теста: python go_sum.py"
