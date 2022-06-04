from src.Lexer import *
from src.Parser import * 
from src.Interpreter import * 
from include.Error import *
from include.Util import *
from include.Values import * 

# Create A Global Symbol Table 
global_symbol_table = SymbolTable()
# Set Prdefined Values for Certain Keywords
global_symbol_table.set("null",Number.null)
global_symbol_table.set("True",Number.true)
global_symbol_table.set("False",Number.false)
global_symbol_table.set("MAX_INT",Number.MAX_INT)
global_symbol_table.set("MIN_INT",Number.MIN_INT)
global_symbol_table.set("MATH_PI",Number.MATH_PI)
global_symbol_table.set("Print",BuiltInFunction.print)
# global_symbol_table.set("Return",BuiltInFunction.return_)
global_symbol_table.set("Clear",BuiltInFunction.clear)
global_symbol_table.set("Cls",BuiltInFunction.clear)
global_symbol_table.set("Input",BuiltInFunction.input_)
global_symbol_table.set("Input_Number",BuiltInFunction.input_number)
global_symbol_table.set("isNumber",BuiltInFunction.is_number)
global_symbol_table.set("isString",BuiltInFunction.is_string)
global_symbol_table.set("isList",BuiltInFunction.is_list)
global_symbol_table.set("isFunction",BuiltInFunction.is_function)
global_symbol_table.set("Insert",BuiltInFunction.insert)
global_symbol_table.set("Pop",BuiltInFunction.pop)
global_symbol_table.set("Extend",BuiltInFunction.extend)
global_symbol_table.set("Length",BuiltInFunction.length)




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
	# print(tokens)
	ast = parser.parse()
	if ast.error :
		return None , ast.error 
	# Initialize the Interpreter 
	interpreter = Interpreter()
	# Create Root Context 
	context = Context("<shell>")
	context.symbol_table = global_symbol_table 
	# Get the Result from the Evaluation of the Expression 
	result = interpreter.visit(ast.node,context)
	
	return result.value,result.error 
