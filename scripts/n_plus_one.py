from decimal import Decimal

from sqlalchemy import event, select
from sqlalchemy.orm import selectinload

from app.db import SessionLocal
from app.models import Order, User


def seed() -> None:
    with SessionLocal() as s:
        for i in range(5):
            u = User(email=f"u{i}@example.com", balance=Decimal("100.00"))
            s.add(u)
            s.flush()
            for j in range(3):
                s.add(Order(user_id=u.id, amount=Decimal("10.00"), status="pending"))
        s.commit()


def count_queries(fn):
    counter = {"n": 0}
    with SessionLocal() as s:
        @event.listens_for(s.bind, "before_cursor_execute")
        def _inc(conn, cursor, stmt, params, ctx, many):
            counter["n"] += 1

        fn(s)
        event.remove(s.bind, "before_cursor_execute", _inc)
    return counter["n"]


def naive(s):
    users = s.scalars(select(User)).all()
    for u in users:
        _ = [o.amount for o in u.orders]


def optimized(s):
    users = s.scalars(select(User).options(selectinload(User.orders))).all()
    for u in users:
        _ = [o.amount for o in u.orders]


if __name__ == "__main__":
    seed()
    print("naive queries:    ", count_queries(naive))
    print("selectinload:     ", count_queries(optimized))