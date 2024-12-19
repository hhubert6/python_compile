#!/usr/bin/python


class Symbol:

    def __init__(self, name):
        self.name = name


class VariableSymbol(Symbol):

    def __init__(self, name, var_type, dims: list[int] = [], elements_type = None):
        super().__init__(name)
        self.var_type = var_type
        self.dims = dims
        self.elements_type = elements_type


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


    def pushScope(self, name):
        return SymbolTable(self, name)


    def popScope(self):
        return self.parent
