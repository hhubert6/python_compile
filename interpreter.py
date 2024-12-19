
import AST
import symbol_table
from memory import Memory, MemoryStack
from exceptions import BreakException, ContinueException, ReturnValueException
from visit import on, when
import sys

sys.setrecursionlimit(10000)

class Interpreter(object):


    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        pass
        # r1 = node.left.accept(self)
        # r2 = node.right.accept(self)
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(AST.Assignment)
    def visit(self, node):
        pass
    #
    #

    # simplistic while loop interpretation
    @when(AST.WhileLoop)
    def visit(self, node: AST.WhileLoop):
        r = None
        # while node.cond.accept(self):
        #     r = node.body.accept(self)
        return r

    @when(AST.Program)
    def visit(self, node: AST.Program):
        pass

