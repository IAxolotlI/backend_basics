from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Order, User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, email: str, balance) -> User:
        user = User(email=email, balance=balance)
        self.session.add(user)
        return user

    def get_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.session.scalar(select(User).where(User.email == email))


class OrderRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, user_id: int, amount, status: str = "pending") -> Order:
        order = Order(user_id=user_id, amount=amount, status=status)
        self.session.add(order)
        return order

    def find_for_user(self, user_id: int) -> list[Order]:
        return list(
            self.session.scalars(
                select(Order).where(Order.user_id == user_id)
            ).all()
        )