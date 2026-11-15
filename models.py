from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class DrinkSize(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"


class OrderStatus(str, Enum):
    pending = "pending"
    ready = "ready"
    completed = "completed"
    cancelled = "cancelled"


class OrderCreate(BaseModel):
    drink: str = Field(
        min_length=1,
        max_length=100,
        description="Название напитка",
        examples=["Латте"],
    )
    size: DrinkSize = Field(
        description="Размер напитка",
        examples=["medium"],
    )
    quantity: int = Field(
        gt=0,
        description="Количество порций",
        examples=[2],
    )
    customer_name: str | None = Field(
        default=None,
        max_length=100,
        description="Имя клиента",
        examples=["Ирина"],
    )


class OrderUpdate(BaseModel):
    drink: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Название напитка",
        examples=["Капучино"],
    )
    size: DrinkSize | None = Field(
        default=None,
        description="Размер напитка",
        examples=["large"],
    )
    quantity: int | None = Field(
        default=None,
        gt=0,
        description="Количество порций",
        examples=[1],
    )
    customer_name: str | None = Field(
        default=None,
        max_length=100,
        description="Имя клиента",
        examples=["Матвей"],
    )
    status: OrderStatus | None = Field(
        default=None,
        description="Статус заказа",
        examples=["ready"],
    )


class Order(BaseModel):
    id: int = Field(description="Идентификатор заказа", examples=[1])
    drink: str = Field(description="Название напитка из меню", examples=["Латте"])
    size: DrinkSize = Field(description="Размер напитка", examples=["medium"])
    quantity: int = Field(description="Количество порций", examples=[2])
    customer_name: str | None = Field(
        default=None, description="Имя клиента", examples=["Ирина"]
    )
    status: OrderStatus = Field(
        description="Статус заказа", examples=["pending"]
    )
    created_at: datetime = Field(
        description="Метка времени создания заказа",
        examples=["2026-07-10T09:15:00"],
    )