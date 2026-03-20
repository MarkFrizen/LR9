# pyo3-person

Rust-библиотека с использованием PyO3 и Maturin, которая экспортирует класс `Person` в Python.

## Требования

- **Rust** — установите с https://rustup.rs/
- **Python 3.8+**
- **Maturin** — устанавливается автоматически

## Сборка и установка

```bash
# Перейдите в директорию проекта
cd pyo3-person

# Создайте виртуальное окружение (опционально, но рекомендуется)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate     # Windows

# Установите maturin и соберите модуль
pip install maturin
maturin develop
```

## Запуск примера

```bash
python example_rust.py
```

## Запуск тестов

```bash
pip install pytest
pytest tests/
```

## Использование

```python
from pyo3_person import Person, older

# Создание экземпляра
person = Person("Alice", 25)

# Поля
print(person.name)  # Alice
print(person.age)   # 25

# Методы
print(person.greet())        # Hello, I'm Alice, age 25
person.have_birthday()
print(person.age)            # 26

# Сравнение возрастов
p1 = Person("Bob", 30)
p2 = Person("Charlie", 25)
print(older(p1, p2))  # True
```

## API

### Класс `Person`

| Поле/Метод | Описание |
|------------|----------|
| `name: str` | Имя человека (чтение/запись) |
| `age: int` | Возраст (чтение/запись) |
| `greet() -> str` | Возвращает приветствие |
| `have_birthday() -> None` | Увеличивает возраст на 1 |

### Функция `older`

| Функция | Описание |
|---------|----------|
| `older(p1: Person, p2: Person) -> bool` | `True`, если `p1` старше `p2` |

## Структура проекта

```
pyo3-person/
├── Cargo.toml          # Конфигурация Rust
├── pyproject.toml      # Конфигурация Maturin
├── src/
│   └── lib.rs          # Исходный код Rust
├── tests/
│   └── test_person.py  # Python-тесты
├── example_rust.py     # Пример использования
└── README.md
```
