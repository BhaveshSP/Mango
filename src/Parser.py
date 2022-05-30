from include.Constants import *
from include.Nodes import * 
from include.Error import * 

class ParserResult:
	def __init__(self):
		self.node = None 
		self.error = None 
	def register(self,result):
		if isinstance(result,ParserResult):
			if result.error :
				self.error = result.error 
			return result.node 
		return result 

	def success(self,node):
		self.node = node 
		return self 
	
	def failure(self,error):
		self.error = error 
		return self 



class Parser:

	def __init__(self,tokens):
		self.tokens = tokens 
		self.index = -1 
		self.size = len(tokens)
		self.current_token = None 
		self.advance()

	def parse(self):
		result = self.expression()
		if not result.error and self.current_token.type != TT_EOF:
			return result.failure(InvalidSyntaxError("Expected +,-,* or / ",self.current_token.position_start,self.current_token.position_end))
		return result 
	
	def advance(self):
		self.index += 1 
		if self.index < self.size :
			self.current_token = self.tokens[self.index]
		return self.current_token 

	def factor(self):

		result = ParserResult()
		token = self.current_token 

		if token.type in (TT_PLUS,TT_MINUS):
			result.register(self.advance())
			temp_factor = result.register(self.factor())
			if result.error : return result 
			return result.success(UnaryOperatorNode(token,temp_factor))
		elif token.type == TT_LPAREN:
			result.register(self.advance())
			temp_expr = result.register(self.expression())
			if result.error : return result
			if self.current_token.type == TT_RPAREN:
				result.register(self.advance())
				return result.success(temp_expr)
			else:
				return result.failure(InvalidSyntaxError("Expected ')'",token.position_start,token.position_end))
		elif token.type in (TT_INT,TT_FLOAT):
			result.register(self.advance())
			return result.success(NumberNode(token))
		
		return result.failure(InvalidSyntaxError("Expected Int or Float",token.position_start,token.position_end))

	def binary_operator_helper(self,func,operations):
		result = ParserResult()
		left_node = result.register(func())
		if result.error :
			return result 
		while self.current_token.type in operations:
			bin_op_node = self.current_token 
			result.register(self.advance())
			right_node = result.register(func())
			if result.error :
				return result 
			left_node = BinaryOperatorNode(left_node,bin_op_node,right_node)
		return result.success(left_node)

	def term(self):
		return self.binary_operator_helper(self.factor,(TT_MUL,TT_DIV))

	def expression(self):
		return self.binary_operator_helper(self.term,(TT_PLUS,TT_MINUS))

