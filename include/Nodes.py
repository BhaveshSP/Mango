

# Node to Store the Number in AST 
class NumberNode:
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

# Node to Access Value of a Variable in AST 
class VarAccessNode:
	def __init__(self,var_name_token):
		self.var_name_token = var_name_token
		self.position_start = var_name_token.position_start
		self.position_end = var_name_token.position_end 

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