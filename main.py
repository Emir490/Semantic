import lexer
from grammar import parser

with open('data/sample.txt', 'r') as f:
    data = f.read()

lexer.lexer.input(data)

# for tok in lexer.lexer:
#     print(f"Type: {tok.type}, Value: {tok.value}, Line: {tok.lineno}, Position: {tok.lexpos}")  
    
result = parser.parse(data)
