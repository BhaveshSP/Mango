from src.Lexer import *
from src.Parser import * 
from include.Error import *
# Runner 
def run(file_name,text):
	
	# Initialize the Lexer 
	lexer = Lexer(file_name,text)
	# Tokenize the Input Stream 
	tokens,error = lexer.tokenize()
	if error : return None,error
	# Initialize the Parser 
	parser = Parser(tokens)
	# # AST - Abstract Syntax Tree  
	# # Create a AST  
	ast = parser.parse()
	return ast.node, ast.error 
