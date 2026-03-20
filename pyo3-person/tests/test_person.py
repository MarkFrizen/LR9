import pytest
from pyo3_person import Person, older


class TestPerson:
    """Тесты для класса Person"""

    def test_new_person(self):
        """Тест создания нового человека"""
        person = Person("Alice", 25)
        assert person.name == "Alice"
        assert person.age == 25

    def test_greet(self):
        """Тест метода greet"""
        person = Person("Bob", 30)
        assert person.greet() == "Hello, I'm Bob, age 30"

    def test_have_birthday(self):
        """Тест метода have_birthday"""
        person = Person("Charlie", 40)
        initial_age = person.age
        person.have_birthday()
        assert person.age == initial_age + 1

    def test_have_birthday_multiple_times(self):
        """Тест multiple вызовов have_birthday"""
        person = Person("Diana", 20)
        person.have_birthday()
        person.have_birthday()
        person.have_birthday()
        assert person.age == 23

    def test_greet_after_birthday(self):
        """Тест greet после дня рождения"""
        person = Person("Eve", 25)
        assert person.greet() == "Hello, I'm Eve, age 25"
        person.have_birthday()
        assert person.greet() == "Hello, I'm Eve, age 26"

    def test_set_name(self):
        """Тест изменения имени"""
        person = Person("Frank", 35)
        person.name = "George"
        assert person.name == "George"

    def test_set_age(self):
        """Тест изменения возраста"""
        person = Person("Helen", 28)
        person.age = 30
        assert person.age == 30

    def test_empty_name(self):
        """Тест с пустым именем"""
        person = Person("", 0)
        assert person.name == ""
        assert person.age == 0
        assert person.greet() == "Hello, I'm , age 0"

    def test_large_age(self):
        """Тест с большим возрастом"""
        person = Person("Old", 999)
        assert person.age == 999
        person.have_birthday()
        assert person.age == 1000


class TestOlder:
    """Тесты для функции older"""

    def test_older_true(self):
        """Тест когда первый старше"""
        p1 = Person("Alice", 30)
        p2 = Person("Bob", 25)
        assert older(p1, p2) is True

    def test_older_false_younger(self):
        """Тест когда первый младше"""
        p1 = Person("Charlie", 20)
        p2 = Person("Diana", 25)
        assert older(p1, p2) is False

    def test_older_false_same_age(self):
        """Тест когда одинаковый возраст"""
        p1 = Person("Eve", 30)
        p2 = Person("Frank", 30)
        assert older(p1, p2) is False

    def test_older_with_birthday(self):
        """Тест older после дня рождения"""
        p1 = Person("George", 25)
        p2 = Person("Helen", 26)
        assert older(p1, p2) is False
        p1.have_birthday()
        assert older(p1, p2) is False  # теперь оба 26
        p1.have_birthday()
        assert older(p1, p2) is True  # p1 стал 27
