from include.Lexer import *

# Runner 
def run(file_name,text):
	lexer = Lexer(file_name,text)
	tokens,error = lexer.tokenize()
	return tokens,error