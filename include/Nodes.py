

# Node to Store the Number in AST 
class NumberNode:
	def __init__(self,token):
		self.token = token 
		self.position_start = token.position_start
		self.position_end = token.position_end
	def __repr__(self):
		return f"{self.token}"


class StringNode:
	def __init__(self,token):
		self.token = token 
		self.position_start = token.position_start
		self.position_end = token.position_end
	def __repr__(self):
		return f"{self.token}"

# Node to Assign a Variable a Value in AST 
class VarAssignNode:
	def __init__(self,var_name_token,var_value_node):
		self.var_name_token = var_name_token.value 
		self.var_value_node = var_value_node
		self.position_start = var_name_token.position_start
		self.position_end = var_value_node.position_end 
	def __repr__(self):
		return f"({self.var_name_token}:{(self.var_value_node)})"

# Node to Access Value of a Variable in AST 
class VarAccessNode:
	def __init__(self,var_name_token):
		self.var_name_token = var_name_token
		self.position_start = var_name_token.position_start
		self.position_end = var_name_token.position_end 
	def __repr__(self):
		return f"{self.var_name_token}"

# Node to Store the Binary Operator with (left operand) operator (right operand) 
# format in AST 
class BinaryOperatorNode:
	def __init__(self,left_node,operator_node,right_node):
		self.operator_node = operator_node 
		self.right_node = right_node 
		self.left_node = left_node 
		self.position_start = left_node.position_start
		self.position_end = right_node.position_end
	def __repr__(self):
		return f"{self.left_node,self.operator_node,self.right_node}"

# Node to Store the Unary Operator with Operator (Operand) format in AST 
class UnaryOperatorNode:
	def __init__(self,operator_node,node):
		self.operator_node = operator_node
		self.node = node 
		self.position_start = operator_node.position_start
		self.position_end = node.position_end
	def __repr__(self):
		return f"{self.operator_node,self.node}"

# Node to Store the If Operator with cases(condition,expression) format in AST 
class IfOperatorNode:
	def __init__(self,cases,else_node):
		self.cases = cases
		self.else_node = else_node 
		self.position_start = cases[0][0].position_start
		self.position_end = cases[-1][1].position_end
		if else_node :
		 self.position_end = else_node.position_end
	def __repr__(self):
		return f"conditions:{self.cases},else:{self.else_node}"


# Node to Store the For Loop Values in AST 
class ForOperatorNode:
	def __init__(self,var_name_token, start_value_node, end_value_node, step_value_node, body_node):
		self.var_name_token = var_name_token
		self.start_value_node = start_value_node
		self.end_value_node = end_value_node
		self.step_value_node = step_value_node
		self.body_node = body_node
		self.position_start = var_name_token.position_start
		self.position_end = body_node.position_end


# Node to Store the While Loop Values is AST 
class WhileOperatorNode:
	def __init__(self,condition_node,body_node):
		self.condition_node = condition_node 
		self.body_node = body_node
		self.position_start = condition_node.position_start
		self.position_end = body_node.position_end



# Node to Store the Function Definition in AST 
class FunctionDefinitionNode:
	def __init__(self,var_name_token,arg_name_tokens,body_node):
		self.var_name_token = var_name_token
		self.arg_name_tokens = arg_name_tokens
		self.body_node = body_node
		self.arg_size = len(arg_name_tokens)
		if var_name_token :
			self.position_start = var_name_token.position_start
		elif self.arg_size > 0 :
			self.position_start = self.arg_name_tokens[0].position_start 
		else:
			self.position_start = body_node.position_start

		self.position_end = body_node.position_end


# Node to Store the Function Call in AST 
class CallNode:

	def __init__(self,node_to_call,arg_nodes):
		self.node_to_call = node_to_call
		self.arg_nodes = arg_nodes
		self.arg_size = len(arg_nodes)
		self.position_start = node_to_call.position_start
		if self.arg_size > 0 :
			self.position_end = arg_nodes[-1].position_end
		else:
			self.position_end = node_to_call.position_end