import sys
from scanner import Scanner
from parser import Mparser


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"

    try:
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()

    lexer = Scanner()
    parser = Mparser()
    res = parser.parse(lexer.tokenize(text))
    print(res)

    # for tok in lexer.tokenize(text):
    #     print("(%d): %s(%s)" % (tok.lineno, tok.type, tok.value))
