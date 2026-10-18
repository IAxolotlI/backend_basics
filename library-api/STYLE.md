# API Style Guide (Library API)

1. **URL — kebab-case, множественное число.** `/books`, `/readers`, `/loans`, `/loans/{id}/return`.
2. **JSON — snake_case.** `book_id`, `due_date`, `available_copies`, `registered_at`.
3. **Версия в URL.** Все пути монтируются под `/v1/`.
4. **Серверные поля — readOnly.** `id`, `registered_at`, `loaned_at`, `returned_at`, `available_copies` не принимаются от клиента.
5. **Запрет неизвестных полей.** Все request-схемы: `additionalProperties: false`.
6. **Единый формат ошибок.** `ErrorResponse { code, message, details? }`, коды — из фиксированного enum.
7. **Коды ответов осмысленные.** 200 — чтение/обновление, 201 — создание, 204 — удаление, 404 — не найдено, 409 — конфликт/идемпотентность, 422 — бизнес-правила/валидация.

8. **Коллекции — пагинация и сортировка.** `page`, `page_size`, `sort=<field>:<dir>`, ответ `{ items, page, page_size, total }`.
