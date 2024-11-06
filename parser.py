from sly import Parser
from scanner import Scanner


class Mparser(Parser):
    tokens = Scanner.tokens
    debugfile = 'parser.out'

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("nonassoc", '<', '>', 'LE', 'GE', 'EQ', 'NEQ'),
        ("left", '+', '-'),
        ("left", '*', '/'),
        ("right", 'UMINUS'),
    )

    start = 'program'

    @_('instruction program')
    def program(self, p):
        return [p.instruction, *p.program]

    @_('instruction')
    def program(self, p):
        return [p.instruction]

    @_('assignment', 
       'if_else_instr',
       'print_instr',
       'loop_instr',
       'block')
    def instruction(self, p):
        return p[0]

    #
    # ---------- ASSIGNMENT -----------
    #
    @_('access "="       value ";"',
       'access ADDASSIGN value ";"',
       'access SUBASSIGN value ";"',
       'access MULASSIGN value ";"',
       'access DIVASSIGN value ";"')
    def assignment(self, p):
        return (p[1], p.access, p.value)

    @_('ID', 'ID "[" indexes "]"')
    def access(self, p):
        return p.ID

    @_('integer "," indexes')
    def indexes(self, p):
        pass

    @_('integer')
    def indexes(self, p):
        pass

    @_('expr')
    def value(self, p):
        return p.expr

    #
    # ----------- IF ELSE INSTRUCTION ------------
    #
    @_('IF "(" expr ")" instruction %prec IFX')
    def if_else_instr(self, p):
        return ("if", p.expr, p.instruction)

    @_('IF "(" expr ")" instruction ELSE instruction')
    def if_else_instr(self, p):
        return ("if", p.expr, p.instruction0, p.instruction1)

    #
    # ----------- PRINT INSTRUCTION ------------
    #
    @_('PRINT args ";"')
    def print_instr(self, p):
        return ("print", p.args)

    @_('arg "," args')
    def args(self, p):
        return [p.arg, *p.args]

    @_('arg')
    def args(self, p):
        return [p.arg]

    @_('expr', 'STRING')
    def arg(self, p):
        return p[0]

    #
    # ----------- LOOP INSTRUCTIONS ------------
    #
    @_('WHILE "(" expr ")" instruction')
    def loop_instr(self, p):
        return ("while", p.expr, p.instruction)
    
    @_('FOR ID "=" integer ":" integer instruction')
    def loop_instr(self, p):
        return ("for", p.ID, p.integer0, p.integer1, p.instruction)

    @_('ID', 'INTNUM')
    def integer(self, p):
        return p[0]


    # ------- BLOCK --------
    @_('"{" program "}"')
    def block(self, p):
        return p.program

    #
    # ----------- EXPRESSION -------------
    #
    @_('expr "+" expr',
       'expr "-" expr',
       'expr "*" expr',
       'expr "/" expr',
       'expr "<" expr',
       'expr ">" expr',
       'expr LE expr',
       'expr GE expr',
       'expr EQ expr',
       'expr NEQ expr',
       )
    def expr(self, p):
        return (p[1], p.expr0, p.expr1)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('"-" expr %prec UMINUS ')
    def expr(self, p):
        return ("-", p.expr)

    @_('INTNUM', 
       'FLOATNUM', 
       'ID')
    def expr(self, p):
        return p[0]
