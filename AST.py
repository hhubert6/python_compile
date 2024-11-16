from dataclasses import dataclass


class Node(object):
    pass

# --------- TYPES ---------

@dataclass
class IntNum(Node):
    value: int


@dataclass
class FloatNum(Node):
    value: float


@dataclass
class Variable(Node):
    name: str


@dataclass
class String(Node):
    name: str


@dataclass
class Ref(Node):
    variable: Variable
    indexes: list[int]


@dataclass
class Range(Node):
    start: Node
    end: Node


# ------- EXPRESSIONS -------

@dataclass
class BinExpr(Node):
    op: str
    left: Node
    right: Node 


@dataclass
class Vector(Node):
    values: list[Node]


# ---------- INSTRUCTIONS ----------
@dataclass
class Assignment(Node):
    instr: str
    ref: Ref | Variable
    value: BinExpr | String 


@dataclass
class SpecialInstr(Node):
    name: str


@dataclass
class IfElseInstr(Node):
    condition: Node
    then_block: Node
    else_block: Node


@dataclass
class PrintInstr(Node):
    args: list[Node]


@dataclass
class ForLoop(Node):
    variable: Variable
    var_range: Range
    block: Node


@dataclass
class WhileLoop(Node):
    condition: Node
    block: Node


class Program(Node):
    def __init__(self, instructions: list):
        self.instructions = instructions


class Error(Node):
    def __init__(self):
        pass
      
