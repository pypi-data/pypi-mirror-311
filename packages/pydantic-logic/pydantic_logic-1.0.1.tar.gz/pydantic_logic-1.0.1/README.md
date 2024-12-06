<div align="center">
  <h1>pydantic-logic</h1>
  <p>
    <img alt="License: MIT" src="https://img.shields.io/github/license/barabum0/pydantic-logic">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/barabum0/pydantic-logic">
    <a href="https://pypi.org/project/pydantic-logic">
        <img alt="PyPI version" src="https://img.shields.io/pypi/v/pydantic-logic.svg?logo=pypi&logoColor=FFE873">
    </a>
    <a href="https://github.com/psf/black">
        <img alt="code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
    </a>
    <a href="https://github.com/PyCQA/isort">
        <img alt="formatted with: isort" src="https://img.shields.io/badge/formatted%20with-isort-blue.svg">
    </a>
    <a href="https://mypy-lang.org/">
        <img alt="mypy: checked" src="https://www.mypy-lang.org/static/mypy_badge.svg">
    </a>
  </p>
</div>
Build complex rules, operate them with Pydantic, and execute them in Python

## Installation
```shell
pip install pydantic-logic
```

## Examples

### True expression
```python
from pydantic_logic import Logic, LogicExpression, Operator

data = {
    "Phone number": "123123123",
    "some_value": True,
    "some_other_value": 1,
}

logic = Logic(
    expressions=[
        LogicExpression.b("Phone number", Operator.NE, "adasdasdasd"),
        LogicExpression.b("some_value", Operator.EQ, True),
        LogicExpression.b("some_other_value", Operator.GT, 0),
    ]
)
assert logic.evaluate(data)
```

### False expression
```python
from pydantic_logic import Logic, LogicExpression, Operator

data = {
    "Phone number": "123123123",
    "some_value": True,
    "some_other_value": 1,
}

logic = Logic(
    expressions=[
        LogicExpression.b("Phone number", Operator.EQ, "123123123"),
        LogicExpression.b("some_value", Operator.NE, False),
        LogicExpression.b("some_other_value", Operator.LT, 1),
    ]
)
assert not logic.evaluate(data)
```

### Empty expression with default result
Suitable if the expressions are set by the end users, not the code
```python
from pydantic_logic import Logic

data = {
    "Phone number": "123123123",
    "some_value": True,
    "some_other_value": 1,
}

logic = Logic(
    expressions=[]
)
assert logic.evaluate(data, default_if_empty=True)
```
