#!/usr/bin/python


class Symbol:

    def __init__(self, name):
        self.name = name


class VariableSymbol(Symbol):

    def __init__(self, name, var_type, dims: list[int] = []):
        super().__init__(name)
        self.var_type = var_type
        self.dims = dims


class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        self.parent = parent
        self.scope_name = name
        self.symbols = {}


    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol


    def get(self, name) -> VariableSymbol | None: # get variable symbol or fundef from <name> entry
        if name in self.symbols:
            return self.symbols[name]
        return self.parent.get(name) if self.parent else None


    def getParentScope(self):
        return self.parent
    

    def pushScope(self, name):
        return SymbolTable(self, name)


    def popScope(self):
        return self.parent
