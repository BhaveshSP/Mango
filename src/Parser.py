from include.Types import *
from include.Nodes import * 
from include.Error import * 



# Result Class to Handle the Value and Error of the Parser 
class ParserResult:
	def __init__(self):
		self.node = None 
		self.error = None 
		self.advance_count = 0 

	def register_advancement(self):
		self.advance_count += 1 

	def register(self,result):
		self.advance_count += result.advance_count
		if result.error :
			self.error = result.error 
		return result.node

	def success(self,node):
		self.node = node 
		return self 
	
	def failure(self,error):
		if not self.error or self.advance_count == 0 :
			self.error = error 
		return self 



# Creates AST of the Token List 
class Parser:

	def __init__(self,tokens):
		self.tokens = tokens 
		self.index = -1 
		self.size = len(tokens)
		self.current_token = None
		self.advance()

	def parse(self):
		# Top Root is a Expression 
		# it is create according to the rules in the Grammer 
		result = self.expression()
		if not result.error and self.current_token.type != TT_EOF:
			return result.failure(InvalidSyntaxError("Expected '+','-','*', '/' or '^'",self.current_token.position_start,self.current_token.position_end))
		return result 
	
	def advance(self):
		self.index += 1 
		if self.index < self.size :
			self.current_token = self.tokens[self.index]
		return self.current_token 

	# Functions Created According to the Grammer Rules 
	def atom(self):
		result = ParserResult()
		token = self.current_token 
		if token.type == TT_LPAREN:
			result.register_advancement()
			self.advance()
			temp_expr = result.register(self.expression())
			if result.error : return result
			if self.current_token.type == TT_RPAREN:
				result.register_advancement()
				self.advance()
				return result.success(temp_expr)
			else:
				return result.failure(InvalidSyntaxError("Expected ')'",token.position_start,token.position_end))
		elif token.type == TT_IDENTIFIER :
			result.register_advancement()
			self.advance()
			return result.success(VarAccessNode(token))
		elif token.type in (TT_INT,TT_FLOAT):
			result.register_advancement()
			self.advance()
			return result.success(NumberNode(token))
		
		return result.failure(InvalidSyntaxError("Expected integer, float, identifier , '+', '-' or '('",token.position_start,token.position_end))

	def power(self):
		return self.binary_operator_helper(self.atom,(TT_POW,),self.factor)


	def factor(self):

		result = ParserResult()
		token = self.current_token 

		if token.type in (TT_PLUS,TT_MINUS):
			result.register_advancement()
			self.advance()
			
			temp_factor = result.register(self.factor())
			if result.error : return result 
			return result.success(UnaryOperatorNode(token,temp_factor))
		
		return self.power()

	def binary_operator_helper(self,func_a,operations,func_b=None):
		result = ParserResult()
		if not func_b:
			func_b = func_a 
		left_node = result.register(func_a())
		if result.error :
			return result 
		while self.current_token.type in operations or (self.current_token.type,self.current_token.value) in operations:
			bin_op_node = self.current_token 
			result.register_advancement()
			self.advance()
			right_node = result.register(func_b())
			if result.error :
				return result 
			left_node = BinaryOperatorNode(left_node,bin_op_node,right_node)
		return result.success(left_node)

	def term(self):
		return self.binary_operator_helper(self.factor,(TT_MUL,TT_DIV))

	def comp_expr(self):
		result = ParserResult()
		if self.current_token.matches(TT_KEYWORD,"not"):
			operator_token = self.current_token 
			result.register_advancement()
			self.advance()
			node = result.register(self.comp_expr())
			if result.error :
				return result
			return result.success(UnaryOperatorNode(operator_token,node))
		node = result.register(self.binary_operator_helper(self.arith_expr,(TT_NE,TT_EE,TT_LT,TT_LTE,TT_GT,TT_GTE)))
		if result.error :
			return result.failure(InvalidSyntaxError("Expected 'let', integer, float, identifier , '+', '-' , '(', or  not ",
				                      self.current_token.position_start,
				                      self.current_token.position_end
				                      ))
		return result.success(node)
	def arith_expr(self):
		return self.binary_operator_helper(self.term,(TT_PLUS,TT_MINUS))

	def expression(self):
		result = ParserResult()
		if self.current_token.matches(TT_KEYWORD,"let"):
			result.register_advancement()
			self.advance()
			
			if self.current_token.type != TT_IDENTIFIER:
				return result.failure(InvalidSyntaxError("Expected identifier",self.current_token.position_start,self.current_token.position_end))
			var_name = self.current_token 
			result.register_advancement()
			self.advance()
			if self.current_token.type != TT_EQ:
				return result.failure(InvalidSyntaxError("Expected '='",
				                      self.current_token.position_start,
				                      self.current_token.position_end
				                      ))
			result.register_advancement()
			self.advance()
			expr = result.register(self.expression())
			
			if result.error :
				return result 
			return result.success(VarAssignNode(var_name,expr))

		node =  result.register(self.binary_operator_helper(self.comp_expr,((TT_KEYWORD,"and"),(TT_KEYWORD,"or"))))
		
		if result.error : 
			return result.failure(InvalidSyntaxError("Expected 'let', integer, float, identifier , '+', '-' , '(', or  not ",
				                      self.current_token.position_start,
				                      self.current_token.position_end
				                      ))

		return result.success(node)


