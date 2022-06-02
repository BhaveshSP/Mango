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
			return result 
		context.symbol_table.set(var_name,var_value)
		temp  = context.symbol_table
		while temp.get(var_name) != None :
			temp = temp.parent
			if temp == None:
				break
			if temp.get(var_name) == None:
				break
			temp.set(var_name,var_value)  
		var_value = var_value.copy().set_context(context).set_position(node.position_start,node.position_end)
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

	# Get result after executing if condition
	def visit_IfOperatorNode(self,node,context):
		result = RuntimeResult()
		cases = node.cases
		value = None 
		for condition,expr in cases:
			condition_evaluation = result.register(self.visit(condition,context))
			if result.error :
				return result 
			if condition_evaluation.is_true():
				value = result.register(self.visit(expr,context))
				if result.error :
					return result 
				break
		if value == None :
			value = result.register(self.visit(node.else_node ,context))
			if result.error:
				return result 
		return result.success(value)


	# Get result after executing if condition
	def visit_ForOperatorNode(self,node,context):
		result = RuntimeResult()

		start_value = result.register(self.visit(node.start_value_node,context))
		if result.error:
			return result 
		end_value = result.register(self.visit(node.end_value_node,context))
		if result.error:
			return result 
		step_value = None 
		if node.step_value_node:
			step_value = result.register(self.visit(node.step_value_node,context))
			if result.error:
				return result 
		else:
			step_value = Number(1)
		i = start_value.value 
		condition = None 
		if step_value.value >= 0:
			condition = lambda : i <= end_value.value 
		else:
			condition = lambda : i >= end_value.value 

		while condition() :

			context.symbol_table.set(node.var_name_token.value,Number(i))
			i += step_value.value 
			result.register(self.visit(node.body_node,context))
			if result.error :
				return result 


		return result.success(None)



	# Get result after executing if condition
	def visit_WhileOperatorNode(self,node,context):
		result = RuntimeResult()

		while True :
			
			condition_evaluation = result.register(self.visit(node.condition_node,context))
			
			if result.error :
				return result 

			if not condition_evaluation.is_true():
				break 
			result.register(self.visit(node.body_node,context))
			if result.error :
				return result
			 
		return result.success(None)

	def visit_FunctionDefinitionNode(self,node,context):
		result = RuntimeResult()
		name = None 
		if node.var_name_token :
			name = node.var_name_token.value 
		body_node = node.body_node
		arg_names = [arg.value for arg in node.arg_name_tokens]

		func_value = Function(name,arg_names,body_node).set_context(context).set_position(node.position_start,node.position_end)

		if name:
			context.symbol_table.set(name,func_value)

		return result.success(func_value)

	def visit_CallNode(self,node,context):
		result = RuntimeResult()
		args = [] 

		value_to_call = result.register(self.visit(node.node_to_call,context))
		if result.error:
			return result 

		value_to_call = value_to_call.copy().set_context(context).set_position(node.position_start,node.position_end)
		
		for arg_node in node.arg_nodes:
			args.append(result.register(self.visit(arg_node,context)))
			if result.error :
				return result

		result_new = RuntimeResult()
		interpreter_new = Interpreter()

		return_value = result.register(value_to_call.execute(args,result_new,interpreter_new))
		if result.error:
			return result
		return result.success(return_value)

	def visit_StringNode(self,node,context):	
		return RuntimeResult().success(String(node.token.value).set_context(context).set_position(node.position_start,node.position_end))



