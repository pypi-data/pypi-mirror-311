from typing import Any

from pydantic import BaseModel

from pydantic_logic.expression import LogicExpression


class Logic(BaseModel):
    expressions: list[LogicExpression]

    def evaluate(self, data: dict[str, Any], *, default_if_empty: bool = False) -> bool:
        if len(self.expressions) == 0:
            return default_if_empty
        return all(expr.evaluate(data) for expr in self.expressions)

    def get_wrong_expressions(self, data: dict[str, Any]) -> list[LogicExpression]:
        return [expr for expr in self.expressions if not expr.evaluate(data)]
