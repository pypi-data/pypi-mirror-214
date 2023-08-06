from __future__ import annotations

from repleno.item import Item
from datetime import datetime, date
from enum import Enum


class OrderType(Enum):
    WORK_ORDER = "Work Order"
    PURCHASE_ORDER = "Purchase Order"
    NOT_SET = "Not set"


class Order:
    def __init__(self, item, due_date, qty, type=OrderType.NOT_SET):
        if not isinstance(item, Item):
            raise TypeError("item must be of Item type")

        self._item = item
        self.due_date = due_date
        self.qty = qty
        self.type = type

    def __repr__(self) -> str:
        return f"Order(item=Item({self._item}), due_date={self._due_date:%Y-%m-%d}, qty={self._qty}, type={self._type})"

    def __str__(self) -> str:
        return f"{self._qty} of {self._item} on {self._due_date:%Y-%m-%d}"

    def __eq__(self, other: Order) -> bool:
        if isinstance(other, Order):
            return (
                self.item == other.item
                and self.due_date == other.due_date
                and self.qty == other.qty
            )
        return False

    @property
    def item(self):
        return self._item

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        if not isinstance(value, (datetime, date)):
            raise TypeError("due date must a datetime or date object.")

        self._due_date = value

    @property
    def qty(self):
        return self._qty

    @qty.setter
    def qty(self, value):
        try:
            value = float(value)
        except TypeError:
            print("order qty must be an integer or a float.")
            raise
        if value < 0:
            return ValueError(f"order qty must be a positive number.")

        self._qty = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if not isinstance(value, OrderType):
            raise TypeError("Value must be of type OrderType.")

        self._type = value
