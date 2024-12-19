import AST
import symbol_table
from memory import Memory, MemoryStack
from exceptions import BreakException, ContinueException, ReturnValueException
from visit import on, when
import sys

sys.setrecursionlimit(10000)

operations = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
    '<': lambda a, b: a < b,
    '<=': lambda a, b: a <= b,
    '>': lambda a, b: a > b,
    '>=': lambda a, b: a >= b,
    '==': lambda a, b: a == b,
    '!=': lambda a, b: a != b,
}

mat_operations = {
    '+': lambda a, b: NotImplemented,
    '*': lambda a, b: NotImplemented,
    '==': lambda a, b: a == b,
    '!=': lambda a, b: a != b,
    '.+': lambda a, b: NotImplemented,
    '.-': lambda a, b: NotImplemented,
    '.*': lambda a, b: NotImplemented,
    './': lambda a, b: NotImplemented,
}

class Interpreter(object):
    memory: MemoryStack = MemoryStack('global')

    @on('node')
    def visit(self, node):
        pass


    @when(AST.IntNum)
    def visit(self, node: AST.IntNum):
        return node.value

        
    @when(AST.FloatNum)
    def visit(self, node: AST.FloatNum):
        return node.value


    @when(AST.Variable)
    def visit(self, node: AST.Variable):
        return self.memory.get(node.name)


    @when(AST.String)
    def visit(self, node: AST.String):
        return node.value


    @when(AST.Ref)
    def visit(self, node: AST.Ref):
        variable: list = node.variable.accept(self)

        for index in node.indices:
            variable = variable[index.accept(self)]

        return variable


    @when(AST.Range)
    def visit(self, node: AST.Range):
        start = node.start.accept(self)
        end = node.end.accept(self)
        return start, end


    @when(AST.BinExpr)
    def visit(self, node: AST.BinExpr):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)

        if isinstance(r1, list) or isinstance(r2, list):
            mat_operations[node.op](r1, r2)

        return operations[node.op](r1, r2)


    @when(AST.UnaryExpr)
    def visit(self, node: AST.UnaryExpr):
        value = node.value.accept(self)
        if node.op == '-':
            return -value
        elif node.op == 'TRANSPOSE':
            return NotImplemented


    @when(AST.Vector)
    def visit(self, node: AST.Vector):
        vector = []

        for value in node.values:
            vector.append(value.accept(self))

        return vector


    @when(AST.FunctionCall)
    def visit(self, node: AST.FunctionCall):
        args = [arg.accept(self) for arg in node.args]
        return NotImplemented(*args)


    @when(AST.Assignment)
    def visit(self, node: AST.Assignment):
        value = node.value.accept(self)

        if node.instr != '=':
            old_value = node.ref.accept(self)
            op = node.instr[0]
            value = operations[op](old_value, value)

        if isinstance(node.ref, AST.Variable):
            self.memory.set(node.ref.name, value)
        elif isinstance(node.ref, AST.Ref):
            variable = node.ref.variable.accept(self)

            for index in node.ref.indices[:-1]:
                variable = variable[index.accept(self)]

            variable[node.ref.indices[-1].accept(self)] = value


    @when(AST.ReturnInstr)
    def visit(self, node: AST.ReturnInstr):
        raise ReturnValueException(node.value.accept(self))


    @when(AST.SpecialInstr)
    def visit(self, node: AST.SpecialInstr):
        print(node.name)
        if node.name == 'CONTINUE':
            raise ContinueException()
        elif node.name == 'BREAK':
            raise BreakException()


    @when(AST.IfElseInstr)
    def visit(self, node: AST.IfElseInstr):
        if node.condition.accept(self):
            self.memory.push('if_then')
            node.then_block.accept(self)
            self.memory.pop()
        elif node.else_block:
            self.memory.push('if_else')
            node.else_block.accept(self)
            self.memory.pop()


    @when(AST.PrintInstr)
    def visit(self, node: AST.PrintInstr):
        for arg in node.args:
            print(arg.accept(self), end=' ')
        print('')


    @when(AST.ForLoop)
    def visit(self, node: AST.ForLoop):
        start, end = node.var_range.accept(self)
        self.memory.push('for_loop')

        for i in range(start, end+1):
            self.memory.set(node.variable.name, i)
            try:
                node.block.accept(self)
            except ContinueException as _:
                continue
            except BreakException as _:
                break

        self.memory.pop()


    @when(AST.WhileLoop)
    def visit(self, node: AST.WhileLoop):
        self.memory.push('while_loop')

        while node.condition.accept(self):
            try:
                node.block.accept(self)
            except ContinueException as _:
                continue
            except BreakException as _:
                break

        self.memory.pop()


    @when(AST.Program)
    def visit(self, node: AST.Program, toplevel=False):
        try:
            for instruction in node.instructions:
                if isinstance(instruction, AST.Program):
                    self.memory.push('block')
                instruction.accept(self)
        except ReturnValueException as e:
            if toplevel:
                print(f'Program exited with value {e.value}')
            else:
                raise e


    @when(AST.Error)
    def visit(self, node: AST.Error):
        pass

