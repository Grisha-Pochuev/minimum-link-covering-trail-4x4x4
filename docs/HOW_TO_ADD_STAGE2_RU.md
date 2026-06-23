# Как добавить второй этап в репозиторий

Нужно добавить три обычных файла и один скрытый файл GitHub Actions.

## 1. Обычные файлы

Через `Add file -> Upload files` можно перетащить:

```text
scripts/search_22_parallel.py
scripts/analyze_22_results.py
docs/NEXT_STAGE_RU.md
docs/HOW_TO_ADD_STAGE2_RU.md
```

Коммит можно назвать так:

```text
Add parallel 22-link search stage
```

## 2. Скрытый файл workflow

Файл в папке `.github` лучше создать руками.

Нажмите:

```text
Add file -> Create new file
```

В имя файла вставьте:

```text
.github/workflows/overnight-parallel-search.yml
```

Потом скопируйте туда содержимое файла:

```text
.github/workflows/overnight-parallel-search.yml
```

Коммит можно назвать так:

```text
Add parallel overnight search workflow
```

## 3. Первый запуск

Откройте:

```text
Actions -> overnight-22-parallel-search -> Run workflow
```

Оставьте значения по умолчанию.

Если будет зеленая галочка, скачайте артефакты `parallel-22-shard-*`.
