# Chereshnev_Denis_IKBO-71-25_Praktika2_Variant23

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
## Этап 2

Добавлен сбор прямых зависимостей Cargo-пакета через публичный API crates.io.

Приложение получает метаданные указанного пакета и выводит список
его прямых зависимостей.

## Пример

```bash
python -m src.cli \
  --package serde \
  --source [https://crates.io](https://crates.io) \
  --max-depth 3 \
  --filter "dev"
```

## Обработка ошибок

Программа обрабатывает:

- отсутствие пакета в crates.io;
- ошибки соединения с crates.io;
- HTTP-ошибки;
- некорректный JSON-ответ.

## Тестовый режим

В тестовом режиме запрос к crates.io не выполняется:

```bash
python -m src.cli \
  --package A \
  --source tests/test_graph.txt \
  --test \
  --max-depth 2 \
  --filter ""
```
## Получение зависимостей

Программа получает последнюю версию пакета из crates.io,
затем запрашивает зависимости этой версии через отдельный
эндпоинт crates.io.
## Этап 3

Добавлено построение графа зависимостей с использованием рекурсивного BFS.

Программа учитывает максимальную глубину анализа, исключает пакеты
по заданной подстроке и корректно обрабатывает циклические зависимости.

## Тестовый режим

```bash
python -m src.cli \
  --package A \
  --source tests/test_graph.txt \
  --test \
  --max-depth 3 \
  --filter ""
```

## Ограничение глубины

```bash
python -m src.cli \
  --package A \
  --source tests/test_graph.txt \
  --test \
  --max-depth 1 \
  --filter ""
```

## Фильтрация пакетов

```bash
python -m src.cli \
  --package A \
  --source tests/test_graph.txt \
  --test \
  --max-depth 3 \
  --filter "B"
```
## Этап 4

Добавлен вывод порядка загрузки зависимостей.

Порядок вычисляется топологической сортировкой: зависимости
выводятся раньше пакетов, которые их используют.

## Ациклический граф

```bash
python -m src.cli \
  --package A \
  --source tests/test_graph_acyclic.txt \
  --test \
  --max-depth 3 \
  --filter ""
```

## Циклический граф

Для графа с циклом программа сообщает об ошибке:

```bash
python -m src.cli \
  --package A \
  --source tests/test_graph.txt \
  --test \
  --max-depth 3 \
  --filter ""
```
