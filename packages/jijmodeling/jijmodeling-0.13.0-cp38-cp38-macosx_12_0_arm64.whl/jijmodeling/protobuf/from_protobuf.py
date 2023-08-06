from __future__ import annotations

import struct
from functools import reduce
from dataclasses import dataclass

import jijmodeling.protobuf.pb2 as pb2

from jijmodeling.expression.expression import (
    DataType,
    Expression,
    Number,
)
from jijmodeling.expression.mathfunc import (
    abs,
    ceil,
    floor,
    log2,
    min,
    max,
)
from jijmodeling.expression.prod import prod
from jijmodeling.expression.sum import sum
from jijmodeling.expression.variables.deci_vars import (
    BinaryVar,
    IntegerVar,
    DecisionVariable,
)
from jijmodeling.expression.variables.placeholders import ArrayShape, Placeholder
from jijmodeling.expression.variables.variable import Element, Subscripts
from jijmodeling.problem import Problem, ProblemSense
from jijmodeling.expression.constraint import Constraint, Penalty, CustomPenaltyTerm

# The minimum supported version of the schema.
# If the schema version of the input is less than this version, an error will be returned.
# The version of the schema would be bumped when the schema is changed.
#
# NOTE: If we support backward compatibility, this would be unnecessary, or alternatively, should be set to 0.
MINIMUM_SUPPORTED_VERSION = 1

# The maximum supported version of the schema.
# If the schema version of the input is greater than this version, an error will be returned.
# The version of the schema would be bumped when the schema is changed.
MAXIMUM_SUPPORTED_VERSION = 1


def from_protobuf(buf: bytes):
    """
    Convert a bytes object in protobuf to a Problem object.

    Args:
        bytes (bytes): a bytes object in protobuf

    Returns:
        Problem: a Problem object
    """
    # Convert the bytes object into the `Header` message object.
    header = pb2.Header.FromString(buf)

    # Check the schema version.
    check_version(header.version)

    body = header.WhichOneof("body")
    if body == "expression":
        return deserialize_expr(header.expression)
    elif body == "problem":
        return deserialize_problem(header.problem)
    elif body == "constraint":
        return deserialize_constraint(header.constraint)
    elif body == "custom_penalty_term":
        return deserialize_custom_penalty_term(header.custom_penalty_term)


def check_version(version: int):
    if version < MINIMUM_SUPPORTED_VERSION:
        raise ValueError(
            f"The schema version {version} is less than the minimum supported version {MINIMUM_SUPPORTED_VERSION}."
        )
    elif version > MAXIMUM_SUPPORTED_VERSION:
        raise ValueError(
            f"The schema version {version} is greater than the maximum supported version {MAXIMUM_SUPPORTED_VERSION}."
        )


def deserialize_problem(message: pb2.Problem) -> Problem:
    if message.sense == pb2.Problem.Sense.SENSE_MINIMIZE:
        sense = ProblemSense.MINIMUM
    elif message.sense == pb2.Problem.Sense.SENSE_MAXIMIZE:
        sense = ProblemSense.MAXIMUM
    return Problem(
        name=message.name,
        sense=sense,
        objective=deserialize_expr(message.objective_function),
        constraints={
            name: deserialize_constraint(constraint)
            for name, constraint in message.constraints.items()
        },
        penalties={
            name: deserialize_custom_penalty_term(term)
            for name, term in message.custom_penalty_terms.items()
        },
    )


def deserialize_constraint(message: pb2.Constraint) -> Constraint:
    left = deserialize_expr(message.left)
    right = deserialize_expr(message.right)

    if message.equality == pb2.Constraint.Equality.EQUALITY_EQUAL:
        expression = left == right
    elif message.equality == pb2.Constraint.Equality.EQUALITY_LESS_THAN_EQUAL:
        expression = left <= right
    elif message.equality == pb2.Constraint.Equality.EQUALITY_GREATER_THAN_EQUAL:
        expression = left >= right

    forall_list = deserialize_forall_list(message.forall_list)

    return Constraint(name=message.name, expression=expression, forall=forall_list)


def deserialize_forall_list(message: pb2.ForallList):
    deserializer = ProtobufExprDeserializer(message.expr_nodes)

    return [deserializer.deserialize_index(index) for index in message.indices]


def deserialize_custom_penalty_term(message: pb2.CustomPenaltyTerm) -> Penalty:
    term = deserialize_expr(message.term)
    forall_list = deserialize_forall_list(message.forall_list)

    return CustomPenaltyTerm(name=message.name, expression=term, forall=forall_list)


def deserialize_expr(
    message: pb2.Expr,
) -> Expression:
    """
    Convert a message object to a `Expression` object.

    Args:
        expression (pb.Expression): a `Expression` message

    Returns:
        Expression: an instance object that is a subclass of the `Expression` class
    """
    deserializer = ProtobufExprDeserializer(message.expr_nodes)
    root = message.expr_nodes[message.root_id]
    return deserializer.deserialize_expr_node(root)


@dataclass
class ProtobufExprDeserializer:
    expr_nodes: list

    def get_node(self, id: int):
        return self.deserialize_expr_node(self.expr_nodes[id])

    def deserialize_number_lit(self, message: pb2.NumberLit) -> Number:
        if message.type == pb2.NumberLit.Type.TYPE_INTEGER:
            dtype = DataType.INT
            # Convert the bits to the integer value.
            value = struct.unpack(
                ">q",
                message.value.to_bytes(length=struct.calcsize(">q"), byteorder="big"),
            )[0]
        # Case: float
        elif message.type == pb2.NumberLit.Type.TYPE_FLOAT:
            dtype = DataType.FLOAT
            # Convert the bits to the float value.
            value = struct.unpack(
                ">d",
                message.value.to_bytes(length=struct.calcsize(">d"), byteorder="big"),
            )[0]

        return Number(value=value, dtype=dtype)

    def deserialize_placeholder(self, message: pb2.Placeholder) -> Placeholder:
        return Placeholder(name=message.name, ndim=message.ndim)

    def deserialize_element(self, message: pb2.Element) -> Element:
        belong_to = message.WhichOneof("belong_to")
        if belong_to == "range":
            start = self.get_node(message.range.start_id)
            end = self.get_node(message.range.end_id)
            return Element(name=message.name, belong_to=(start, end))
        elif belong_to == "bound":
            bound = self.get_node(message.bound.bound_id)
            return Element(name=message.name, belong_to=bound)
        else:
            raise ValueError(
                f"fail to deserialize the {belong_to} message as a parent of the Element."
            )

    def deserialize_decision_var(self, message: pb2.DecisionVar) -> DecisionVariable:
        name = message.name
        shape = [self.get_node(id) for id in message.shape_ids]
        if message.type == pb2.DecisionVar.Type.TYPE_BINARY:
            return BinaryVar(name, shape=shape)
        elif message.type == pb2.DecisionVar.Type.TYPE_INTEGER:
            lower_bound = self.get_node(message.lower_bound.bound_id)
            upper_bound = self.get_node(message.upper_bound.bound_id)
            # NOTE:
            # After setting dummy values to the lower and upper bounds,
            # set the correct values to them.
            var = IntegerVar(name, shape=shape, lower_bound=0, upper_bound=1)
            var._lower = lower_bound
            var._upper = upper_bound
            return var
        elif message.type == pb2.DecisionVar.Type.TYPE_CONTINUOUS:
            raise ValueError("continuous variable is not supported")
        elif message.type == pb2.DecisionVar.Type.TYPE_SEMI_INTEGER:
            raise ValueError("semi-integer variable is not supported")
        elif message.type == pb2.DecisionVar.Type.TYPE_SEMI_CONTINUOUS:
            raise ValueError("semi-continuous variable is not supported")
        else:
            raise ValueError(
                f"unsupported decision variable type (type: {message.type})"
            )

    def deserialize_subscript(self, message: pb2.Subscript) -> Subscripts:
        subscripts = [self.get_node(id) for id in message.subscript_ids]
        var = self.get_node(message.variable_id)
        return var[subscripts]

    def deserialize_array_length(self, message: pb2.ArrayLength) -> ArrayShape:
        array = self.get_node(message.array_id)
        axis = message.axis
        return array.shape[axis]

    def deserialize_unary_op(self, message: pb2.UnaryOp):
        operand = self.get_node(message.operand_id)
        kind = message.kind
        if kind == pb2.UnaryOp.Kind.KIND_ABS:
            return abs(operand)
        elif kind == pb2.UnaryOp.Kind.KIND_CEIL:
            return ceil(operand)
        elif kind == pb2.UnaryOp.Kind.KIND_FLOOR:
            return floor(operand)
        elif kind == pb2.UnaryOp.Kind.KIND_LOG_2:
            return log2(operand)
        elif kind == pb2.UnaryOp.Kind.KIND_LOG_10:
            raise ValueError("log10 is not supported")
        elif kind == pb2.UnaryOp.Kind.KIND_LOG_E:
            raise ValueError("ln is not supported")
        else:
            raise ValueError(f"unsupported unary operator (kind: {kind}))")

    def deserialize_binary_op(self, message: pb2.BinaryOp):
        left = self.get_node(message.left_id)
        right = self.get_node(message.right_id)
        kind = message.kind
        if kind == pb2.BinaryOp.Kind.KIND_POW:
            return left**right
        elif kind == pb2.BinaryOp.Kind.KIND_MOD:
            return left % right
        elif kind == pb2.BinaryOp.Kind.KIND_EQ:
            return left == right
        elif kind == pb2.BinaryOp.Kind.KIND_NOT_EQ:
            return left != right
        elif kind == pb2.BinaryOp.Kind.KIND_LESS_THAN:
            return left < right
        elif kind == pb2.BinaryOp.Kind.KIND_LESS_THAN_EQ:
            return left <= right
        elif kind == pb2.BinaryOp.Kind.KIND_GREATER_THAN:
            return left > right
        elif kind == pb2.BinaryOp.Kind.KIND_GREATER_THAN_EQ:
            return left >= right
        else:
            raise ValueError(f"unsupported binary operator (kind: {kind})")

    def deserialize_commutative_op(self, message: pb2.CommutativeOp):
        first, *rest = message.term_ids
        kind = message.kind
        if kind == pb2.CommutativeOp.KIND_ADD:
            op = lambda acc, id: acc + self.get_node(id)
        elif kind == pb2.CommutativeOp.KIND_MUL:
            op = lambda acc, id: acc * self.get_node(id)
        elif kind == pb2.CommutativeOp.KIND_MIN:
            op = lambda acc, id: min(acc, self.get_node(id))
        elif kind == pb2.CommutativeOp.KIND_MAX:
            op = lambda acc, id: max(acc, self.get_node(id))
        elif kind == pb2.CommutativeOp.KIND_AND:
            op = lambda acc, id: acc & self.get_node(id)
        elif kind == pb2.CommutativeOp.KIND_OR:
            op = lambda acc, id: acc | self.get_node(id)
        elif kind == pb2.CommutativeOp.KIND_XOR:
            op = lambda acc, id: acc ^ self.get_node(id)
        else:
            raise ValueError(f"unsupported commutative operator (kind: {kind})")
        return reduce(op, rest, self.get_node(first))

    def deserialize_index(self, message: pb2.Index):
        elt = self.get_node(message.element_id)
        if message.HasField("condition_id"):
            condition = self.get_node(message.condition_id)
        else:
            condition = None
        return (elt, condition)

    def deserialize_reduction_op(self, message: pb2.ReductionOp):
        index, condition = self.deserialize_index(message.index)
        operand = self.get_node(message.operand_id)
        kind = message.kind
        if kind == pb2.ReductionOp.Kind.KIND_SUM:
            return sum((index, condition), operand)
        elif kind == pb2.ReductionOp.Kind.KIND_PROD:
            return prod((index, condition), operand)
        else:
            raise ValueError(f"unsupported reduction operator (kind: {kind})")

    def deserialize_expr_node(self, message: pb2.ExprNode):
        kind = message.WhichOneof("kind")
        if kind == "number_lit":
            return self.deserialize_number_lit(message.number_lit)
        elif kind == "placeholder":
            return self.deserialize_placeholder(message.placeholder)
        elif kind == "element":
            return self.deserialize_element(message.element)
        elif kind == "decision_var":
            return self.deserialize_decision_var(message.decision_var)
        elif kind == "subscript":
            return self.deserialize_subscript(message.subscript)
        elif kind == "array_length":
            return self.deserialize_array_length(message.array_length)
        elif kind == "unary_op":
            return self.deserialize_unary_op(message.unary_op)
        elif kind == "binary_op":
            return self.deserialize_binary_op(message.binary_op)
        elif kind == "commutative_op":
            return self.deserialize_commutative_op(message.commutative_op)
        elif kind == "reduction_op":
            return self.deserialize_reduction_op(message.reduction_op)
