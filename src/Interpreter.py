from include.Values import * 
from include.Types import *

# Result Class to Handle the Value and Error of the Interpreter 
class RuntimeResult:
	
	def __init__(self):
		self.value = None
		self.error = None 

	# Register the result returned from a function 
	# helps to check if any error occurred 
	def register(self,node):
		if node.error: self.error = node.error 
		return node.value 
	
	def success(self,value):
		self.value = value 
		return self 

	def failure(self,error):
		self.error = error 
		return self 


class Interpreter: 
	# Visit a Node in the AST 
	def visit(self,node,context):
		self.node = node 
		self.context = context
		# Get the Node Type Name 
		method_name = f"visit_{type(node).__name__}"
		# Get the visit_NodeTypeName
		method = getattr(self,method_name,self.no_such_method)

		return method(node,context)

	# If No such method is implemented for a node type a default method is called 
	def no_such_method(self,node,context):
		raise Exception(f"No such visit method defined 'visit_{type(node).__name__}'")

	# Get the Number from node 
	def visit_NumberNode(self,node,context):
		result = RuntimeResult()
		return result.success(Number(node.token.value).set_context(context).set_position(node.position_start,node.position_end))
	
	# Get result of Performing Binary Operator 
	def visit_BinaryOperatorNode(self,node,context):
		result = RuntimeResult()
		left_child = result.register(self.visit(node.left_node,context))
		if result.error : return result 
		right_child = result.register(self.visit(node.right_node,context))
		if result.error : return result 
		number = None 
		error = None 

		# Perform Addition for Plus Type Operator 
		if node.operator_node.type == TT_PLUS:
			number, error = left_child.added_to(right_child)
		# Perform Substraction for Minus Type Operator
		elif node.operator_node.type == TT_MINUS:
			number, error =  left_child.subtracted_by(right_child)
		# Perform Multiplication for Multiply Type Operator
		elif node.operator_node.type == TT_MUL:
			number, error  = left_child.multiply_by(right_child)
		# Perform Division for Type Division Operator
		elif node.operator_node.type == TT_DIV:
			number, error =  left_child.divide_by(right_child)
		# Perform Addition for Type Power Operator
		elif node.operator_node.type == TT_POW:
			number, error = left_child.power(right_child)
		# Perform Addition for Type Double Equals Operator
		elif node.operator_node.type == TT_EE:
			number, error = left_child.get_comparsion_equals(right_child)
		# Perform Addition for Type Not Equals Operator
		elif node.operator_node.type == TT_NE:
			number, error = left_child.get_comparsion_not_equals(right_child)
		# Perform Addition for Type Less than Operator
		elif node.operator_node.type == TT_LT:
			number, error = left_child.get_comparsion_less_than(right_child)
		# Perform Addition for Type Less than Eqaul to Operator
		elif node.operator_node.type == TT_LTE:
			number, error = left_child.get_comparsion_less_than_equal(right_child)
		# Perform Addition for Type Greater than Operator
		elif node.operator_node.type == TT_GT:
			number, error = left_child.get_comparsion_greater_than(right_child)
		# Perform Addition for Type Greater than Equal Operator
		elif node.operator_node.type == TT_GTE:
			number, error = left_child.get_comparsion_greater_than_equal(right_child)

		# Perform Addition for Type And Operator
		elif node.operator_node.matches(TT_KEYWORD,"and"):
			number, error = left_child.anded_by(right_child)
		# Perform Addition for Type Or Operator
		elif node.operator_node.matches(TT_KEYWORD,"or"):
			number, error = left_child.or_by(right_child)
		# If Error found return Failure 
		if error :
			return result.failure(error)
		else:
			# Otherwise return Result Number 
			return result.success(number.set_position(node.position_start,node.position_end))
		
	# Get the Result after performing the Unary Operation
	def visit_UnaryOperatorNode(self,node,context):
		result = RuntimeResult()
		child = result.register(self.visit(node.node,context))
		if result.error : return result 
		error = None 

		# Perform Muplication by -1 is Minus Unary Operator Type 
		if node.operator_node.type == TT_MINUS:
			child,error =  child.multiply_by(Number(-1))
		# Perform Negation on the Condition result 
		elif node.operator_node.matches(TT_KEYWORD,"not"):
			child,error = child.not_by()
		if error :
			return result.failure(child.set_position(node.position_start,node.position_end))
		else:
			return result.success(child.set_position(node.position_start,node.position_end))

	# Assign the Value to the Varible in the Symbol Table 
	def visit_VarAssignNode(self,node,context):
		result = RuntimeResult()
		var_name = node.var_name_token 
		# Get the result of the expression 
		var_value = result.register(self.visit(node.var_value_node,context))
		if result.error :
			result 
		context.symbol_table.set(var_name,var_value)
		var_value = var_value.copy().set_position(node.position_start,node.position_end)
		return result.success(var_value)

	# Access the Value of the Variable in the Symbol Table 
	def visit_VarAccessNode(self,node,context):
		result = RuntimeResult()
		var_name = node.var_name_token.value 
		# Get the value of the variable from the symbol table if exist
		value = context.symbol_table.get(var_name)
		if value == None :
			# if the variable doesn't exist return error
			return result.failure(RuntimeError(f"'{var_name}' is not defined",node.position_start,node.position_end,context))
		return result.success(value)
