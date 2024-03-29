from include.Values import * 
from include.Types import *


# Result Class to Handle the Value and Error of the Interpreter 
class RuntimeResult:
	

	def __init__(self):
		self.reset()


	def reset(self):
		self.value = None
		self.error = None
		self.function_return_value =  None 
		self.loop_continue = False
		self.loop_break  = False 


	# Register the result returned from a function 
	# helps to check if any error occurred 
	def register(self,node):
		self.error = node.error 
		self.function_return_value =  node.function_return_value 
		self.loop_continue = node.loop_continue
		self.loop_break  = node.loop_break 
		return node.value 
	

	def success(self,value):
		self.reset()
		self.value = value 
		return self 


	def success_return(self,value):
		self.reset()
		self.function_return_value = value 
		return self 


	def success_continue(self):
		self.reset()
		self.loop_continue = True  
		return self 

	
	def success_break(self):
		self.reset()
		self.loop_break = True  
		return self 


	def failure(self,error):
		self.error = error 
		return self 


	def should_return(self):
		return (self.error or self.function_return_value or self.loop_break or self.loop_continue)


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
		if result.should_return() : return result 
		right_child = result.register(self.visit(node.right_node,context))
		if result.should_return() : return result 
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

		# Perform Modulus for Type Modulus Operator
		elif node.operator_node.type == TT_MOD:
			number, error =  left_child.moded_by(right_child)
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
		if result.should_return() : return result 
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
		if result.should_return() :
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
		value = value.copy().set_context(context).set_position(node.position_start,node.position_end)
		return result.success(value)


	# Get result after executing if condition
	def visit_IfOperatorNode(self,node,context):
		result = RuntimeResult()
		cases = node.cases
		value = None 
		for condition,expr,should_return_null in cases:
			condition_evaluation = result.register(self.visit(condition,context))
			if result.should_return() :
				return result 
			if condition_evaluation.is_true():
				value = result.register(self.visit(expr,context))
				if result.should_return() :
					return result 
				return result.success(Number.null if should_return_null else value)
		if node.else_node != None :
			should_return_null = node.else_node[1]
			value = result.register(self.visit(node.else_node[0] ,context))
			if result.should_return():
				return result 
			return result.success(Number.null if should_return_null else value)
		return result.success(Number.null)


	# Get result after executing if condition
	def visit_ForOperatorNode(self,node,context):
		result = RuntimeResult()
		elements = [] 
		start_value = result.register(self.visit(node.start_value_node,context))
		if result.should_return():
			return result 
		end_value = result.register(self.visit(node.end_value_node,context))
		if result.should_return():
			return result 
		step_value = None 
		if node.step_value_node:
			step_value = result.register(self.visit(node.step_value_node,context))
			if result.should_return():
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
			value = result.register(self.visit(node.body_node,context))
			if result.should_return() and result.loop_continue == False and result.loop_break == False :
				return result 
			if result.loop_continue :
				continue 
			if result.loop_break:
				break 
			elements.append(value)


		return result.success(Number.null if node.should_return_null else List(elements).set_context(context).set_position(node.position_start,node.position_end))



	# Get result after executing if condition
	def visit_WhileOperatorNode(self,node,context):

		result = RuntimeResult()
		elements = [] 

		while True :
			condition_evaluation = result.register(self.visit(node.condition_node,context))
			if result.should_return() :
				return result 
			if not condition_evaluation.is_true():
				break 
			value = result.register(self.visit(node.body_node,context))
			if result.should_return() and result.loop_continue == False and result.loop_break == False :
				return result 
			if result.loop_continue :
				continue 
			if result.loop_break:
				break 
			elements.append(value)

		return result.success(Number.null if node.should_return_null else List(elements).set_context(context).set_position(node.position_start,node.position_end))


	def visit_FunctionDefinitionNode(self,node,context):
		result = RuntimeResult()
		name = None 
		if node.var_name_token :
			name = node.var_name_token.value 
		body_node = node.body_node
		arg_names = [arg.value for arg in node.arg_name_tokens]

		func_value = Function(name,arg_names,body_node,node.should_auto_return).set_context(context).set_position(node.position_start,node.position_end)

		if name:
			context.symbol_table.set(name,func_value)

		return result.success(func_value)


	def visit_CallNode(self,node,context):
		result = RuntimeResult()
		args = [] 

		value_to_call = result.register(self.visit(node.node_to_call,context))
		if result.should_return():
			return result 

		value_to_call = value_to_call.copy().set_context(context).set_position(node.position_start,node.position_end)
		
		for arg_node in node.arg_nodes:
			args.append(result.register(self.visit(arg_node,context)))
			if result.should_return():
				return result

		result_new = RuntimeResult()
		interpreter_new = Interpreter()
		return_value = result.register(value_to_call.execute(args,result_new,interpreter_new))
		if result.should_return():
			return result
		result_value = return_value.copy().set_context(context).set_position(node.position_start,node.position_end)
		return result.success(return_value)


	def visit_StringNode(self,node,context):	
		return RuntimeResult().success(String(node.token.value).set_context(context).set_position(node.position_start,node.position_end))


	def visit_ListNode(self,node,context):	
		result = RuntimeResult()
		elements = [] 

		for element_node in node.element_nodes:
			elements.append(result.register(self.visit(element_node,context)))
			if result.should_return() :
				return result 
		return result.success(List(elements).set_context(context).set_position(node.position_start,node.position_end))



	def visit_ReturnNode(self,node,context):

		result = RuntimeResult()
		if node.node_to_return:
			value = result.register(self.visit(node.node_to_return,context))
			
			if result.should_return() :
				return result
		else:
			value = Number.null
		return result.success_return(value)



	def visit_ContinueNode(self,node,context):
		return RuntimeResult().success_continue()


	def visit_BreakNode(self,node,context):
		return RuntimeResult().success_break()
	
