from sly import Parser
from scanner import Scanner


class Mparser(Parser):
    tokens = Scanner.tokens
    debugfile = 'parser.out'

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("nonassoc", '<', '>', 'LE', 'GE', 'EQ', 'NEQ'),
        ("left", '+', '-', 'DOTADD', 'DOTSUB'),
        ("left", '*', '/', 'DOTMUL', 'DOTDIV'),
        ("right", "\'"),
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
       'block',
       'return_instr',
       'BREAK ";"',
       'CONTINUE ";"')
    def instruction(self, p):
        return p[0]

    # @_('error')
    # def instruction(self, p):
    #     return "error"

    #
    # ---------- ASSIGNMENT -----------
    #
    @_('ref "="       expr ";"',
       'ref "="     STRING ";"',
       'ref ADDASSIGN expr ";"',
       'ref SUBASSIGN expr ";"',
       'ref MULASSIGN expr ";"',
       'ref DIVASSIGN expr ";"')
    def assignment(self, p):
        return (p[1], p.ref, p[2])

    @_('ID')
    def ref(self, p):
        return p.ID

    @_('ID "[" indexes "]"')
    def ref(self, p):
        return ('ref', p.ID, p.indexes)

    @_('integer "," indexes')
    def indexes(self, p):
        return [p.integer, *p.indexes]

    @_('integer')
    def indexes(self, p):
        return [p.integer]

    #
    # ----------- IF ELSE INSTRUCTION ------------
    #
    @_('IF "(" expr ")" instruction %prec IFX')
    def if_else_instr(self, p):
        return ("if", p.expr, ("then", p.instruction))

    @_('IF "(" expr ")" instruction ELSE instruction')
    def if_else_instr(self, p):
        return ("if", p.expr, ("then", p.instruction0), ("else", p.instruction1))

    #
    # ----------- PRINT INSTRUCTION ------------
    #
    @_('PRINT args ";"')
    def print_instr(self, p):
        return ("print", p.args)

    # @_('PRINT error ";"')
    # def print_instr(self, p):
    #     return ("print", "error")

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

    #
    # ------- BLOCK --------
    #
    @_('"{" program "}"')
    def block(self, p):
        return p.program

    #
    # ------- RETURN INSTRUCTION --------
    #
    @_('RETURN expr ";"')
    def return_instr(self, p):
        return ("return", p.expr)

    #
    # ----------- EXPRESSION -------------
    #
    @_('expr "+" expr',
       'expr DOTADD expr',
       'expr "-" expr',
       'expr DOTSUB expr',
       'expr "*" expr',
       'expr DOTMUL expr',
       'expr "/" expr',
       'expr DOTDIV expr',
       'expr "<" expr',
       'expr ">" expr',
       'expr LE expr',
       'expr GE expr',
       'expr EQ expr',
       'expr NEQ expr')
    def expr(self, p):
        return (p[1], p.expr0, p.expr1)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('"-" expr %prec UMINUS ')
    def expr(self, p):
        return ("-", p.expr)

    @_('expr "\'"')
    def expr(self, p):
        return ("transpose", p.expr)

    @_('EYE "(" expr ")"', 
       'ZEROS "(" expr ")"',
       'ONES "(" expr ")"')
    def expr(self, p):
        return (p[0], p.expr)

    @_('vector',
       'INTNUM', 
       'FLOATNUM', 
       'ID')
    def expr(self, p):
        return p[0]

    #
    # ---------- VECTOR INITILIZATION ---------
    #
    @_('"[" innerlist "]"')
    def vector(self, p):
        return ("vector", p.innerlist)

    @_('expr "," innerlist')
    def innerlist(self, p):
        return [p.expr, *p.innerlist]

    @_('expr')
    def innerlist(self, p):
        return [p.expr]

