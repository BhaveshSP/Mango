from src.Lexer import *
from src.Parser import * 
from src.Interpreter import * 
from include.Error import *
from include.Util import *
from include.Values import * 

# Create A Global Symbol Table 
global_symbol_table = SymbolTable()
# Set Prdefined Values for Certain Keywords
global_symbol_table.set("null",Number(0))
global_symbol_table.set("True",Number(1))
global_symbol_table.set("False",Number(0))

# Runner 
def run(file_name,text):
	
	# Initialize the Lexer 
	lexer = Lexer(file_name,text)

	# Tokenize the Input Stream 
	tokens,error = lexer.tokenize()
	if error : return None,error
	# print(tokens)

	# Initialize the Parser 
	parser = Parser(tokens)
	# AST - Abstract Syntax Tree  
	# Create a AST  
	ast = parser.parse()
	if ast.error :
		return None , ast.error 
	# print(ast)
	# Initialize the Interpreter 
	interpreter = Interpreter()
	# Create Root Context 
	context = Context("<shell>")
	context.symbol_table = global_symbol_table 
	# Get the Result from the Evaluation of the Expression 
	result = interpreter.visit(ast.node,context)
	
	return result.value,result.error 
