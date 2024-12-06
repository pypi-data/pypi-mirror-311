from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel
from typing_extensions import Self


class Operator(Enum):
    EQ = "eq"
    NE = "ne"
    GT = "gt"
    GE = "ge"
    LT = "lt"
    LE = "le"


class ExpressionType(Enum):
    COMPARISON = "comparison"
    # TODO: logic(any, all), and maybe more..


class LogicExpression(BaseModel):
    type: Literal[ExpressionType.COMPARISON] = ExpressionType.COMPARISON
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
