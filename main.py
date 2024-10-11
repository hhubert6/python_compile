from sly import Lexer


class Scanner(Lexer):
    # Set of token names.   This is always required
    tokens = {ID, IF, ELSE, WHILE, FOR, ZEROS, PRINT, NUMBER, PLUS, MINUS, TIMES, DIVIDE, ASSIGN, LPAREN, RPAREN, SEMICOLON}

    # String containing ignored characters between tokens
    ignore = " \t"
    ignore_comment = r"\#.*"

    # Regular expression rules for tokens
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    # keywords
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['for'] = FOR

#     ID['break'] = BREAK
#     ID['continue'] = CONTINUE
#     ID['return'] = RETURN
# 
#     ID['eye'] = EYE
    ID['zeros'] = ZEROS
#     ID['ones'] = ONES

    ID['print'] = PRINT

    NUMBER = r"\d+"
    SEMICOLON = r";"
    # binary operators
    PLUS = r"\+"
    MINUS = r"-"
    TIMES = r"\*"
    DIVIDE = r"/"
    # matrix binary operators
    # PLUS = r"\+"
    # MINUS = r"-"
    # TIMES = r"\*"
    # DIVIDE = r"/"

    ASSIGN = r"="
    LPAREN = r"\("
    RPAREN = r"\)"

    # Define a rule so we can track line numbers
    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print("Line %d: Bad character %r" % (self.lineno, t.value[0]))
        self.index += 1


if __name__ == "__main__":
    data = """A = zeros(5);"""
    lexer = Scanner()
    for tok in lexer.tokenize(data):
        print("line=%r, type=%r, value=%r" % (tok.lineno, tok.type, tok.value))
