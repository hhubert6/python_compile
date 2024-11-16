import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, value, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.IntNum)
    def printTree(self: AST.IntNum, indent=0):
        print(("|  " * indent) + str(self.value))

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print(("|  " * indent) + str(self.value))

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print(("|  " * indent) + self.name)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print(("|  " * indent) + self.op)
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)


    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass    
        # fill in the body


    # define printTree for other classes
    # ...


