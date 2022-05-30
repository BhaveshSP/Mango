class NumberNode:
	def __init__(self,token):
		self.token = token 
	def __repr__(self):
		return f"{self.token}"
class BinaryOperatorNode:
	def __init__(self,left_node,operator_node,right_node):
		self.operator_node = operator_node 
		self.right_node = right_node 
		self.left_node = left_node 
	def __repr__(self):
		return f"{self.left_node,self.operator_node,self.right_node}"

class UnaryOperatorNode:
	def __init__(self,operator_node,right_node):
		self.operator_node = operator_node
		self.right_node = right_node 
	def __repr__(self):
		return f"{self.operator_node,self.right_node}"