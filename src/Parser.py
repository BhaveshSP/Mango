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

	def register_decreament(self):
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
		# It is create according to the rules in the Grammer 
		result = self.expression()
		if not result.error and self.current_token.type != TT_EOF:
			return result.failure(InvalidSyntaxError("Expected 'set', '+','-','*', '/' or '^'",self.current_token.position_start,self.current_token.position_end))
		return result 
	
	def advance(self):
		self.index += 1 
		if self.index < self.size :
			self.current_token = self.tokens[self.index]
		return self.current_token 
	def go_back(self):
		self.index -= 1 
		if self.index >=0 :
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

		elif token.matches(TT_KEYWORD,"if"):
			if_expr = result.register(self.if_expression())
			if result.error:
				return result

			result.register_advancement()
			self.advance()
			return result.success(if_expr)

		elif token.matches(TT_KEYWORD,"for"):
			for_expr = result.register(self.for_expression())
			if result.error:
				return result

			result.register_advancement()
			self.advance()
			return result.success(for_expr)

		elif token.matches(TT_KEYWORD,"while"):
			while_expr = result.register(self.while_expression())
			if result.error:
				return result

			result.register_advancement()
			self.advance()
			return result.success(while_expr)

		elif token.matches(TT_KEYWORD,"function"):
			func_def = result.register(self.func_def())
			if result.error:
				return result

			result.register_advancement()
			self.advance()
			return result.success(func_def)

		elif token.type == TT_LSQUARE:
			list_expr = result.register(self.list_expr())
			if result.error:
				return result
			result.register_advancement()
			self.advance()
			return result.success(list_expr)


		elif token.type == TT_IDENTIFIER :
			result.register_advancement()
			self.advance()
			return result.success(VarAccessNode(token))

		elif token.type in (TT_INT,TT_FLOAT):
			result.register_advancement()
			self.advance()
			return result.success(NumberNode(token))


		elif token.type == TT_STRING:

			result.register_advancement()
			self.advance()
			return result.success(StringNode(token))
			
		
		return result.failure(InvalidSyntaxError("Expected integer, float, identifier , '+', '-' , '(', if , for, while or function",token.position_start,token.position_end))

	def list_expr(self):
		result = ParserResult()
		element_nodes = [] 
		position_start = self.current_token.position_start.copy()

		result.register_advancement()
		self.advance()

		if self.current_token.type == TT_RSQUARE:
			result.register_advancement()
			self.advance()
		else:
			temp_expr = result.register(self.expression())
			if result.error:
				return result.failure(InvalidSyntaxError("Expected ']', integer, float, identifier , '[', '+', '-' ",
				                      self.current_token.position_start,
				                      self.current_token.position_end
				                      ))

			element_nodes.append(temp_expr)

			while self.current_token != None and self.current_token.type == TT_COMMA :
				result.register_advancement()
				self.advance()
				temp_expr = result.register(self.expression())
				if result.error:
					return result 
				element_nodes.append(temp_expr)


			if self.current_token.type != TT_RSQUARE:
				
				return result.failure(InvalidSyntaxError("Expected ',' or ']'",
				                      self.current_token.position_start,
				                      self.current_token.position_end
				                      ))
		return result.success(ListNode(element_nodes,position_start,self.current_token.position_end.copy()))







	def func_def(self):
		result = ParserResult()
		var_name_token = None 
		args_names_tokens = []
		node_to_return = None 

		result.register_advancement()
		self.advance()

		if self.current_token.type == TT_IDENTIFIER:
			var_name_token = self.current_token 
			result.register_advancement()
			self.advance()
		if self.current_token.type != TT_LPAREN:
			if var_name_token :
				return result.failure(InvalidSyntaxError("Expected '('",self.current_token.position_start,self.current_token.position_end))
			else:
				return result.failure(InvalidSyntaxError("Expected identifier or '('",self.current_token.position_start,self.current_token.position_end))

		result.register_advancement()
		self.advance()

		if self.current_token.type == TT_IDENTIFIER:
			
			args_names_tokens.append(self.current_token)
			result.register_advancement()
			self.advance()

			while self.current_token.type == TT_COMMA:
				result.register_advancement()
				self.advance()
				if self.current_token.type != TT_IDENTIFIER:
					return result.failure(InvalidSyntaxError("Expected identifier",self.current_token.position_start,self.current_token.position_end))
				args_names_tokens.append(self.current_token)
				result.register_advancement()
				self.advance()
		if self.current_token.type != TT_RPAREN:
			if len(args_names_tokens) > 0:
				return result.failure(InvalidSyntaxError("Expected ',' or ')'",self.current_token.position_start,self.current_token.position_end))
			else:
				result.failure(InvalidSyntaxError("Expected identifier or ')'",self.current_token.position_start,self.current_token.position_end))

		result.register_advancement()
		self.advance()


		if self.current_token.type != TT_ARROW:
			return result.failure(InvalidSyntaxError("Expected '=>'",self.current_token.position_start,self.current_token.position_end))

		result.register_advancement()
		self.advance()


		node_to_return = result.register(self.expression())
		if result.error :
			return result 
		return result.success(FunctionDefinitionNode(var_name_token,args_names_tokens,node_to_return))




	def for_expression(self):

		result = ParserResult()
		start_value_node = None 
		var_name = None 
		end_value_node = None 
		step_value_node = None 
		body_value_node = None 
		
		result.register_advancement()
		self.advance()
		
		if self.current_token.type == TT_IDENTIFIER:
			var_name = self.current_token
		else:
			return result.failure(InvalidSyntaxError("Expected a loop variable after for statement",
			                      self.current_token.position_start,
			                      self.current_token.position_end
			                      ))

		result.register_advancement()
		self.advance()

		if self.current_token.type != TT_EQ:
			return result.failure(InvalidSyntaxError("Expected '='",
				                      self.current_token.position_start,
				                      self.current_token.position_end
				                      ))

		result.register_advancement()
		self.advance()

		start_value_node = result.register(self.expression())
		if result.error :
			return result 

		if not self.current_token.matches(TT_KEYWORD,"to"):
			return result.failure(InvalidSyntaxError("Expected 'to' keyword",
				                      self.current_token.position_start,
				                      self.current_token.position_end
				                      ))

		result.register_advancement()
		self.advance()

		end_value_node = result.register(self.expression())

		if self.current_token.matches(TT_KEYWORD,"with"):

			result.register_advancement()
			self.advance()

			if not self.current_token.matches(TT_KEYWORD,"step"):
				return result.failure(InvalidSyntaxError("Expected 'step' keyword after with ",
				                      self.current_token.position_start,
				                      self.current_token.position_end
				                      ))

			result.register_advancement()
			self.advance()


			if not self.current_token.type == TT_EQ:
				return result.failure(InvalidSyntaxError("Expected '='  ",
				                      self.current_token.position_start,
				                      self.current_token.position_end
				                      ))

			result.register_advancement()
			self.advance()


			step_value_node = result.register(self.expression())
			if result.error :
				return result

		if not self.current_token.matches(TT_KEYWORD,"do"):
			return result.failure(InvalidSyntaxError("Expected 'do' keyword ",
				                      self.current_token.position_start,
				                      self.current_token.position_end
				                      ))

		result.register_advancement()
		self.advance()

		body_value_node = result.register(self.expression())
		if result.error :
			return result 

		return result.success(ForOperatorNode(var_name,start_value_node,end_value_node,step_value_node,body_value_node))

	def while_expression(self):

		result = ParserResult()

		condition = None 
		body_value_node = None 

		result.register_advancement()
		self.advance()

		condition = result.register(self.expression())

		if result.error :
			return result 

		
		if not self.current_token.matches(TT_KEYWORD,"do"):
			return result.failure(InvalidSyntaxError("Expected 'do' keyword ",
				                      self.current_token.position_start,
				                      self.current_token.position_end
				                      ))

		result.register_advancement()
		self.advance()

		body_value_node = result.register(self.expression())
		if result.error :
			return result 
		return result.success(WhileOperatorNode(condition,body_value_node))




	def if_expression(self):
		result = ParserResult()
		cases = []
		else_node = None 
		result.register_advancement()
		self.advance()
		condition = result.register(self.expression())
		if result.error:
			return result.failure(InvalidSyntaxError("Expected a <condition> after an if statement",
			                      self.current_token.position_start,
			                      self.current_token.position_end
			                      ))

		if not self.current_token.matches(TT_KEYWORD,"then"):
			return result.failure(InvalidSyntaxError("Expected 'then' after <condition>",
			                      self.current_token.position_start,
			                      self.current_token.position_end
			                      ))
		result.register_advancement()
		self.advance()
		temp_expr = result.register(self.expression())
		if result.error :
			return result 
		cases.append((condition,temp_expr))
		while self.current_token.matches(TT_KEYWORD,"elseif"):
			result.register_advancement()
			self.advance()
			condition = result.register(self.expression())
			if result.error:
				return result.failure(InvalidSyntaxError("Expected a <condition> after an if or elseif statement",
				                      self.current_token.position_start,
				                      self.current_token.position_end
				                      ))
			if not self.current_token.matches(TT_KEYWORD,"then"):
				return result.failure(InvalidSyntaxError("Expected 'then' after <condition>",
				                      self.current_token.position_start,
				                      self.current_token.position_end
				                      ))
			result.register_advancement()
			self.advance()
			temp_expr = result.register(self.expression())
			if result.error :
				return result 
			cases.append((condition,temp_expr)) 
		if self.current_token.matches(TT_KEYWORD,"else"):
			result.register_advancement()
			self.advance()
			else_node = result.register(self.expression())
			if result.error :
				return result 
		else:
			result.register_decreament()
			self.go_back()

		return result.success(IfOperatorNode(cases,else_node))

	def power(self):
		return self.binary_operator_helper(self.call,(TT_POW,),self.factor)

	def call(self):
		result = ParserResult()
		atom = result.register(self.atom())
		if result.error :
			return result 
		if self.current_token.type == TT_LPAREN:
			args_nodes = []
			result.register_advancement()
			self.advance()
			if self.current_token.type == TT_RPAREN:
				result.register_advancement()
				self.advance()
			else:
				temp_expr = result.register(self.expression())
				if result.error:
					return result.failure(InvalidSyntaxError("Expected ')', integer, float, identifier , if , for, while , function, '+', '-' , '(', '[' ,or  not ",
					                      self.current_token.position_start,
					                      self.current_token.position_end
					                      ))
				
				args_nodes.append(temp_expr)
				while self.current_token != None and self.current_token.type == TT_COMMA :
					result.register_advancement()
					self.advance()
					temp_expr = result.register(self.expression())
					if result.error:
						return result 
					args_nodes.append(temp_expr)


				if self.current_token.type != TT_RPAREN:
					
					return result.failure(InvalidSyntaxError("Expected ',' or ')'",
					                      self.current_token.position_start,
					                      self.current_token.position_end
					                      ))
				result.register_advancement()
				self.advance()

			return result.success(CallNode(atom,args_nodes))
		return result.success(atom)


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
		return self.binary_operator_helper(self.factor,(TT_MUL,TT_DIV,TT_MOD))

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
			return result.failure(InvalidSyntaxError("Expected 'set', integer, float, identifier , if , for, while , function, '+', '-' , '(', '[' ,or  not ",
				                      self.current_token.position_start,
				                      self.current_token.position_end
				                      ))
		return result.success(node)
	def arith_expr(self):
		return self.binary_operator_helper(self.term,(TT_PLUS,TT_MINUS))

	def expression(self):
		result = ParserResult()

		if self.current_token.matches(TT_KEYWORD,"set"):
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
			return result.failure(InvalidSyntaxError("Expected 'set', integer, float, identifier , if , for, while , function, '+', '-' , '(', '[' ,or  not ",
				                      self.current_token.position_start,
				                      self.current_token.position_end
				                      ))

		return result.success(node)


