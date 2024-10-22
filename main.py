import sys
from sly import Lexer


class Scanner(Lexer):
    # Set of token names
    tokens = {PLUS, MINUS, TIMES, DIVIDE,               # binary operators
              DOTPLUS, DOTMINUS, DOTTIMES, DOTDIVIDE,   # matrix binary operators
              EQ, PLUSEQ, MINUSEQ, TIMESEQ, DIVEQ,      # assignment operators
              LT, GT, LE, GE, NE, EQEQ,                 # relational operators
              COLON,                                    # extent operator
              COMMA, SEMICOLON,                         # comma and semicolon
              IF, ELSE, FOR, WHILE,                     # keywords
              BREAK, CONTINUE, RETURN,                  # keywords
              EYE, ZEROS, ONES,                         # keywords
              PRINT,                                    # keyword
              ID,                                       # identifiers
              INTNUM,                                   # integers
              FLOATNUM,                                 # floating-point numbers
              STRING}                                   # strings

    literals = {"(", ")", "[", "]", "{", "}",           # brackets
                "'"}                                    # matrix transposition

    # String containing ignored characters between tokens (special name "ignore")
    ignore = " \t"
    ignore_comment = r"\#.*"

    # relational operators
    LE = r"<="         # Less than or equal to
    GE = r">="         # Greater than or equal to
    LT = r"<"          # Less than
    GT = r">"          # Greater than
    NE = r"!="         # Not equal
    EQEQ = r"=="       # Equal

    # assignment operators
    EQ = r"="          # Assignment
    PLUSEQ = r"\+="    # Plus equal
    MINUSEQ = r"-="    # Minus equal
    TIMESEQ = r"\*="   # Times equal
    DIVEQ = r"/="      # Divide equal

    # binary operators
    PLUS = r"\+"
    MINUS = r"-"
    TIMES = r"\*"
    DIVIDE = r"/"

    # matrix binary operators
    DOTPLUS = r"\.\+"
    DOTMINUS = r"\.-"
    DOTTIMES = r"\.\*"
    DOTDIVIDE = r"\./"

    # brackets assigned in literals

    # extent operator
    COLON = r":"

    # matrix transposition assigned in literals

    # comma and semicolon
    COMMA = r","
    SEMICOLON = r";"

    # identifiers
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"

    # keywords
    ID['if'] = IF
    ID['else'] = ELSE
    ID['for'] = FOR
    ID['while'] = WHILE
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID['return'] = RETURN
    ID['eye'] = EYE
    ID['zeros'] = ZEROS
    ID['ones'] = ONES
    ID['print'] = PRINT

    # floating-point numbers
    FLOATNUM = r"-?\d+\.(\d+)"

    # integers
    INTNUM = r"-?\d+"

    # strings
    STRING = r'".*?"'

    # Define a rule so we can track line numbers
    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print("Line %d: Bad character %r" % (self.lineno, t.value[0]))
        self.index += 1


if __name__ == "__main__":

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()

    lexer = Scanner()
    for tok in lexer.tokenize(text):
        print("line=%r, type=%r, value=%r" % (tok.lineno, tok.type, tok.value))
