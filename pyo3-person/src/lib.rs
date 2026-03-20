use pyo3::prelude::*;

/// Класс Person для представления человека с именем и возрастом
#[pyclass]
pub struct Person {
    #[pyo3(get, set)]
    name: String,
    #[pyo3(get, set)]
    age: u32,
}

#[pymethods]
impl Person {
    /// Создаёт новый экземпляр Person
    ///
    /// # Arguments
    /// * `name` - Имя человека
    /// * `age` - Возраст человека
    ///
    /// # Returns
    /// Новый экземпляр Person
    #[new]
    fn new(name: String, age: u32) -> Self {
        Person { name, age }
    }

    /// Возвращает приветственное сообщение
    ///
    /// # Returns
    /// Строка вида "Hello, I'm {name}, age {age}"
    fn greet(&self) -> String {
        format!("Hello, I'm {}, age {}", self.name, self.age)
    }

    /// Увеличивает возраст на 1 (день рождения)
    fn have_birthday(&mut self) {
        self.age += 1;
    }
}

/// Сравнивает возраст двух людей и возвращает true, если p1 старше p2
#[pyfunction]
fn older(p1: &Person, p2: &Person) -> bool {
    p1.age > p2.age
}

/// Модуль pyo3_person предоставляет класс Person для Python
#[pymodule]
fn pyo3_person(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Person>()?;
    m.add_function(wrap_pyfunction!(older, m)?)?;
    Ok(())
}
