#!/usr/bin/env python3
"""
Пример использования Rust-модуля pyo3_person из Python.

Перед запуском убедитесь, что модуль собран:
    cd pyo3-person
    maturin develop
"""

from pyo3_person import Person, older


def main():
    # Создание экземпляров Person
    alice = Person("Alice", 25)
    bob = Person("Bob", 30)

    # Доступ к полям
    print(f"Имя Alice: {alice.name}")
    print(f"Возраст Alice: {alice.age}")

    # Метод greet
    print(alice.greet())
    print(bob.greet())

    # День рождения
    print(f"\n{alice.name} празднует день рождения!")
    alice.have_birthday()
    print(f"Теперь {alice.name} {alice.age} лет")
    print(alice.greet())

    # Изменение полей
    print("\nИзменяем имя и возраст:")
    alice.name = "Alicia"
    alice.age = 27
    print(f"Новое имя: {alice.name}, возраст: {alice.age}")

    # Сравнение возрастов с функцией older
    print("\n--- Сравнение возрастов ---")
    p1 = Person("Charlie", 35)
    p2 = Person("Diana", 28)

    print(f"{p1.name} ({p1.age} лет) и {p2.name} ({p2.age} лет)")
    print(f"older({p1.name}, {p2.name}) = {older(p1, p2)}")

    p3 = Person("Eve", 20)
    p4 = Person("Frank", 45)
    print(f"\n{p3.name} ({p3.age} лет) и {p4.name} ({p4.age} лет)")
    print(f"older({p3.name}, {p4.name}) = {older(p3, p4)}")

    # Одинаковый возраст
    p5 = Person("George", 30)
    p6 = Person("Helen", 30)
    print(f"\n{p5.name} ({p5.age} лет) и {p6.name} ({p6.age} лет)")
    print(f"older({p5.name}, {p6.name}) = {older(p5, p6)}")


if __name__ == "__main__":
    main()
