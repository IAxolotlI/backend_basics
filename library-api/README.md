## Запуск mock-сервера

```bash
npx @stoplight/prism-cli mock library-api/openapi.yaml
```

## Пример запроса (curl)

> Все эндпоинты защищены `BearerAuth`, поэтому Prism требует заголовок `Authorization`.
> В режиме мока принимается любой Bearer-токен.

```bash
# Создать книгу
curl -X POST http://localhost:4010/books \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-token" \
  -d '{"title":"1984","author":"Джордж Оруэлл","isbn":"978-5-17-118880-4","published_year":1949,"total_copies":3}'

# Создать выдачу с Idempotency-Key
curl -X POST http://localhost:4010/loans \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-token" \
  -H "Idempotency-Key: 7c9e6679-7425-40de-944b-e07fc1f90ae7" \
  -d '{"book_id":1,"reader_id":2,"due_date":"2027-01-01T12:00:00Z"}'

# Список просроченных
curl "http://localhost:4010/loans?status=overdue" \
  -H "Authorization: Bearer test-token"

# Возврат
curl -X POST http://localhost:4010/loans/5/return \
  -H "Authorization: Bearer test-token"
```

## Структура

- `openapi.yaml` — контракт
- `STYLE.md` — правила оформления API
- `REVIEW.md` — саморевью по чек-листу
