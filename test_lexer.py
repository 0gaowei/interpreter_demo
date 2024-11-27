from lexer.lexer import Lexer

# 测试代码
source_code = """
// This is a comment
ORIGIN IS (360, 240);  -- Origin coordinates
SCALE IS (100, 100);
ROT IS PI/2;
FOR T FROM 0 TO 2*PI STEP PI/50 DRAW (cos(T), sin(T));
"""

lexer = Lexer(source_code)
tokens = lexer.tokenize()   # TODO: 记号在源程序中的位置信息，用于报错或调试

test_expression = """-16+5**3/cos(T);"""

lexer2 = Lexer(test_expression)
tokens2 = lexer2.tokenize()   # TODO: 记号在源程序中的位置信息，用于报错或调试
