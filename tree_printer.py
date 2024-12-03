import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:
    @staticmethod
    def print(value: str, indent=0):
        print(('|  ' * indent) + value)


    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.IntNum)
    def printTree(self: AST.IntNum, indent=0):
        TreePrinter.print(str(self.value), indent)


    @addToClass(AST.FloatNum)
    def printTree(self: AST.FloatNum, indent=0):
        TreePrinter.print(str(self.value), indent)


    @addToClass(AST.Variable)
    def printTree(self: AST.Variable, indent=0):
        TreePrinter.print(self.name, indent)


    @addToClass(AST.String)
    def printTree(self: AST.String, indent=0):
        TreePrinter.print(self.value, indent)


    @addToClass(AST.Ref)
    def printTree(self: AST.Ref, indent=0):
        TreePrinter.print('REF', indent)
        self.variable.printTree(indent + 1)
        for n in self.indexes:
            n.printTree(indent + 1)


    @addToClass(AST.Range)
    def printTree(self: AST.Range, indent=0):
        TreePrinter.print('RANGE', indent)
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)


    # ------- EXPRESSIONS -------


    @addToClass(AST.BinExpr)
    def printTree(self: AST.BinExpr, indent=0):
        TreePrinter.print(self.op, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)


    @addToClass(AST.UnaryExpr)
    def printTree(self: AST.UnaryExpr, indent=0):
        TreePrinter.print(self.op, indent)
        self.value.printTree(indent + 1)


    @addToClass(AST.Vector)
    def printTree(self: AST.Vector, indent=0):
        TreePrinter.print('VECTOR', indent)
        for n in self.values:
            n.printTree(indent + 1)


    @addToClass(AST.FunctionCall)
    def printTree(self: AST.FunctionCall, indent=0):
        TreePrinter.print(self.name, indent)
        self.arg.printTree(indent + 1)


    # ---------- INSTRUCTIONS ----------


    @addToClass(AST.Assignment)
    def printTree(self: AST.Assignment, indent=0):
        TreePrinter.print(self.instr, indent)
        self.ref.printTree(indent + 1)
        self.value.printTree(indent + 1)


    @addToClass(AST.ReturnInstr)
    def printTree(self: AST.ReturnInstr, indent=0):
        TreePrinter.print('RETURN', indent)
        self.value.printTree(indent + 1)


    @addToClass(AST.SpecialInstr)
    def printTree(self: AST.SpecialInstr, indent=0):
        TreePrinter.print(self.name, indent)


    @addToClass(AST.IfElseInstr)
    def printTree(self: AST.IfElseInstr, indent=0):
        TreePrinter.print('IF', indent)
        self.condition.printTree(indent + 1)

        TreePrinter.print('THEN', indent)
        self.then_block.printTree(indent + 1)

        if self.else_block:
            TreePrinter.print('ELSE', indent)
            self.else_block.printTree(indent + 1)


    @addToClass(AST.PrintInstr)
    def printTree(self: AST.PrintInstr, indent=0):
        TreePrinter.print('PRINT', indent)
        for n in self.args:
            n.printTree(indent + 1)


    @addToClass(AST.ForLoop)
    def printTree(self: AST.ForLoop, indent=0):
        TreePrinter.print('FOR', indent)
        self.variable.printTree(indent + 1)
        self.var_range.printTree(indent + 1)
        self.block.printTree(indent + 1)


    @addToClass(AST.WhileLoop)
    def printTree(self: AST.WhileLoop, indent=0):
        TreePrinter.print('WHILE', indent)
        self.condition.printTree(indent + 1)
        self.block.printTree(indent + 1)


    # ---------- OTHER ----------


    @addToClass(AST.Program)
    def printTree(self: AST.Program, indent=0):
        for n in self.instructions:
            n.printTree(indent)


    @addToClass(AST.Error)
    def printTree(self: AST.Error, indent=0):
        TreePrinter.print(self.msg, indent)

