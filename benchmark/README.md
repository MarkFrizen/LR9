# Бенчмарк производительности: Sum of Squares

Сравнение производительности трёх подходов для вычисления суммы квадратов чисел от 1 до N:

1. **Чистый Python** - интерпретируемый код
2. **Python + Rust (PyO3)** - нативное расширение на Rust
3. **Python + Go (cgo)** - нативное расширение на Go с cgo

## Структура

```
benchmark/
├── benchmark.py          # Основной скрипт бенчмарка
├── pyo3-sum/             # Rust модуль
│   ├── Cargo.toml
│   ├── pyproject.toml
│   └── src/
│       └── lib.rs
└── go-sum/               # Go модуль
    ├── go.mod
    ├── go_sum.go
    ├── setup.py
    └── build.sh
```

## Установка и запуск

### 1. Подготовка окружения

```bash
cd benchmark

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
```

### 2. Установка Rust модуля (PyO3)

```bash
# Установка Rust (если не установлен)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Сборка и установка pyo3-sum
cd pyo3-sum
pip install maturin
maturin develop
cd ..
```

### 3. Установка Go модуля (cgo)

```bash
# Установка Go (если не установлен)
# Ubuntu/Debian:
sudo apt-get update && sudo apt-get install -y golang-go

# Или через snap:
sudo snap install go --classic

# Сборка и установка go-sum
cd go-sum
bash build.sh
cd ..
```

### 4. Запуск бенчмарка

```bash
# Установка зависимостей для графиков
pip install matplotlib

# Запуск с параметрами по умолчанию (N=10_000_000)
python benchmark.py

# Свой размер N и количество итераций
python benchmark.py -n 1000000 -i 5

# С тестом формулы Python
python benchmark.py --formula
```

## Параметры командной строки

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `-n, --number` | Верхняя граница диапазона | 10_000_000 |
| `-i, --iterations` | Количество итераций | 3 |
| `--formula` | Включить тест формулы Python | выключена |
| `--no-csv` | Не сохранять CSV | включён |
| `--no-plot` | Не сохранять график | включён |

## Быстрый старт (без Rust и Go)

Если Rust и Go не установлены, бенчмарк всё равно можно запустить — будут протестированы только реализации на Python:

```bash
# Запуск только с чистым Python
python benchmark.py -n 1000000

# С тестом оптимизированной формулы
python benchmark.py --formula -n 1000000
```

## Выходные данные

После запуска бенчмарка создаются:

- `benchmark_results_YYYYMMDD_HHMMSS.csv` - результаты с временами
- `benchmark_plot_YYYYMMDD_HHMMSS.png` - график сравнения

## Пример результатов

```
Метод                     Время (сек)     Относительно Python
------------------------------------------------------------
Go (cgo)                  0.010522        46.88x быстрее>
Rust (PyO3)               0.199767        2.47x быстрее>
Python                    0.493268        1.00x (базовый)
```

**Примечание:** Go (cgo) показывает наилучшую производительность благодаря:
- Минимальным накладным расходам при вызове C-функции
- Оптимизации компилятора GCC (-O3)
- Отсутствию накладных расходов PyO3

## Как это работает

### Чистый Python
```python
def sum_of_squares_python(n: int) -> int:
    return sum(i * i for i in range(1, n + 1))
```

### Rust (PyO3)
```rust
#[pyfunction]
fn sum_of_squares(n: u64) -> u128 {
    (1..=n as u128).map(|x| x * x).sum()
}
```

### Go (cgo)
```go
//export sum_of_squares
func sum_of_squares(n C.ulonglong) C.ulonglong {
    var sum C.ulonglong
    for i := C.ulonglong(1); i <= n; i++ {
        sum += i * i
    }
    return sum
}
```

## Ожидаемая производительность

| Метод | Относительная скорость | Примечание |
|-------|----------------------|------------|
| Python | 1.0x (базовый) | Интерпретируемый код |
| Rust (PyO3) | 2-5x быстрее | Компилированный код, оптимизации LLVM |
| Go (cgo) | 10-50x быстрее | Компилированный код, минимальные накладные расходы |

**Примечание:** Фактическая производительность зависит от:
- Размера N (большие числа показывают большую разницу)
- Компилятора и флагов оптимизации
- Аппаратного обеспечения

## Требования

- Python 3.8+
- Rust 1.70+ (для pyo3-sum)
- Go 1.22+ (для go-sum)
- matplotlib (для графиков)
