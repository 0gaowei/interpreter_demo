from .my_token import Token, TokenType
from .dfa import DFA
from .symbol_table import SymbolTable
import string


class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code  # 源代码字符串
        self.position = 0    # 当前位置, 指向下一个要处理的字符
        self.tokens = []     # 保存Token的列表
        self.dfa = DFA()  # 使用DFA进行状态机管理

    # 获取下一个Token
    def get_token(self):
        lexeme = ''
        while self.position < len(self.source_code):
            curr_char = self.source_code[self.position]  # 取出当前字符
            self.position += 1  # 移动到下一个字符
            curr_char_class = self.char_classification(curr_char)  # 字符分类
            next_state = self.dfa.curr_state.get_next_state(curr_char_class)  # 获取下一个状态
            if curr_char_class == 'blank':  # 空白字符
                if lexeme:  # 词素不为空，则返回Token
                    if self.dfa.curr_state.name == 'MIX':
                        if lexeme == '**':
                            return Token(TokenType.MUL, lexeme)
                        elif lexeme == '+':
                            return Token(TokenType.PLUS, lexeme)
                        elif lexeme == '//' or lexeme == '--':
                            while self.source_code[self.position] != '\n':
                                self.position += 1
                            return Token(TokenType.COMMENT, lexeme)
                        elif lexeme == ',':
                            return Token(TokenType.COMMA, lexeme)
                        elif lexeme == ';':
                            return Token(TokenType.SEMICO, lexeme)
                        elif lexeme == '(':
                            return Token(TokenType.L_BRACKET, lexeme)
                        elif lexeme == ')':
                            return Token(TokenType.R_BRACKET, lexeme)
                        elif lexeme == '=':
                            return Token(TokenType.ASSIGN, lexeme)
                    elif self.dfa.curr_state.name == 'ID':
                        # TODO: 判断是否为关键字或标识符
                        return SymbolTable.lookup(lexeme)
                    elif self.dfa.curr_state.name == 'NUMBER':
                        return Token(TokenType.CONST, lexeme, func_ptr=int)
                    elif self.dfa.curr_state.name == 'POINT':
                        return Token(TokenType.CONST, lexeme, func_ptr=float)
                    elif self.dfa.curr_state.name == 'MUL':
                        return Token(TokenType.MUL, lexeme)
                    elif self.dfa.curr_state.name == '/':
                        return Token(TokenType.DIV, lexeme)
                    elif self.dfa.curr_state.name == 'MINUS':
                        return Token(TokenType.MINUS, lexeme)
                else:  # 词素为空，则继续读取
                    return None
            else:  # 非空白字符
                if next_state is None:  # 到达终点，返回Token
                    self.position -= 1  # 回退到上一个字符
                    if lexeme:  # 词素不为空，则返回Token
                        if self.dfa.curr_state.name == 'MIX':
                            if lexeme == '**':
                                return Token(TokenType.MUL, lexeme)
                            elif lexeme == '+':
                                return Token(TokenType.PLUS, lexeme)
                            elif lexeme == '//' or lexeme == '--':
                                while self.source_code[self.position] != '\n':
                                    self.position += 1
                                return Token(TokenType.COMMENT, lexeme)
                            elif lexeme == ',':
                                return Token(TokenType.COMMA, lexeme)
                            elif lexeme == ';':
                                return Token(TokenType.SEMICO, lexeme)
                            elif lexeme == '(':
                                return Token(TokenType.L_BRACKET, lexeme)
                            elif lexeme == ')':
                                return Token(TokenType.R_BRACKET, lexeme)
                            elif lexeme == '=':
                                return Token(TokenType.ASSIGN, lexeme)
                        elif self.dfa.curr_state.name == 'ID':
                            # TODO: 判断是否为关键字或标识符
                            return SymbolTable.lookup(lexeme)
                        elif self.dfa.curr_state.name == 'NUMBER':
                            return Token(TokenType.CONST, lexeme, func_ptr=int)
                        elif self.dfa.curr_state.name == 'POINT':
                            return Token(TokenType.CONST, lexeme, func_ptr=float)
                        elif self.dfa.curr_state.name == 'MUL':
                            return Token(TokenType.MUL, lexeme)
                        elif self.dfa.curr_state.name == '/':
                            return Token(TokenType.DIV, lexeme)
                        elif self.dfa.curr_state.name == 'MINUS':
                            return Token(TokenType.MINUS, lexeme)
                else:  # 未到达终点，加入词素
                    lexeme += curr_char  # 加入词素
            ''' # 调试信息
            print(f"当前状态：{self.dfa.curr_state.name}，\t当前字符：{repr(curr_char)}，"
                  f"\t分类：{curr_char_class}；\t词素：{repr(lexeme)}，"
                  f"\t下一个状态：{next_state.name if next_state else 'None'}")
                  '''
            self.dfa.curr_state = next_state  # 更新状态机状态

    # 输入字符串进行分类
    @staticmethod
    def char_classification(ch):
        if ch in string.ascii_letters:  # 字母
            return 'letter'
        elif ch in string.digits:  # 数字
            return 'digit'
        elif ch in '*+-/,;()':  # 运算符
            return ch
        elif ch in '\t\n\r ':  # 空白字符
            return 'blank'
        else:
            return 'error'  # 非法字符

    # 词法分析
    def tokenize(self):
        # 打印源代码长度和字符数
        print(f"词法分析开始...\n源代码长度：{len(self.source_code)}，字符数：{len(self.source_code.replace(' ', ''))}")
        while self.position < len(self.source_code):
            self.dfa.curr_state = self.dfa.start_state  # 重置状态机状态
            token = self.get_token()
            if token:
                # print(f"Token：{token}")   # 打印Token
                self.tokens.append(token)

        # 打印Token
        print("Token列表：")
        for token in self.tokens:
            print(token)

        print(f"词法分析结束，共生成{len(self.tokens)}个Token。")
        return self.tokens
