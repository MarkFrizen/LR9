#!/usr/bin/env python3
"""
Бенчмарк производительности трёх решений для вычисления суммы квадратов чисел.

Сравниваются:
1. Чистый Python
2. Python + Rust (PyO3)
3. Python + Go (cgo)

Вычисляется сумма квадратов чисел от 1 до N (по умолчанию 10_000_000).
"""

import time
import argparse
import sys
import csv
from typing import Callable, Tuple, Dict, List
from datetime import datetime

# Опциональный импорт matplotlib для графиков
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# Попытка импорта Rust-модуля
try:
    import pyo3_sum
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False
    print("⚠️  Модуль pyo3_sum не найден. Установите: cd benchmark/pyo3-sum && maturin develop")

# Попытка импорта Go-модуля
try:
    import go_sum
    GO_AVAILABLE = True
except ImportError:
    GO_AVAILABLE = False
    print("⚠️  Модуль go_sum не найден. Установите: cd benchmark/go-sum && bash build.sh")


def sum_of_squares_python(n: int) -> int:
    """Вычисление суммы квадратов на чистом Python."""
    return sum(i * i for i in range(1, n + 1))


def sum_of_squares_python_formula(n: int) -> int:
    """Вычисление суммы квадратов по формуле (оптимизированный Python)."""
    return n * (n + 1) * (2 * n + 1) // 6


def benchmark(func: Callable[[int], int], n: int, name: str, iterations: int = 3) -> Tuple[float, int, List[float]]:
    """
    Бенчмарк функции.

    Args:
        func: Функция для бенчмарка
        n: Верхняя граница диапазона
        name: Название функции для вывода
        iterations: Количество итераций для усреднения

    Returns:
        Кортеж (среднее время, результат функции, список всех времён)
    """
    print(f"\n📊 Бенчмарк: {name}")
    print(f"   Диапазон: 1..{n:,}")
    print(f"   Итераций: {iterations}")

    times = []
    result = None

    for i in range(iterations):
        start = time.perf_counter()
        result = func(n)
        end = time.perf_counter()
        elapsed = end - start
        times.append(elapsed)
        print(f"   Итерация {i + 1}: {elapsed:.6f} сек")

    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)

    print(f"\n   ✅ Результат: {result:,}")
    print(f"   ⏱️  Среднее время: {avg_time:.6f} сек")
    print(f"   ⏱️  Минимальное: {min_time:.6f} сек")
    print(f"   ⏱️  Максимальное: {max_time:.6f} сек")

    return avg_time, result, times


def run_benchmark(n: int, iterations: int, include_formula: bool = False,
                  save_csv: bool = True, save_plot: bool = True) -> Dict:
    """
    Запуск полного бенчмарка всех доступных реализаций.

    Args:
        n: Верхняя граница диапазона
        iterations: Количество итераций для усреднения
        include_formula: Включить бенчмарк формулы
        save_csv: Сохранить результаты в CSV
        save_plot: Сохранить график

    Returns:
        Словарь с результатами бенчмарка
    """
    print("=" * 60)
    print("🚀 БЕНЧМАРК: Сумма квадратов чисел")
    print("=" * 60)

    results: Dict[str, float] = {}
    all_times: Dict[str, List[float]] = {}
    reference_result = None

    # 1. Чистый Python
    print("\n" + "=" * 60)
    print("1️⃣  ЧИСТЫЙ PYTHON")
    print("=" * 60)
    avg_time, result, times = benchmark(sum_of_squares_python, n, "sum_of_squares_python", iterations)
    results["Python"] = avg_time
    all_times["Python"] = times
    reference_result = result

    # 1b. Python с формулой (опционально)
    if include_formula:
        print("\n" + "=" * 60)
        print("1️⃣b PYTHON (ФОРМУЛА)")
        print("=" * 60)
        avg_time, result, times = benchmark(sum_of_squares_python_formula, n, "sum_of_squares_python_formula", iterations)
        results["Python (formula)"] = avg_time
        all_times["Python (formula)"] = times
        if reference_result is None:
            reference_result = result

    # 2. Python + Rust (PyO3)
    if RUST_AVAILABLE:
        print("\n" + "=" * 60)
        print("2️⃣  PYTHON + RUST (PyO3)")
        print("=" * 60)
        avg_time, result, times = benchmark(pyo3_sum.sum_of_squares, n, "pyo3_sum.sum_of_squares", iterations)
        results["Rust (PyO3)"] = avg_time
        all_times["Rust (PyO3)"] = times

        # Проверка корректности результата
        if result != reference_result:
            print(f"\n   ⚠️  ВНИМАНИЕ: Результат Rust отличается!")
            print(f"   Ожидалось: {reference_result:,}")
            print(f"   Получено:  {result:,}")
    else:
        print("\n" + "=" * 60)
        print("2️⃣  PYTHON + RUST (PyO3) — ПРОПУЩЕНО (модуль не установлен)")
        print("=" * 60)

    # 3. Python + Go (cgo)
    if GO_AVAILABLE:
        print("\n" + "=" * 60)
        print("3️⃣  PYTHON + GO (cgo)")
        print("=" * 60)
        avg_time, result, times = benchmark(go_sum.sum_of_squares, n, "go_sum.sum_of_squares", iterations)
        results["Go (cgo)"] = avg_time
        all_times["Go (cgo)"] = times

        # Проверка корректности результата
        if result != reference_result:
            print(f"\n   ⚠️  ВНИМАНИЕ: Результат Go отличается!")
            print(f"   Ожидалось: {reference_result:,}")
            print(f"   Получено:  {result:,}")
    else:
        print("\n" + "=" * 60)
        print("3️⃣  PYTHON + GO (cgo) — ПРОПУЩЕНО (модуль не установлен)")
        print("=" * 60)

    # Итоговая таблица
    print("\n" + "=" * 60)
    print("📈 ИТОГОВАЯ ТАБЛИЦА")
    print("=" * 60)

    if len(results) > 1:
        python_time = results.get("Python", float("inf"))

        print(f"\n{'Метод':<25} {'Время (сек)':<15} {'Относительно Python':<20}")
        print("-" * 60)

        for method, time_val in sorted(results.items(), key=lambda x: x[1]):
            if method == "Python":
                ratio = 1.0
            else:
                ratio = time_val / python_time if python_time > 0 else float("inf")

            speedup = python_time / time_val if time_val > 0 else float("inf")

            if method == "Python":
                print(f"{method:<25} {time_val:<15.6f} {'1.00x (базовый)':<20}")
            else:
                if time_val < python_time:
                    print(f"{method:<25} {time_val:<15.6f} {speedup:.2f}x быстрее{'>':<10}")
                else:
                    print(f"{method:<25} {time_val:<15.6f} {ratio:.2f}x медленнее{'':<8}")
    else:
        print("\nДоступен только один метод — сравнение невозможно.")

    print("\n" + "=" * 60)
    print("✅ Бенчмарк завершён")
    print("=" * 60)

    # Сохранение результатов
    benchmark_data = {
        "results": results,
        "all_times": all_times,
        "n": n,
        "iterations": iterations,
        "timestamp": datetime.now().isoformat()
    }

    if save_csv and results:
        save_to_csv(benchmark_data)

    if save_plot and results and MATPLOTLIB_AVAILABLE:
        save_plot_fig(benchmark_data)
    elif save_plot and results and not MATPLOTLIB_AVAILABLE:
        print("\n⚠️  Matplotlib не установлен. График не будет сохранён.")
        print("   Установите: pip install matplotlib")

    return benchmark_data


def save_to_csv(data: Dict) -> str:
    """Сохраняет результаты бенчмарка в CSV файл."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"benchmark_results_{timestamp}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Benchmark Results - Sum of Squares"])
        writer.writerow(["Timestamp", data["timestamp"]])
        writer.writerow(["N", f"{data['n']:,}"])
        writer.writerow(["Iterations", data["iterations"]])
        writer.writerow([])
        writer.writerow(["Method", "Avg Time (s)", "Min Time (s)", "Max Time (s)"])

        for method, times in data["all_times"].items():
            avg_t = sum(times) / len(times)
            min_t = min(times)
            max_t = max(times)
            writer.writerow([method, f"{avg_t:.6f}", f"{min_t:.6f}", f"{max_t:.6f}"])

        writer.writerow([])
        writer.writerow(["Performance Comparison"])
        python_time = data["results"].get("Python", 1)
        for method, time_val in data["results"].items():
            if method == "Python":
                ratio = 1.0
            else:
                ratio = time_val / python_time if python_time > 0 else float("inf")
            speedup = python_time / time_val if time_val > 0 else float("inf")
            writer.writerow([method, f"{time_val:.6f}", f"{speedup:.2f}x speedup"])

    print(f"\n📁 Результаты сохранены в: {filename}")
    return filename


def save_plot_fig(data: Dict) -> str:
    """Сохраняет график производительности."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"benchmark_plot_{timestamp}.png"

    methods = list(data["results"].keys())
    times = list(data["results"].values())

    # Определяем цвета
    colors = []
    for method in methods:
        if "Python" in method and "formula" not in method.lower():
            colors.append("#FF6B6B")  # Красный для чистого Python
        elif "Rust" in method:
            colors.append("#FFA502")  # Оранжевый для Rust
        elif "Go" in method:
            colors.append("#70A1FF")  # Синий для Go
        elif "formula" in method.lower():
            colors.append("#2ED573")  # Зелёный для формулы
        else:
            colors.append("#CCCCCC")  # Серый для остальных

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # График 1: Среднее время по методам
    ax1 = axes[0]
    bars = ax1.bar(methods, times, color=colors, edgecolor="black", linewidth=1.2)
    ax1.set_ylabel("Время (сек)", fontsize=11)
    ax1.set_title(f"Сравнение производительности\n(N = {data['n']:,}, {data['iterations']} итераций)", fontsize=12)
    ax1.tick_params(axis="x", rotation=15)

    # Добавляем значения на столбцы
    for bar, time_val in zip(bars, times):
        height = bar.get_height()
        ax1.annotate(f"{time_val:.4f}s",
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha="center", va="bottom", fontsize=10)

    # График 2: Относительная производительность (speedup)
    ax2 = axes[1]
    python_time = data["results"].get("Python", 1)
    speedups = [python_time / t if t > 0 else float("inf") for t in times]

    bars2 = ax2.bar(methods, speedups, color=colors, edgecolor="black", linewidth=1.2)
    ax2.set_ylabel("Speedup (относительно Python)", fontsize=11)
    ax2.set_title("Ускорение относительно чистого Python", fontsize=12)
    ax2.tick_params(axis="x", rotation=15)
    ax2.axhline(y=1.0, color="red", linestyle="--", linewidth=1, alpha=0.7, label="Базовый Python")

    # Добавляем значения на столбцы
    for bar, speedup in zip(bars2, speedups):
        height = bar.get_height()
        ax2.annotate(f"{speedup:.2f}x",
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha="center", va="bottom", fontsize=10)

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"📊 График сохранён в: {filename}")
    return filename


def main():
    parser = argparse.ArgumentParser(
        description="Бенчмарк производительности для вычисления суммы квадратов",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python benchmark.py                    # По умолчанию N=10_000_000
  python benchmark.py -n 1000000         # N=1_000_000
  python benchmark.py -n 10000000 -i 5   # N=10_000_000, 5 итераций
  python benchmark.py --formula          # Включить тест формулы
  python benchmark.py --no-plot          # Без сохранения графика
  python benchmark.py --no-csv           # Без сохранения CSV
        """
    )

    parser.add_argument(
        "-n", "--number",
        type=int,
        default=10_000_000,
        help="Верхняя граница диапазона (по умолчанию: 10_000_000)"
    )

    parser.add_argument(
        "-i", "--iterations",
        type=int,
        default=3,
        help="Количество итераций для усреднения (по умолчанию: 3)"
    )

    parser.add_argument(
        "--formula",
        action="store_true",
        help="Включить бенчмарк оптимизированной формулы Python"
    )

    parser.add_argument(
        "--no-csv",
        action="store_true",
        help="Не сохранять результаты в CSV"
    )

    parser.add_argument(
        "--no-plot",
        action="store_true",
        help="Не сохранять график"
    )

    args = parser.parse_args()

    print(f"\n📋 Параметры бенчмарка:")
    print(f"   N = {args.number:,}")
    print(f"   Итерации = {args.iterations}")
    print(f"   Формула = {'включена' if args.formula else 'выключена'}")
    print(f"   CSV = {'выключен' if args.no_csv else 'включён'}")
    print(f"   График = {'выключен' if args.no_plot else 'включён'}")

    run_benchmark(args.number, args.iterations, args.formula,
                  save_csv=not args.no_csv, save_plot=not args.no_plot)


if __name__ == "__main__":
    main()
