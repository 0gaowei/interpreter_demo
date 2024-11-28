from lexer.lexer import Lexer
from parser.parser import Parser
from semantics.semantics import Semantics

# 输入源代码
source_code = """
// This is a comment
ROT IS 0;
ORIGIN IS (50, 400);  -- Origin coordinates
SCALE IS (2, 1);  -- Scale factors
FOR T FROM 0 TO 2*PI STEP PI/50 DRAW (cos(T), sin(T));
"""

# 词法分析
lexer = Lexer(source_code)
tokens = lexer.tokenize()

# 语法分析
parser = Parser(tokens)
ast_root = parser.parse_program()
print(ast_root)

# 语义分析
semantics = Semantics()
semantics.eval(ast_root)

# 显示绘图
semantics.show_plot()
