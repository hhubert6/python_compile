from sly import Parser
from scanner import Scanner


class Mparser(Parser):
    tokens = Scanner.tokens
    debugfile = 'parser.out'

    precedence = (
        # ("nonassoc", '<', '>'),
        ("left", '+', '-'),
        ("left", '*', '/'),
        ("right", 'UMINUS'),
    )

    start = 'program'

    @_('instruction ";" program')
    def program(self, p):
        return [p.instruction, *p.program]

    @_('instruction ";"')
    def program(self, p):
        return [p.instruction]

    @_('assignment')
       # 'loop_instr',
       # 'function')
    def instruction(self, p):
        return p[0]

    @_('ID "=" value',
       'ID ADDASSIGN value',
       'ID SUBASSIGN value',
       'ID MULASSIGN value',
       'ID DIVASSIGN value')
    def assignment(self, p):
        return (p[1], p.ID, p.value)

    @_('expr')
    def value(self, p):
        return p.expr

    @_('expr "+" expr',
       'expr "-" expr',
       'expr "*" expr',
       'expr "/" expr')
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
