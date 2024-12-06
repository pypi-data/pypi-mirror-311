from typing import Any

from pydantic import BaseModel

from pydantic_logic.expression import LogicExpression


class Logic(BaseModel):
    expressions: list[LogicExpression]

    def evaluate(self, data: dict[str, Any]) -> bool:
        return all(expr.evaluate(data) for expr in self.expressions)
