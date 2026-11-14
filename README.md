# Chereshnev Denis IKBO-71-25 Praktika 2 Variant 23

CLI-приложение для настройки анализа графа зависимостей пакетов Rust (Cargo).

## Этап 1

Реализован минимальный прототип с конфигурацией через опции командной строки.

Приложение принимает параметры, проверяет их корректность и выводит
конфигурацию в формате `ключ=значение`.

## Параметры

| Опция | Назначение |
|---|---|
| `--package` | Имя анализируемого пакета |
| `--source` | URL репозитория Cargo или путь к тестовому файлу |
| `--test` | Включает режим тестового репозитория |
| `--max-depth` | Максимальная глубина анализа зависимостей |
| `--filter` | Подстрока для исключения пакетов |

## Запуск

```bash
python -m src.cli \
  --package serde \
  --source [https://crates.io](https://crates.io) \
  --max-depth 3 \
  --filter "dev"
```

## Тестовый режим

```bash
python -m src.cli \
  --package A \
  --source tests/test_graph.txt \
  --test \
  --max-depth 2 \
  --filter ""
```

## Запуск через Makefile

```bash
make run
```

## Тесты

```bash
python -m pytest
```