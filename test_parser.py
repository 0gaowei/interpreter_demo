from lexer.lexer import Lexer  # 导入词法分析器
from parser.parser import Parser  # 导入语法分析器


# 输入源代码
source_code = """
// This is a comment
ORIGIN IS (360, 240);  -- Origin coordinates
SCALE IS (100, 100);
ROT IS PI/2;
FOR T FROM 0 TO 2*PI STEP PI/50 DRAW (cos(T), sin(T));
"""

test_expression = """-16+5**3/cos(T);
"""

# 初始化词法分析器
lexer = Lexer(source_code)
tokens = lexer.tokenize()  # 执行词法分析，生成Token列表

# 初始化语法分析器
parser = Parser(tokens)
try:
    ast = parser.parse_program()  # 执行语法分析，生成AST
    print("\nAbstract Syntax Tree (AST):")
    print(ast)  # 打印生成的抽象语法树
except SyntaxError as e:
    print("\nSyntax Error encountered:")
    print(e)


lexer = Lexer(test_expression)
tokens = lexer.tokenize()  # 执行词法分析，生成Token列表

parser = Parser(tokens)
try:
    ast = parser.parse_expression()  # 执行语法分析，生成AST
    print("\nAbstract Syntax Tree (AST):")
    print(ast)  # 打印生成的抽象语法树
except SyntaxError as e:
    print("\nSyntax Error encountered:")
    print(e)
