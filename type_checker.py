#!/usr/bin/python

from collections import defaultdict
import AST
from symbol_table import SymbolTable, VariableSymbol

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))

ttype['+']['int']['int'] = 'int'
ttype['+']['int']['float'] = 'float'
ttype['+']['float']['int'] = 'float'
ttype['+']['float']['float'] = 'float'
ttype['+']['str']['str'] = 'str'

ttype['-']['int']['int'] = 'int'
ttype['-']['int']['float'] = 'float'
ttype['-']['float']['int'] = 'float'
ttype['-']['float']['float'] = 'float'

ttype['*']['int']['int'] = 'int'
ttype['*']['int']['float'] = 'float'
ttype['*']['float']['int'] = 'float'
ttype['*']['float']['float'] = 'float'

ttype['/']['int']['int'] = 'int'
ttype['/']['int']['float'] = 'float'
ttype['/']['float']['int'] = 'float'
ttype['/']['float']['float'] = 'float'

ttype['>']['int']['int'] = 'bool'
ttype['>']['int']['float'] = 'bool'
ttype['>']['float']['int'] = 'bool'
ttype['>']['float']['float'] = 'bool'

ttype['<']['int']['int'] = 'bool'
ttype['<']['int']['float'] = 'bool'
ttype['<']['float']['int'] = 'bool'
ttype['<']['float']['float'] = 'bool'

ttype['>=']['int']['int'] = 'bool'
ttype['>=']['int']['float'] = 'bool'
ttype['>=']['float']['int'] = 'bool'
ttype['>=']['float']['float'] = 'bool'

ttype['<=']['int']['int'] = 'bool'
ttype['<=']['int']['float'] = 'bool'
ttype['<=']['float']['int'] = 'bool'
ttype['<=']['float']['float'] = 'bool'

ttype['==']['int']['int'] = 'bool'
ttype['==']['int']['float'] = 'bool'
ttype['==']['float']['int'] = 'bool'
ttype['==']['float']['float'] = 'bool'
ttype['==']['vector']['vector'] = 'bool'

ttype['!=']['int']['int'] = 'bool'
ttype['!=']['int']['float'] = 'bool'
ttype['!=']['float']['int'] = 'bool'
ttype['!=']['float']['float'] = 'bool'
ttype['!=']['vector']['vector'] = 'bool'

ttype['.+']['vector']['vector'] = 'vector'
ttype['.-']['vector']['vector'] = 'vector'
ttype['.*']['vector']['vector'] = 'vector'
ttype['./']['vector']['vector'] = 'vector'

ttype['+=']['int']['int'] = 'int'
ttype['+=']['int']['float'] = 'float'
ttype['+=']['float']['int'] = 'float'
ttype['+=']['float']['float'] = 'float'
ttype['+=']['str']['str'] = 'str'

ttype['-=']['int']['int'] = 'int'
ttype['-=']['int']['float'] = 'float'
ttype['-=']['float']['int'] = 'float'
ttype['-=']['float']['float'] = 'float'

ttype['*=']['int']['int'] = 'int'
ttype['*=']['int']['float'] = 'float'
ttype['*=']['float']['int'] = 'float'
ttype['*=']['float']['float'] = 'float'

ttype['/=']['int']['int'] = 'int'
ttype['/=']['int']['float'] = 'float'
ttype['/=']['float']['int'] = 'float'
ttype['/=']['float']['float'] = 'float'


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):
        print(f"\n\n There is no {node.__class__.__name__} class in AST.py that inherits node \n\n")
        # raise Error # auxiliary


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.symbol_table = SymbolTable(None, "global")
        self.loop_indent = 0
        self.errors = []


    # ------- EXTRA -------
    def report_errors(self):
        print("-- Errors --")
        for error in self.errors:
            print(error)
    # ---------------------
    

    def visit_IntNum(self, node):
        return "int"
    

    def visit_FloatNum(self, node):
        return "float"


    def visit_Variable(self, node):
        symbol = self.symbol_table.get(node.name)
        if symbol is None:
            self.errors.append(f"Undeclared variable {node.name}")
            return None
        return symbol.type


    def visit_String(self, node):
        return "str"
    

    def visit_Ref(self, node: AST.Ref):
        pass # TODO
        variable: AST.Variable
        indexes: list[AST.Node]


    def visit_Range(self, node):
        start_type = self.visit(node.start)
        end_type = self.visit(node.end)
        if start_type == end_type == "int":
            return "range"
        else:
            self.errors.append(f"Type error in range: type of start {start_type}, type of end {end_type}")


# ------- EXPRESSIONS -------


    def visit_BinExpr(self, node: AST.BinExpr):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        op = node.op

        if ttype[op][left_type][right_type] == "":
            self.errors.append(f"Type error in binary expression (not supported): {left_type} {op} {right_type}")
            return None

        return ttype[op][left_type][right_type]

        
    def visit_UnaryExpr(self, node):
        value_type = self.visit(node.value)
        op = node.op
        if op == "-" and value_type in ["int", "float"]:
            return value_type
        elif op == "\'" and value_type == "vector": # vector...?
            return value_type
        else:
            self.errors.append(f"Type error in unary expression: {node.op} {value_type}")

    
    def visit_Vector(self, node):
        if not node.values:
            self.errors.append("Empty vector declaration")
            return "vector"
        first_type = self.visit(node.values[0])
        for value in node.values:
            value_type = self.visit(value)
            if value_type != first_type:
                self.errors.append(f"Mixed types in vector: {first_type} and {value_type}")
        return "vector"

    
    def visit_FunctionCall(self, node):
        pass
 

# ---------- INSTRUCTIONS ----------


    def visit_Assignment(self, node):
        value_type = self.visit(node.value)

        if isinstance(node.ref, AST.Variable):
            var_name = node.ref.name
            var_symbol = VariableSymbol(var_name, value_type)
            self.symbol_table.put(var_name, var_symbol)

        ref_type = self.visit(node.ref)
        
        return ref_type
    

    def visit_ReturnInstr(self, node):
        return self.visit(node.value)


    def visit_SpecialInstr(self, node: AST.SpecialInstr):
        if self.loop_indent == 0:
            self.errors.append(f"Usage of '{node.name}' out of loop")


    def visit_IfElseInstr(self, node):
        condition_type = self.visit(node.condition)
        if condition_type != "bool":
            self.errors.append(f"Type error in condition in if-else: '{condition_type}'")
        self.visit(node.then_block)
        if node.else_block:
            self.visit(node.else_block)


    def visit_PrintInstr(self, node):
        for arg in node.args:
            self.visit(arg)


    def visit_ForLoop(self, node: AST.ForLoop):
        range_type = self.visit(node.var_range)
        if range_type != "range":
            self.errors.append(f"Type error in range in for loop: {range_type}")

        self.symbol_table = self.symbol_table.pushScope("for")
        self.loop_indent += 1

        self.symbol_table.put(node.variable.name, VariableSymbol(node.variable.name, "int"))
        self.visit(node.block)

        self.symbol_table = self.symbol_table.popScope()
        self.loop_indent -= 1


    def visit_WhileLoop(self, node: AST.WhileLoop):
        condition_type = self.visit(node.condition)
        if condition_type != "bool":
            self.errors.append(f"Type error in condition in while-loop '{condition_type}'")

        self.symbol_table = self.symbol_table.pushScope("while")
        self.loop_indent += 1

        self.visit(node.block)

        self.symbol_table = self.symbol_table.popScope()
        self.loop_indent -= 1


# ---------- OTHER ----------


    def visit_Program(self, node):
        for instruction in node.instructions:
            self.visit(instruction)
        

    def visit_Error(self, node):
        if self.visit(node.msg) != "str":
            self.errors.append(f"Type error in error message: {self.visit(node.msg)}")
