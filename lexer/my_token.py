from enum import Enum


class TokenType(Enum):
    # 定义Token的类别
    COMMENT = 0  # 注释
    ORIGIN = 1  # 原点
    SCALE = 2  # 缩放
    ROT = 3  # 旋转
    IS = 4  # 是
    TO = 5  # 到
    STEP = 6  # 步长
    DRAW = 7  # 画图
    FOR = 8  # 循环
    FROM = 9  # 从

    T = 10

    SEMICO = 11  # 分号
    L_BRACKET = 12  # 左括号
    R_BRACKET = 13  # 右括号
    COMMA = 14  # 逗号

    PLUS = 15  # 加号
    MINUS = 16  # 减号
    MUL = 17  # 乘号
    DIV = 18  # 除号
    POWER = 19  # 幂

    FUNC = 20  # 函数
    CONST = 21  # 常量
    NONTOKEN = 22  # 非Token
    ERRTOKEN = 23  # 错误Token
    ASSIGN = 24  # 赋值


class Token:
    def __init__(self, type_: TokenType, lexeme: str, value: float = None, func_ptr=None):
        self.type = type_       # Token类型
        self.lexeme = lexeme    # 原始字符串
        self.value = value      # Token值
        self.func_ptr = func_ptr  # 函数指针，指向数学函数（如sin, cos等）

    def __repr__(self):
        # 打印Token信息：类型，词素，值，函数指针
        return f"{self.type}, \n{self.lexeme}, \t{self.value}, \t{self.func_ptr}"
