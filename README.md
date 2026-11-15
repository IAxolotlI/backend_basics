# Домашнее задание: SQLAlchemy и Alembic

## 1. Модели и репозитории
- **User**: `id`, `email`, `balance` (Numeric, NOT NULL). Связь `orders`.
- **Order**: `id`, `user_id` (FK на `users.id`, ondelete=CASCADE, index), `amount` (Numeric, NOT NULL), `status` (String(20), NOT NULL, server_default='pending'). Связь `user`.
- **Репозитории** (`app/repositories.py`): `UserRepository` (add, get_by_id, get_by_email), `OrderRepository` (add, find_for_user).

## 2. Начальная миграция
- `0001_initial`: создаёт таблицы `users` и `orders` с PK, FK, индексами и ограничениями (без колонки `status`).

## 3. Статус заказа и миграции
- `0002_add_status`: `ALTER TABLE orders ADD COLUMN status varchar(20) NOT NULL DEFAULT 'pending'`.
- В `alembic/env.py` модели импортируются до `context.configure`, чтобы `Base.metadata` был заполнен.
- Проверка цикла:
  - `alembic upgrade head` → у существующего заказа статус pending.
  - `alembic downgrade -1` → колонка удалена. Значения безвозвратно потеряны.
  - Повторный `alembic upgrade head` → снова `pending`. Это не восстановление исходных данных, цикл необратим по данным.

## 4. Атомарное создание заказа
- Граница транзакции в `app/service.py` (use case `create_order`): проверка суммы > 0, наличия пользователя и баланса → списание → вставка заказа → `session.commit()`. При исключении — `session.rollback()`.
- Тест `scripts/atomic_test.py`: намеренная ошибка (RuntimeError) между списанием и вставкой. Проверка в новой сессии показала: баланс не изменился (100.00), заказ не создан (0).

## 5. Исправление N+1
- Скрипт `scripts/n_plus_one.py` (5 пользователей, по 3 заказа).
- Для каждого варианта — свежая сессия, счётчик запросов сбрасывается.
- Наивный вариант (цикл по `user.orders`): 6 запросов (1 + 5).
- С `selectinload(User.orders)`: 2 запроса (1 основной + 1 пакетный `IN`).

## Запуск
1. `pip install -r requirements.txt`
2. `alembic upgrade head`
3. `python -m scripts.atomic_test`
4. `python -m scripts.n_plus_one_demo`