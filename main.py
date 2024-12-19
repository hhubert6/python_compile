import sys
from scanner import Scanner
from parser import Mparser
from tree_printer import TreePrinter
from type_checker import TypeChecker


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "samples/example.txt"

    try:
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()

    lexer = Scanner()
    parser = Mparser()
    ast = parser.parse(lexer.tokenize(text))
    # ast.printTree()

    typeChecker = TypeChecker()   
    typeChecker.visit(ast)
    typeChecker.report_errors()

    # for tok in lexer.tokenize(text):
    #     print("(%d): %s(%s)" % (tok.lineno, tok.type, tok.value))
