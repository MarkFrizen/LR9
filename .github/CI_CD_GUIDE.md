# CI/CD Руководство

Автоматизация сборки, тестирования и публикации Rust-модуля **pyo3-sum**.

## Обзор Workflow

### 1. `rust_test.yml` — Тестирование

**Триггеры:**
- Push в ветки `main`, `master`, `develop`
- Pull Request в эти же ветки
- Изменения в `benchmark/pyo3-sum/`

**Задачи:**
| Job | Описание |
|-----|----------|
| `rust-test` | Проверка формата, clippy, Rust тесты |
| `python-integration` | Интеграционные тесты для Python 3.8-3.12 |
| `benchmark` | Бенчмарк производительности |

**Запуск вручную:**
```bash
# Не требуется, запускается автоматически при push
```

---

### 2. `publish_pypi.yml` — Публикация на PyPI

**Триггеры:**
- Публикация GitHub Release
- Ручной запуск через `workflow_dispatch`

**Задачи:**
| Job | Описание |
|-----|----------|
| `check-version` | Проверка соответствия версий в Cargo.toml и pyproject.toml |
| `build-wheels` | Сборка для Linux, Windows, macOS |
| `build-macos-universal` | Universal2 для Apple Silicon + Intel |
| `publish-pypi` | Публикация на PyPI (требуется OIDC) |
| `notify` | Уведомление о результате |

**Запуск вручную:**
```bash
# Через GitHub CLI
gh workflow run publish_pypi.yml -f version=0.1.0 -f dry_run=true

# Или через GitHub UI: Actions → Publish pyo3-sum to PyPI → Run workflow
```

**Подготовка к публикации:**

1. Обновите версию в `benchmark/pyo3-sum/Cargo.toml`:
   ```toml
   [package]
   name = "pyo3-sum"
   version = "0.2.0"  # ← обновите версию
   ```

2. Обновите версию в `benchmark/pyo3-sum/pyproject.toml`:
   ```toml
   [project]
   version = "0.2.0"  # ← та же версия
   ```

3. Закоммитьте изменения:
   ```bash
   git add benchmark/pyo3-sum/Cargo.toml benchmark/pyo3-sum/pyproject.toml
   git commit -m "Bump version to 0.2.0"
   git push
   ```

4. Создайте GitHub Release:
   ```bash
   gh release create v0.2.0 --title "Version 0.2.0" --generate-notes
   ```

   Или через GitHub UI: Releases → Draft a new release

---

### 3. `build_wheels.yml` — Кроссплатформенная сборка

**Триггеры:**
- Публикация GitHub Release
- Ручной запуск через `workflow_dispatch`

**Собираемые платформы:**

| ОС | Архитектуры |
|----|-------------|
| Linux | x86_64, aarch64, i686, armv7 (GNU + musl) |
| Windows | x86_64, i686, aarch64 |
| macOS | x86_64, aarch64, universal2 |

**Запуск вручную:**
```bash
# Сборка без публикации
gh workflow run build_wheels.yml -f publish=false

# Сборка с публикацией на GitHub Releases
gh workflow run build_wheels.yml -f publish=true
```

---

## Настройка PyPI

### Требуемые секреты

Для публикации на PyPI **не требуются секреты** — используется OIDC (OpenID Connect).

### Настройка окружения PyPI

1. Перейдите в репозиторий на GitHub
2. Settings → Environments → New environment
3. Name: `pypi`
4. Deployment branches: Selected branches → `main`
5. Save

### Настройка PyPI Trusted Publisher

1. Войдите на [pypi.org](https://pypi.org/)
2. Account Settings → API tokens
3. "Add API token" → "Trusted publisher"
4. Project name: `pyo3-sum`
5. Owner: ваш GitHub organization/user
6. Repository name: `your-repo`
7. Workflow name: `publish_pypi.yml`
8. Environment: `pypi`
9. Save

---

## Структура файлов

```
.github/
└── workflows/
    ├── rust_test.yml        # CI тестирование
    ├── publish_pypi.yml     # Публикация на PyPI
    └── build_wheels.yml     # Кроссплатформенная сборка

benchmark/pyo3-sum/
├── Cargo.toml               # Rust зависимости + версия
├── pyproject.toml           # Python метаданные + версия
├── README.md                # Документация пакета
├── LICENSE                  # Лицензия MIT
└── tests/
    └── test_python.py       # Python интеграционные тесты
```

---

## Отладка workflow

### Просмотр логов

```bash
# Список запусков workflow
gh run list --workflow rust_test.yml

# Просмотр конкретного запуска
gh run view <RUN_ID> --log

# Просмотр в реальном времени
gh run watch <RUN_ID>
```

### Локальное тестирование

Используйте [act](https://github.com/nektos/act) для локального запуска GitHub Actions:

```bash
# Установка act
brew install act  # macOS
# или
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Запуск workflow
act push        # Все workflow на push
act pull_request # Все workflow на PR

# Запуск конкретного workflow
act -j rust-test
```

---

## Чеклист перед публикацией

- [ ] Версии в `Cargo.toml` и `pyproject.toml` совпадают
- [ ] Все CI тесты проходят (`rust_test.yml`)
- [ ] README.md обновлён
- [ ] LICENSE присутствует
- [ ] Классификаторы в `pyproject.toml` актуальны
- [ ] PyPI Trusted Publisher настроен
- [ ] Создан GitHub Release с тегом версии

---

## Пример полного цикла публикации

```bash
# 1. Обновление версии
# Отредактируйте Cargo.toml и pyproject.toml

# 2. Проверка
cd benchmark/pyo3-sum
cargo test
maturin develop --release
python -m pytest tests/test_python.py

# 3. Коммит
git add .
git commit -m "Release version 0.2.0"
git push

# 4. Создание релиза
gh release create v0.2.0 --title "Version 0.2.0" --generate-notes

# 5. Мониторинг сборки
gh run watch

# 6. Проверка публикации
pip install pyo3-sum
python -c "import pyo3_sum; print(pyo3_sum.sum_of_squares(10))"
```

---

## Поддержка

При проблемах:
1. Проверьте логи workflow на GitHub
2. Убедитесь, что версии совпадают
3. Проверьте настройки PyPI Trusted Publisher
4. Попробуйте dry-run: `gh workflow run publish_pypi.yml -f dry_run=true`
