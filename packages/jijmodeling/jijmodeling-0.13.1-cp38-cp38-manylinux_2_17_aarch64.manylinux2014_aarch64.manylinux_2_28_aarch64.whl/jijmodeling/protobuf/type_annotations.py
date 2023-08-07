from __future__ import annotations

from typing import Union

from jijmodeling.expression.variables.placeholders import Placeholder, ArrayShape
from jijmodeling.expression.variables.variable import Subscripts, Element
from jijmodeling.expression.variables.deci_vars import Binary, Integer
from jijmodeling.expression.mathfunc import (
    AbsoluteValue,
    Ceil,
    Floor,
    Log2,
    Max,
    Min,
)
from jijmodeling.expression.expression import (
    Add,
    Div,
    Mod,
    Mul,
    Number,
    Power,
)
from jijmodeling.expression.condition import (
    AndOperator,
    Equal,
    LessThan,
    LessThanEqual,
    NotEqual,
    OrOperator,
    XorOperator,
)
from jijmodeling.expression.prod import ProdOperator
from jijmodeling.expression.sum import SumOperator

DecisionVar = Union[Binary, Integer]
UnaryOp = Union[AbsoluteValue, Ceil, Floor, Log2]
BinaryOp = Union[Div, Mod, Power, Equal, NotEqual, LessThan, LessThanEqual]
CommutativeOp = Union[Add, Mul, Min, Max, AndOperator, OrOperator, XorOperator]
ReductionOp = Union[SumOperator, ProdOperator]
Expr = Union[
    Number,
    Placeholder,
    DecisionVar,
    Element,
    ArrayShape,
    Subscripts,
    UnaryOp,
    BinaryOp,
    CommutativeOp,
    ReductionOp,
]
