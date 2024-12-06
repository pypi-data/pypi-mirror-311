from enum import Enum
from typing import Any

from pydantic import BaseModel
from typing_extensions import Self


class Operator(Enum):
    EQ = "eq"
    NE = "ne"
    GT = "gt"
    GE = "ge"
    LT = "lt"
    LE = "le"


class LogicExpression(BaseModel):
    key: str
    operator: Operator
    value: str | int | float | bool | None

    @classmethod
    def b(cls, key: str, operator: Operator, value: str | int | float | bool) -> Self:
        return cls(key=key, operator=operator, value=value)

    def evaluate(self, data: dict[str, Any]) -> bool:
        value_to_compare = data.get(self.key)
        try:
            match self.operator:
                case Operator.EQ:
                    return value_to_compare == self.value  # type: ignore[operator]
                case Operator.NE:
                    return value_to_compare != self.value  # type: ignore[operator]
                case Operator.GT:
                    return value_to_compare > self.value  # type: ignore[operator]
                case Operator.GE:
                    return value_to_compare >= self.value  # type: ignore[operator]
                case Operator.LT:
                    return value_to_compare < self.value  # type: ignore[operator]
                case Operator.LE:
                    return value_to_compare <= self.value  # type: ignore[operator]
        except TypeError:
            return False

        return False
