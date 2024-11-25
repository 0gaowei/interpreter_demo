from lexer import Lexer

# 测试代码
source_code = """
// This is a comment
ORIGIN IS (360, 240);  -- Origin coordinates
SCALE IS (100, 100);
ROT IS PI/2;
FOR T FROM 0 TO 2*PI STEP PI/50 DRAW (cos(T), sin(T));
"""

lexer = Lexer(source_code)
tokens = lexer.tokenize()

for token in tokens:
    print(token)
for token in tokens:
    print(token.type, ':\t', token.lexeme)
