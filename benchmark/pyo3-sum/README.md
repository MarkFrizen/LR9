# pyo3-sum

Высокопроизводительная Rust-библиотека для вычисления суммы квадратов чисел, доступная из Python через PyO3.

## Установка

```bash
pip install pyo3-sum
```

Или соберите локально:

```bash
# Установка зависимостей
pip install maturin

# Сборка и установка
maturin develop --release
```

## Использование

```python
from pyo3_sum import sum_of_squares

# Вычисление суммы квадратов от 1 до n
result = sum_of_squares(10)
print(result)  # 385 (1² + 2² + ... + 10²)

# Большие числа
result = sum_of_squares(1_000_000)
print(result)  # 333333833333500000
```

## Производительность

| Метод | Время (N=1_000_000) | Ускорение |
|-------|---------------------|-----------|
| pyo3-sum | ~0.02 сек | **2x** быстрее Python |
| Чистый Python | ~0.04 сек | 1.0x (базовый) |

## API

### `sum_of_squares(n: int) -> int`

Вычисляет сумму квадратов чисел от 1 до `n`.

**Аргументы:**
- `n` (int): Верхняя граница диапазона (включительно). Должно быть неотрицательным целым числом.

**Возвращает:**
- `int`: Сумма квадратов чисел от 1 до `n`.

**Пример:**
```python
>>> sum_of_squares(0)
0
>>> sum_of_squares(1)
1
>>> sum_of_squares(5)
55  # 1 + 4 + 9 + 16 + 25
>>> sum_of_squares(10)
385
```

## Сборка

### Требования

- Rust 1.70+ ([установка](https://rustup.rs/))
- Python 3.8+
- maturin: `pip install maturin`

### Локальная сборка

```bash
# Debug сборка (быстрее, для разработки)
maturin develop

# Release сборка (медленнее, оптимизирована)
maturin develop --release

# Сборка wheel
maturin build --release
```

### Кроссплатформенная сборка

Используйте GitHub Actions для сборки wheel'ов для всех платформ:

```bash
# Триггер для сборки (требуется GH CLI)
gh workflow run build_wheels.yml
```

## Тестирование

```bash
# Rust тесты
cargo test

# Python тесты
python -c "import pyo3_sum; assert pyo3_sum.sum_of_squares(10) == 385"
```

## Лицензия

MIT License - см. файл [LICENSE](LICENSE).

## Вклад в проект

1. Fork репозиторий
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## Бенчмарк

Для сравнения производительности с чистым Python и Go:

```bash
cd benchmark
python benchmark.py -n 1000000 -i 5
```

См. [benchmark/README.md](../../benchmark/README.md) для подробностей.
