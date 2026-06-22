# Как загрузить файлы в GitHub без проблемы со скрытой папкой `.github`

Есть две части.

Первая часть загружается обычным перетаскиванием:

```text
data
scripts
docs
results
```

Вторая часть, то есть файлы GitHub Actions, лучше создаётся руками через `Create new file`, потому что папка `.github` скрытая.

## Шаг 1. Загрузить обычные папки

Открой репозиторий:

```text
Grisha-Pochuev/minimum-link-covering-trail-4x4x4
```

Нажми:

```text
Add file -> Upload files
```

Перетащи туда эти папки из архива:

```text
data
scripts
docs
results
```

Внизу напиши коммит:

```text
Add checker and 22-link search scripts
```

Нажми `Commit changes`.

## Шаг 2. Создать короткий проверочный запуск

Нажми:

```text
Add file -> Create new file
```

В имя файла вставь:

```text
.github/workflows/check-and-short-search.yml
```

Потом открой файл из архива:

```text
workflow-file-to-create-manually/check-and-short-search.yml
```

Скопируй весь текст и вставь в большое поле на GitHub.

Внизу напиши коммит:

```text
Add short GitHub Actions search workflow
```

Нажми `Commit changes`.

## Шаг 3. Создать ночной запуск

Снова нажми:

```text
Add file -> Create new file
```

В имя файла вставь:

```text
.github/workflows/overnight-search.yml
```

Потом открой файл из архива:

```text
workflow-file-to-create-manually/overnight-search.yml
```

Скопируй весь текст и вставь в большое поле на GitHub.

Внизу напиши коммит:

```text
Add overnight 22-link search workflow
```

Нажми `Commit changes`.

## Шаг 4. Сначала проверить короткий запуск

Открой вкладку:

```text
Actions
```

Выбери:

```text
check-and-short-search
```

Нажми:

```text
Run workflow
```

Оставь значения по умолчанию. Дождись зелёной галочки.

## Шаг 5. Потом запускать ночной поиск

Открой:

```text
Actions -> overnight-22-search -> Run workflow
```

Оставь значения:

```text
seconds = 20400
box_min = -3
box_max = 7
top_k = 32
```

Нажми `Run workflow`.

После завершения открой запуск и скачай `Artifacts`.
