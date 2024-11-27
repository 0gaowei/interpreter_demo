from lexer.my_token import TokenType
from .my_ast import ASTNode


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # Token 列表
        self.position = 0  # 当前解析位置

    def current_token(self):
        """获取当前 Token"""
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def next_token(self):
        """移动到下一个 Token"""
        self.position += 1
        return self.current_token()

    def match(self, expected_type):
        """匹配当前 Token 类型"""
        token = self.current_token()
        # print(f"current_token: {token}") if token else print("current_token: None")
        if token and token.type == expected_type:
            self.next_token()
            return token
        self.error(f"Expected {expected_type}, but got {token.type if token else 'EOF'}")

    def error(self, message):
        """报告语法错误"""
        raise SyntaxError(f"Syntax Error at position {self.position}: {message}")

    def parse_program(self) -> ASTNode:
        """解析程序 Program → { Statement SEMICO }"""
        statements = []
        while self.current_token():
            print("\nP A R S E _ P R O G R A M\n")
            print(self.current_token())
            if self.current_token().type == TokenType.COMMENT:
                # 忽略注释
                self.match(TokenType.COMMENT)
                continue
            statements.append(self.parse_statement())
            self.match(TokenType.SEMICO)  # 每个语句以分号结束
        return ASTNode("Program", children=statements)

    def parse_statement(self):
        """解析语句 Statement → OriginStatement | ScaleStatement | ForStatement | RotStatement"""
        print("\n\tP A R S E _ S T A T E M E N T\n")
        token = self.current_token()
        # print("\tstart token:", token)
        if token.type == TokenType.ORIGIN:
            print("\n\t\tP A R S E _ O R I G I N _ S T A T E M E N T\n")
            return self.parse_origin_statement()
        elif token.type == TokenType.SCALE:
            print("\n\t\tP A R S E _ S C  A L E _ S T A T E M E N T\n")
            return self.parse_scale_statement()
        elif token.type == TokenType.ROT:
            print("\n\t\tP A R S E _ R O T _ S T A T E M E N T\n")
            return self.parse_rot_statement()
        elif token.type == TokenType.FOR:
            print("\n\t\tP A R S E _ F O R _ S T A T E M E N T\n")
            return self.parse_for_statement()
        else:
            self.error("Invalid statement")

    def parse_origin_statement(self):
        """OriginStatement → ORIGIN IS L_BRACKET Expression COMMA Expression R_BRACKET"""
        self.match(TokenType.ORIGIN)
        self.match(TokenType.IS)
        self.match(TokenType.L_BRACKET)
        expr1 = self.parse_expression()
        self.match(TokenType.COMMA)
        expr2 = self.parse_expression()
        self.match(TokenType.R_BRACKET)
        return ASTNode("OriginStatement", children=[expr1, expr2])

    def parse_scale_statement(self):
        """ScaleStatement → SCALE IS L_BRACKET Expression COMMA Expression R_BRACKET"""
        self.match(TokenType.SCALE)
        self.match(TokenType.IS)
        self.match(TokenType.L_BRACKET)
        expr1 = self.parse_expression()
        self.match(TokenType.COMMA)
        expr2 = self.parse_expression()
        self.match(TokenType.R_BRACKET)
        return ASTNode("ScaleStatement", children=[expr1, expr2])

    def parse_rot_statement(self):
        """RotStatement → ROT IS Expression"""
        self.match(TokenType.ROT)
        self.match(TokenType.IS)
        expr = self.parse_expression()
        return ASTNode("RotStatement", children=[expr])

    def parse_for_statement(self):
        """ForStatement → FOR T FROM Expression TO Expression STEP Expression
                            DRAW L_BRACKET Expression COMMA Expression R_BRACKET"""
        self.match(TokenType.FOR)
        loop_var = self.match(TokenType.T)
        self.match(TokenType.FROM)
        start_expr = self.parse_expression()
        self.match(TokenType.TO)
        end_expr = self.parse_expression()
        self.match(TokenType.STEP)
        step_expr = self.parse_expression()
        self.match(TokenType.DRAW)
        self.match(TokenType.L_BRACKET)
        draw_x = self.parse_expression()
        self.match(TokenType.COMMA)
        draw_y = self.parse_expression()
        self.match(TokenType.R_BRACKET)
        return ASTNode("ForStatement", children=[
            ASTNode("LoopVar", value=loop_var.lexeme),
            start_expr, end_expr, step_expr,
            ASTNode("Draw", children=[draw_x, draw_y])
        ])

    def parse_expression(self):
        """Expression → Term { ( PLUS | MINUS ) Term }"""
        left = self.parse_term()
        while self.current_token().type in {TokenType.PLUS, TokenType.MINUS}:
            op = self.match(self.current_token().type)
            right = self.parse_term()
            left = ASTNode("BinaryOp", value=op.lexeme, children=[left, right])
        return left

    def parse_term(self):
        """Term → Factor { ( MUL | DIV ) Factor }"""
        left = self.parse_factor()
        while self.current_token().type in {TokenType.MUL, TokenType.DIV}:
            op = self.match(self.current_token().type)
            right = self.parse_factor()
            left = ASTNode("BinaryOp", value=op.lexeme, children=[left, right])
        return left

    def parse_factor(self):
        """Factor → ( PLUS | MINUS ) Factor | Component"""
        token = self.current_token()
        if token.type in {TokenType.PLUS, TokenType.MINUS}:
            op = self.match(token.type)
            factor = self.parse_factor()
            return ASTNode("UnaryOp", value=op.lexeme, children=[factor])
        return self.parse_component()

    def parse_component(self):
        """Component → Atom [ POWER Component ]"""
        left = self.parse_atom()
        if self.current_token().type == TokenType.POWER:
            self.match(TokenType.POWER)
            right = self.parse_component()
            return ASTNode("Power", children=[left, right])
        return left

    def parse_atom(self):
        """Atom → CONST_ID | T | FUNC L_BRACKET Expression R_BRACKET | L_BRACKET Expression R_BRACKET"""
        token = self.current_token()
        if token.type == TokenType.CONST:
            return ASTNode("Constant", value=self.match(TokenType.CONST).func_ptr)
        elif token.type == TokenType.T:
            return ASTNode("Variable", value=self.match(TokenType.T).lexeme)
        elif token.type == TokenType.FUNC:
            func = self.match(TokenType.FUNC)
            self.match(TokenType.L_BRACKET)
            expr = self.parse_expression()
            self.match(TokenType.R_BRACKET)
            return ASTNode("FunctionCall", value=func.lexeme, children=[expr])
        elif token.type == TokenType.L_BRACKET:
            self.match(TokenType.L_BRACKET)
            expr = self.parse_expression()
            self.match(TokenType.R_BRACKET)
            return expr
        self.error("Invalid atom")
