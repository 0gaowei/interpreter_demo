import math
from .my_token import Token, TokenType


class SymbolTable:
    # 符号表，用于存储标识符和其对应的Token，格式为{标识符:Token（包括类型、值、函数指针）}
    SYMBOL_TABLE = {
        'PI':    Token(TokenType.CONST,     'PI',      func_ptr=math.pi),
        'E':     Token(TokenType.CONST,     'E',       func_ptr=math.e),
        'T':     Token(TokenType.T,         'T'),
        'SIN':   Token(TokenType.FUNC,      'SIN',     func_ptr=math.sin),
        'COS':   Token(TokenType.FUNC,      'COS',     func_ptr=math.cos),
        'TAN':   Token(TokenType.FUNC,      'TAN',     func_ptr=math.tan),
        'LN':    Token(TokenType.FUNC,      'LN',      func_ptr=math.log),
        'EXP':   Token(TokenType.FUNC,      'EXP',     func_ptr=math.exp),
        'SQRT':  Token(TokenType.FUNC,      'SQRT',    func_ptr=math.sqrt),
        'ORIGIN': Token(TokenType.ORIGIN,   'ORIGIN'),
        'SCALE': Token(TokenType.SCALE,     'SCALE'),
        'ROT':   Token(TokenType.ROT,       'ROT'),
        'IS':    Token(TokenType.IS,        'IS'),
        'FOR':   Token(TokenType.FOR,       'FOR'),
        'FROM':  Token(TokenType.FROM,      'FROM'),
        'TO':    Token(TokenType.TO,        'TO'),
        'STEP':  Token(TokenType.STEP,      'STEP'),
        'DRAW':  Token(TokenType.DRAW,      'DRAW'),
    }

    @classmethod
    # 查找符号表中是否存在指定的标识符，如果存在，返回Token，否则返回None
    def lookup(cls, name):
        return cls.SYMBOL_TABLE.get(name.upper(), None)
