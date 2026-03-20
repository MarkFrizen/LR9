use pyo3::prelude::*;

/// Вычисляет сумму квадратов чисел от 1 до n
///
/// # Arguments
/// * `n` - Верхняя граница диапазона (включительно)
///
/// # Returns
/// Сумма квадратов чисел от 1 до n
#[pyfunction]
fn sum_of_squares(n: u64) -> u128 {
    (1..=n as u128).map(|x| x * x).sum()
}

/// Модуль pyo3_sum предоставляет функции для вычисления суммы квадратов
#[pymodule]
fn pyo3_sum(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_of_squares, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sum_of_squares_small() {
        assert_eq!(sum_of_squares(1), 1);
        assert_eq!(sum_of_squares(2), 5);
        assert_eq!(sum_of_squares(3), 14);
        assert_eq!(sum_of_squares(10), 385);
    }

    #[test]
    fn test_sum_of_squares_zero() {
        assert_eq!(sum_of_squares(0), 0);
    }
}
