#!/usr/bin/env python3
"""
setup.py для установки Go-модуля go_sum.

Использование:
    pip install .
    
Или для разработки:
    pip install -e .
"""

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import subprocess
import os
import shutil


class BuildGoExtension(build_py):
    """Сборка Go-библиотеки перед установкой Python-пакета."""

    def run(self):
        # Получаем директорию текущего пакета
        build_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"🔨 Сборка Go-библиотеки в {build_dir}...")

        # Запуск сборки Go
        try:
            subprocess.run(
                ["go", "build", "-buildmode=c-shared", "-o", "libgo_sum.so"],
                cwd=build_dir,
                check=True,
                capture_output=True,
                text=True
            )
            print("✅ Go-библиотека собрана: libgo_sum.so")
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка сборки Go: {e.stderr}")
            raise
        except FileNotFoundError:
            print("❌ Go не найден. Установите Go: https://golang.org/dl/")
            raise

        # Создание Python-обёртки
        wrapper_code = '''"""
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
'''

        wrapper_path = os.path.join(build_dir, "go_sum.py")
        with open(wrapper_path, "w", encoding="utf-8") as f:
            f.write(wrapper_code)
        print("✅ Python-обёртка создана: go_sum.py")

        # Копирование библиотеки в директорию пакета
        lib_src = os.path.join(build_dir, "libgo_sum.so")
        lib_dst = os.path.join(build_dir, "libgo_sum.so")
        if os.path.exists(lib_src):
            shutil.copy2(lib_src, lib_dst)

        # Запуск стандартной сборки
        super().run()


setup(
    name="go_sum",
    version="1.0.0",
    description="Go-модуль для вычисления суммы квадратов чисел",
    author="Benchmark Project",
    py_modules=["go_sum"],
    cmdclass={
        "build_py": BuildGoExtension,
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Go",
    ],
)
