#!/usr/bin/python

from AST import *
from symbol_table import SymbolTable, VariableSymbol

"""
types: 'int', 'flaot', 'str', 'range', 'vector' TODO
"""

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):
        print(f"\n\n There is no {node.__class__.__name__} class in AST.py that inherits node \n\n")
        raise Error # auxiliary


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.symbol_table = SymbolTable(None, "global")
        self.errors = []


    # ------- EXTRA -------
    def report_errors(self):
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
        return symbol.type


    def visit_String(self, node):
        return "str"
    

    def visit_Ref(self, node):
        pass # TODO
        variable: Variable
        indexes: list[Node]


    def visit_Range(self, node):
        start_type = self.visit(node.start)
        end_type = self.visit(node.end)
        if start_type == end_type == "int":
            return "range"
        else:
            self.errors.append(f"Type error in range: type of start {start_type}, type of end {end_type}")


# ------- EXPRESSIONS -------


    def visit_BinExpr(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        op = node.op

        if op in ["+", "-", "*", "/"]: # TODO for now we don't accept operations on strings, etc.
            if left_type == right_type and left_type in ["int", "float"]:
                return left_type
            elif left_type in ["int", "float"] and right_type in ["int", "float"]:
                return "float"
            else:
                self.errors.append(f"Type error in binary expression: {left_type} {op} {right_type}")
            
        elif op in [".+", ".-", ".*", "./"]:
            if left_type == right_type and left_type == "vector": # TODO: size of vectors DOES matter
                return "vector"
            else:
                self.errors.append(f"Type error in binary expression: {left_type} {op} {right_type}")
            
        elif op in ["<", ">", "<=", ">=", "==", "!="]:
            if left_type == right_type:
                return "bool"
            else:
                self.errors.append(f"Type error in comparison (binary expression): {left_type} {op} {right_type}")
            
        else:
            self.errors.append(f"Unknown binary operator: {op}")

        
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

        if isinstance(node.ref, Variable):
            var_name = node.ref.name
            var_symbol = VariableSymbol(var_name, value_type)
            self.symbol_table.put(var_name, var_symbol)

        ref_type = self.visit(node.ref)
        
        return ref_type
    

    def visit_ReturnInstr(self, node):
        return self.visit(node.value)


    def visit_SpecialInstr(self, node):
        pass


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


    def visit_ForLoop(self, node):
        range_type = self.visit(node.var_range)
        if range_type != "range":
            self.errors.append(f"Type error in range in for loop: {range_type}")
        self.symbol_table.put(node.variable.name, VariableSymbol(node.variable.name, "int")) # TODO: correct scope (push scope)
        self.visit(node.block)
        return None # TODO


    def visit_WhileLoop(self, node):
        condition_type = self.visit(node.condition)
        if condition_type != "bool":
            self.errors.append(f"Type error in condition in while-loop '{condition_type}'")
        self.visit(node.block)


# ---------- OTHER ----------


    def visit_Program(self, node):
        for instruction in node.instructions:
            self.visit(instruction)
        

    def visit_Error(self, node):
        if self.visit(node.msg) != "str":
            self.errors.append(f"Type error in error message: {self.visit(node.msg)}")
