from __future__ import annotations

import struct
from dataclasses import dataclass
from typing import get_args

import uuid

from jijmodeling.expression.variables.placeholders import Placeholder, ArrayShape
from jijmodeling.expression.variables.variable import Subscripts, Element, Range
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
    DataType,
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
    NoneCondition,
    NotEqual,
    OrOperator,
    XorOperator,
)
from jijmodeling.expression.prod import ProdOperator
from jijmodeling.expression.sum import SumOperator
from jijmodeling.problem.problem import Problem, ProblemSense
from jijmodeling.expression.constraint import Constraint, Penalty

import jijmodeling.protobuf.pb2 as pb2
from jijmodeling.protobuf.type_annotations import (
    DecisionVar,
    UnaryOp,
    BinaryOp,
    CommutativeOp,
    ReductionOp,
    Expr,
)

# The current version of the schema.
# This version is used to check the compatibility of the schema.
# If the schema version of the input is not compatible with this version, an error will be returned.
# The version of the schema should be incremented when the schema is changed.
# The version should be satisfied the following conditions:
#
# 1. `MINIMUM_SUPPORTED_VERSION <= SCHEMA_VERSION`
# 2. `SCHEMA_VERSION <= MAXIMUM_SUPPORTED_VERSION`
#
# The condition 1. would be broken when the deserializer is newer than the serializer generating the schema.
# The condition 2. would be broken when the serializer generating the schema is newer than the deserializer.
_SCHEMA_VERSION = 1


def to_protobuf(obj) -> bytes:
    """
    Convert a Problem object to a bytes object serialized by protobuf.

    Args:
        expr (Expression): a instance object of the `Problem` class

    Raises:
        TypeError: The error raises if the instance object cannot be converted to a protobuf object

    Returns:
        bytes: a bytes object
    """

    # Create an empty `Header` message.
    header = pb2.Header()

    # Set the id.
    header.id = str(uuid.uuid4())

    # Set the version of the JijModeling schema.
    header.version = _SCHEMA_VERSION

    if isinstance(obj, get_args(Expr)):
        header.expression.MergeFrom(serialize_expr(obj))
    elif type(obj) is Problem:
        header.problem.MergeFrom(serialize_problem(obj))
    elif type(obj) is Constraint:
        header.constraint.MergeFrom(serialize_constraint(obj))
    elif type(obj) is Penalty:
        header.custom_penalty_term.MergeFrom(serialize_custom_penalty_term(obj))
    else:
        raise ValueError(
            f"{obj.__class__.__name__} is not a valid object to serialize."
        )

    return header.SerializeToString()


def serialize_problem(problem: Problem) -> pb2.Problem:
    """
    Convert a `Problem` instance object to a `Problem` message.

    Args:
        problem (Problem): a `Problem` instance object

    Returns:
        pb.Problem: a `Problem` message
    """

    # Create an empty `Problem` message.
    message = pb2.Problem()

    # Set the sense of the problem.
    if problem.sense == ProblemSense.MINIMUM:
        message.sense = pb2.Problem.Sense.SENSE_MINIMIZE
    elif problem.sense == ProblemSense.MAXIMUM:
        message.sense = pb2.Problem.Sense.SENSE_MAXIMIZE

    message.id = str(uuid.uuid4())
    message.name = problem.name
    message.objective_function.MergeFrom(serialize_expr(problem.objective))
    for name, constraint in problem.constraints.items():
        message.constraints[name].MergeFrom(serialize_constraint(constraint))
    for name, penalty in problem.custom_penalty_terms.items():
        message.custom_penalty_terms[name].MergeFrom(
            serialize_custom_penalty_term(penalty)
        )

    return message


def serialize_constraint(constraint: Constraint) -> pb2.Constraint:
    """
    Convert a `Constraint` instance object to a `Constraint` message.

    Args:
        constraint (Constraint): a `Constraint` instance object

    Raises:
        TypeError: the error occurs if the instance object cannot be converted to a protobuf object

    Returns:
        pb.Constraint: a `Constraint` message
    """

    # Create an empty `Constraint` message.
    message = pb2.Constraint()

    message.id = str(uuid.uuid4())
    message.name = constraint.name

    # Set the equality of the `Constraint` message.
    if type(constraint.expression) is Equal:
        message.equality = pb2.Constraint.Equality.EQUALITY_EQUAL
    elif type(constraint.expression) is LessThanEqual:
        message.equality = pb2.Constraint.Equality.EQUALITY_LESS_THAN_EQUAL
    else:
        raise ValueError(
            f"The equality {type(constraint.expression).__name__} is not supported."
        )

    message.left.MergeFrom(serialize_expr(constraint.expression.left))
    message.right.MergeFrom(serialize_expr(constraint.expression.right))
    message.forall_list.MergeFrom(serialize_forall_list(constraint.forall))

    return message


def serialize_custom_penalty_term(penalty: Penalty) -> pb2.CustomPenaltyTerm:
    # Create an empty `CustomPenaltyTerm` message.
    message = pb2.CustomPenaltyTerm()

    message.id = str(uuid.uuid4())
    message.name = penalty.name
    message.term.MergeFrom(serialize_expr(penalty.expression))
    message.forall_list.MergeFrom(serialize_forall_list(penalty.forall))
    return message


def serialize_forall_list(forall_list) -> pb2.ForallList:
    serializer = ProtobufSerializer()
    indices = [
        serializer.make_index_message(index, condition)
        for index, condition in forall_list
    ]

    message = pb2.ForallList()
    message.indices.extend(indices)
    message.expr_nodes.extend(serializer.expr_pool)
    return message


def serialize_expr(expr: Expr) -> pb2.Expr:
    """
    Convert a `Expression` instance object to an `Expression` message.

    Args:
        expr (Expression): an `Expression` instance object

    Raises:
        TypeError: the error occurs if the instance ofject cannot be converted to a protobuf object

    Returns:
        pb.Expression: a `Expression` message
    """

    # Create an empty `Expression` message.
    message = pb2.Expr()

    # Set the unique id of the `Expression` message.
    message.id = str(uuid.uuid4())

    serializer = ProtobufSerializer()
    serializer.serialize_expr(expr)
    message.root_id = serializer.root_id
    message.expr_nodes.extend(serializer.expr_pool)

    return message


@dataclass
class ProtobufSerializer:
    root_id: int
    expr_pool: list

    def __init__(self):
        self.root_id = 0
        self.expr_pool = []

    def add_expr_node(self, node):
        message = pb2.ExprNode()
        if type(node) == pb2.NumberLit:
            message.number_lit.MergeFrom(node)
        elif type(node) == pb2.Placeholder:
            message.placeholder.MergeFrom(node)
        elif type(node) == pb2.Element:
            message.element.MergeFrom(node)
        elif type(node) == pb2.DecisionVar:
            message.decision_var.MergeFrom(node)
        elif type(node) == pb2.Subscript:
            message.subscript.MergeFrom(node)
        elif type(node) == pb2.ArrayLength:
            message.array_length.MergeFrom(node)
        elif type(node) == pb2.UnaryOp:
            message.unary_op.MergeFrom(node)
        elif type(node) == pb2.BinaryOp:
            message.binary_op.MergeFrom(node)
        elif type(node) == pb2.CommutativeOp:
            message.commutative_op.MergeFrom(node)
        elif type(node) == pb2.ReductionOp:
            message.reduction_op.MergeFrom(node)

        if message not in self.expr_pool:
            self.expr_pool.append(message)
            self.root_id = len(self.expr_pool) - 1
        else:
            self.root_id = self.expr_pool.index(message)

    def make_index_message(self, index: Element, condition):
        # Create an empty `Index` message.
        message = pb2.Index()

        # Visit the index.
        self.serialize_element(index)
        message.element_id = self.root_id

        # Set the condition of the index.
        if type(condition) is not NoneCondition:
            self.serialize_expr(condition)
            message.condition_id = self.root_id

        return message

    def serialize_number_lit(self, lit: Number):
        # Create an empty `NumberLit` message.
        message = pb2.NumberLit()

        # Set the type of the value.
        if lit.dtype == DataType.INT:
            message.type = pb2.NumberLit.Type.TYPE_INTEGER

            # Set the value that is converted to the bytes object with the big-endian.
            message.value = int.from_bytes(struct.pack(">q", lit.value), "big")
        elif lit.dtype == DataType.FLOAT:
            message.type = pb2.NumberLit.Type.TYPE_FLOAT

            # Set the value that is onverted to the bytes object with the big-endian.
            message.value = int.from_bytes(struct.pack(">d", lit.value), "big")
        else:
            raise ValueError(f"Unsupported data type: {lit.dtype}")

        self.add_expr_node(message)

    def serialize_placeholder(self, ph: Placeholder):
        # Create an empty `Placeholder` message.
        message = pb2.Placeholder()

        # Set the name of the placeholder.
        message.name = ph.name

        # Set the number of dimensions of the placeholder.
        message.ndim = ph.ndim

        self.add_expr_node(message)

    def serialize_element(self, elt: Element):
        # Create an empty `Element` message.
        message = pb2.Element()

        # Set the name of the element.
        message.name = elt.name

        # Set the number of dimensions of the element.
        message.ndim = elt.ndim

        # Set the parent of the element.
        if type(elt.belong_to) is Range:
            range = pb2.Element.Range()
            # Set the start of the range.
            self.serialize_expr(elt.belong_to.start)
            range.start_id = self.root_id
            # Set the end of the range.
            self.serialize_expr(elt.belong_to.last)
            range.end_id = self.root_id

            message.range.MergeFrom(range)
        else:
            bound = pb2.Element.Bound()
            # Set the type of the parent.
            if type(elt.belong_to) is Placeholder:
                bound.type = pb2.Element.Bound.Type.TYPE_PLACEHOLDER
            elif type(elt.belong_to) is Element:
                bound.type = pb2.Element.Bound.Type.TYPE_ELEMENT
            elif type(elt.belong_to) is Subscripts:
                if type(elt.belong_to.variable) is Placeholder:
                    bound.type = pb2.Element.Bound.Type.TYPE_SUBSCRIPTED_PLACEHOLDER
                elif type(elt.belong_to.variable) is Element:
                    bound.type = pb2.Element.Bound.Type.TYPE_SUBSCRIPTED_ELEMENT
                else:
                    raise TypeError(
                        f"Unsupported type of the parent: {type(elt.belong_to.variable).__name__}"
                    )
            else:
                raise TypeError(
                    f"Unsupported type of the parent: {type(elt.belong_to).__name__}"
                )
            # Set the placeholder.
            self.serialize_expr(elt.belong_to)
            bound.bound_id = self.root_id

            message.bound.MergeFrom(bound)

        self.add_expr_node(message)

    def serialize_decision_var(self, var: DecisionVar):
        # Create an empty `DecisionVar` message.
        message = pb2.DecisionVar()

        # Set the name of the decision variable.
        message.name = var.name

        # Set the shape of the decision variable.
        for shape in var.shape:
            self.serialize_expr(shape)
            message.shape_ids.append(self.root_id)

        if type(var) is Binary:
            # Set the type of the decision variable.
            message.type = pb2.DecisionVar.Type.TYPE_BINARY
        elif type(var) is Integer:
            message.type = pb2.DecisionVar.Type.TYPE_INTEGER

            # Set the lower bound of the decision variable.
            lower_bound = pb2.DecisionVar.Bound()
            if var.lower_bound.is_operatable():
                lower_bound.type = pb2.DecisionVar.Bound.Type.TYPE_EXPRESSION
                self.serialize_expr(var.lower_bound)
            elif type(var.lower_bound) is Placeholder:
                lower_bound.type = pb2.DecisionVar.Bound.Type.TYPE_PLACEHOLDER
                self.serialize_placeholder(var.lower_bound)
            elif type(var.lower_bound) is Subscripts:
                lower_bound.type = pb2.DecisionVar.Bound.Type.TYPE_SUBSCRIPTED_PLACEHOLDER
                self.serialize_subscript(var.lower_bound)
            else:
                raise TypeError(
                    f"Unsupported type of lower bound: {type(var.lower_bound)}"
                )
            lower_bound.bound_id = self.root_id

            # Set the upper bound of the decision variable.
            upper_bound = pb2.DecisionVar.Bound()
            if var.upper_bound.is_operatable():
                upper_bound.type = pb2.DecisionVar.Bound.Type.TYPE_EXPRESSION
                self.serialize_expr(var.upper_bound)
            elif type(var.upper_bound) is Placeholder:
                upper_bound.type = pb2.DecisionVar.Bound.Type.TYPE_PLACEHOLDER
                self.serialize_placeholder(var.upper_bound)
            elif type(var.upper_bound) is Subscripts:
                upper_bound.type = pb2.DecisionVar.Bound.Type.TYPE_SUBSCRIPTED_PLACEHOLDER
                self.serialize_subscript(var.upper_bound)
            else:
                raise TypeError(
                    f"Unsupported type of upper bound: {type(var.upper_bound)}"
                )
            upper_bound.bound_id = self.root_id

            # Set the bounds of the decision variable.
            message.lower_bound.MergeFrom(lower_bound)
            message.upper_bound.MergeFrom(upper_bound)

        # The following types are not supported yet.
        # - Continuous variable
        # - Semi-continuous variable
        # - Semi-integer variable
        else:
            raise TypeError(f"Unsupported decision variable type: {type(var)}")

        self.add_expr_node(message)

    def serialize_subscript(self, subscript: Subscripts):
        # Create an empty `Subscript` message.
        message = pb2.Subscript()

        # Set the number of dimensions of the subscript.
        message.ndim = subscript.dim

        if type(subscript.variable) is Placeholder:
            message.type = pb2.Subscript.Type.TYPE_PLACEHOLDER
            self.serialize_placeholder(subscript.variable)
            message.variable_id = self.root_id
        elif type(subscript.variable) is Element:
            message.type = pb2.Subscript.Type.TYPE_ELEMENT
            self.serialize_element(subscript.variable)
            message.variable_id = self.root_id
        elif isinstance(subscript.variable, get_args(DecisionVar)):
            message.type = pb2.Subscript.Type.TYPE_DECISION_VAR
            self.serialize_decision_var(subscript.variable)
            message.variable_id = self.root_id
        else:
            raise TypeError(
                f"Unsupported type of subscripted variable: {type(subscript.variable).__name__}"
            )

        for subs in subscript.subscripts:
            self.serialize_expr(subs)
            message.subscript_ids.append(self.root_id)

        self.add_expr_node(message)

    def serialize_array_length(self, len: ArrayShape):
        # Create an empty `ArrayLength` message.
        message = pb2.ArrayLength()

        # Serialize the array of the array length.
        if type(len.array) is Placeholder:
            message.type = pb2.ArrayLength.Type.TYPE_PLACEHOLDER
            self.serialize_placeholder(len.array)
        elif type(len.array) is Element:
            message.type = pb2.ArrayLength.Type.TYPE_ELEMENT
            self.serialize_element(len.array)
        elif type(len.array) is Subscripts:
            if type(len.array.variable) is Placeholder:
                message.type = pb2.ArrayLength.Type.TYPE_SUBSCRIPTED_PLACEHOLDER
            elif type(len.array.variable) is Element:
                message.type = pb2.ArrayLength.Type.TYPE_SUBSCRIPTED_ELEMENT
            else:
                raise TypeError(
                    f"Unsupported type of subscripted variable: {type(len.array.variable).__name__}"
                )
            self.serialize_subscript(len.array)
        else:
            raise TypeError(f"Unsupported type of array: {type(len.array).__name__}")
        message.array_id = self.root_id

        # Set the axis of the array length.
        message.axis = len.dimension

        self.add_expr_node(message)

    def serialize_unary_op(self, op: UnaryOp):
        # Create an empty `UnaryOp` message.
        message = pb2.UnaryOp()

        # Visit the operand of the unary operator.
        self.serialize_expr(op.operand)
        message.operand_id = self.root_id

        # Set the kind of the unary operation.
        if type(op) is AbsoluteValue:
            message.kind = pb2.UnaryOp.Kind.KIND_ABS
        elif type(op) is Ceil:
            message.kind = pb2.UnaryOp.Kind.KIND_CEIL
        elif type(op) is Floor:
            message.kind = pb2.UnaryOp.Kind.KIND_FLOOR
        elif type(op) is Log2:
            message.kind = pb2.UnaryOp.Kind.KIND_LOG_2
        # The following unary operators are not supported in the current version of jijmodeling
        # - log10 (log10(a))
        # - natural log (ln(a))
        else:
            message.kind = pb2.UnaryOp.Kind.KIND_UNSPECIFIED

        self.add_expr_node(message)

    def serialize_binary_op(self, op: BinaryOp):
        if type(op) is Div:
            # Convert division to multiplication with inverse.
            expr = op.left * (op.right**-1)
            self.serialize_expr(expr)
        else:
            # Create an empty `BinaryOp` message.
            message = pb2.BinaryOp()

            # Visit the left hand side of the operator.
            self.serialize_expr(op.left)
            message.left_id = self.root_id

            # Visit the right hand side of the operator.
            self.serialize_expr(op.right)
            message.right_id = self.root_id

            # Set the kind of the binary operation.
            if type(op) is Power:
                message.kind = pb2.BinaryOp.Kind.KIND_POW
            elif type(op) is Mod:
                message.kind = pb2.BinaryOp.Kind.KIND_MOD
            elif type(op) is Equal:
                message.kind = pb2.BinaryOp.Kind.KIND_EQ
            elif type(op) is NotEqual:
                message.kind = pb2.BinaryOp.Kind.KIND_NOT_EQ
            elif type(op) is LessThan:
                message.kind = pb2.BinaryOp.Kind.KIND_LESS_THAN
            elif type(op) is LessThanEqual:
                message.kind = pb2.BinaryOp.Kind.KIND_LESS_THAN_EQ
            # The following binary operators are not supported in the current version of jijmodeling
            # - GreaterThan (a > b)
            # - GreaterThanEqual (a >= b)
            else:
                message.kind = pb2.BinaryOp.Kind.KIND_UNSPECIFIED

            self.add_expr_node(message)

    def serialize_commutative_op(self, op: CommutativeOp):
        # Create an empty `CommutativeOp` message.
        message = pb2.CommutativeOp()

        # Visit the left hand side of the operator.
        self.serialize_expr(op.left)
        left_id = self.root_id

        # Visit the right hand side of the operator.
        self.serialize_expr(op.right)
        right_id = self.root_id

        # Set the kind of the commutative operator.
        if type(op) is Add:
            message.kind = pb2.CommutativeOp.Kind.KIND_ADD
        elif type(op) is Mul:
            message.kind = pb2.CommutativeOp.Kind.KIND_MUL
        elif type(op) is Min:
            message.kind = pb2.CommutativeOp.Kind.KIND_MIN
        elif type(op) is Max:
            message.kind = pb2.CommutativeOp.Kind.KIND_MAX
        elif type(op) is AndOperator:
            message.kind = pb2.CommutativeOp.Kind.KIND_AND
        elif type(op) is OrOperator:
            message.kind = pb2.CommutativeOp.Kind.KIND_OR
        elif type(op) is XorOperator:
            message.kind = pb2.CommutativeOp.Kind.KIND_XOR
        else:
            message.kind = pb2.CommutativeOp.Kind.KIND_UNSPECIFIED

        # Set the id of the operands.
        message.term_ids.extend([left_id, right_id])

        self.add_expr_node(message)

    def serialize_reduction_op(self, op: ReductionOp):
        # Create an empty `ReductionOp` message.
        message = pb2.ReductionOp()

        # Set the kind of the reduction operator.
        if type(op) is SumOperator:
            message.kind = pb2.ReductionOp.Kind.KIND_SUM
        elif type(op) is ProdOperator:
            message.kind = pb2.ReductionOp.Kind.KIND_PROD
        else:
            message.kind = pb2.ReductionOp.Kind.KIND_UNSPECIFIED

        # Serialize the index of the reduction operator.
        message.index.MergeFrom(self.make_index_message(op.sum_index, op.condition))

        # Visit the operand of the reduction operator.
        self.serialize_expr(op.operand)
        message.operand_id = self.root_id

        self.add_expr_node(message)

    def serialize_expr(self, expr: Expr):
        if type(expr) is Number:
            self.serialize_number_lit(expr)
        elif type(expr) is Placeholder:
            self.serialize_placeholder(expr)
        elif isinstance(expr, get_args(DecisionVar)):
            self.serialize_decision_var(expr)
        elif type(expr) is Element:
            self.serialize_element(expr)
        elif type(expr) is Subscripts:
            self.serialize_subscript(expr)
        elif type(expr) is ArrayShape:
            self.serialize_array_length(expr)
        elif isinstance(expr, get_args(UnaryOp)):
            self.serialize_unary_op(expr)
        elif isinstance(expr, get_args(BinaryOp)):
            self.serialize_binary_op(expr)
        elif isinstance(expr, get_args(CommutativeOp)):
            self.serialize_commutative_op(expr)
        elif isinstance(expr, get_args(ReductionOp)):
            self.serialize_reduction_op(expr)
        else:
            raise TypeError(
                f"{expr.__class__.__name__} is not supported for protobuf serialization."
            )
