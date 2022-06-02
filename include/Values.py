from include.Error import * 
from include.Util import * 


# Number Data Structure for representing and performing operations 
# on Integers or Floats

class Value:

	def __init__(self):
		self.set_position()
		self.set_context()

	def set_position(self,position_start=None,position_end=None):
		self.position_start = position_start 
		self.position_end = position_end 
		return self 

	def set_context(self,context=None):
		self.context = context 
		return self

	def added_to(self,other_node):
		return None , self.illegal_operator_error(other_node)

	def subtracted_by(self,other_node):
		return None , self.illegal_operator_error(other_node)

	def multiply_by(self,other_node):
		return None , self.illegal_operator_error(other_node)

	def divide_by(self,other_node):
		return None , self.illegal_operator_error(other_node)


	def moded_by(self,other_node):
		return None , self.illegal_operator_error(other_node)


	def power(self,other_node):

		return None , self.illegal_operator_error(other_node)


	def get_comparsion_equals(self,other_node):

		return None , self.illegal_operator_error(other_node)

	def get_comparsion_not_equals(self,other_node):

		return None , self.illegal_operator_error(other_node)

	def get_comparsion_less_than(self,other_node):

		return None , self.illegal_operator_error(other_node)

	def get_comparsion_less_than_equal(self,other_node):

		return None , self.illegal_operator_error(other_node)

	def get_comparsion_greater_than(self,other_node):

		return None , self.illegal_operator_error(other_node)

	def get_comparsion_greater_than_equal(self,other_node):

		return None , self.illegal_operator_error(other_node)


	def anded_by(self,other_node):

		return None , self.illegal_operator_error(other_node)


	def or_by(self,other_node):

		return None , self.illegal_operator_error(other_node)

	def not_by(self):
		return None , self.illegal_operator_error()

	def is_true(self):
		return False


	def execute(self,args):
		return None , self.illegal_operator_error()



	# Create a Copy or Duplicate of the Number 
	def copy(self):
		raise Exception("No Copy Method Defined")


	def illegal_operator_error(self,other_node=None):
		if not other_node:other_node = self
		return RuntimeError("Illegal Operation ",self.position_start,
				           self.position_end,
				           self.context) 


class Number(Value):	

	def __init__(self,value):
		super().__init__()
		self.value = value 


	def set_position(self,position_start=None,position_end=None):
		self.position_start = position_start 
		self.position_end = position_end 
		return self 

	def set_context(self,context=None):
		self.context = context 
		return self

	# Operations on Number 
	
	def added_to(self,other_node):
		if isinstance(other_node,Number):
			return Number(self.value + other_node.value).set_context(self.context), None
		else:
			return None , Value.illegal_operator_error(other_node)

	def subtracted_by(self,other_node):
		if isinstance(other_node,Number):
			return Number(self.value - other_node.value).set_context(self.context), None
		else:
			return None , Value.illegal_operator_error(other_node)

	def multiply_by(self,other_node):
		if isinstance(other_node,Number):
			return Number(self.value * other_node.value).set_context(self.context), None
		else:
			return None , Value.illegal_operator_error(other_node)
	def divide_by(self,other_node):
		if isinstance(other_node,Number):
			if other_node.value == 0:
				return None , RuntimeError(
				         "ZeroDivisionError : Can't Divide by Zero",
				          self.position_start,
				           self.position_end,
				           self.context
				           )
			return Number(self.value / other_node.value).set_context(self.context), None
		else:
			return None , Value.illegal_operator_error(other_node)


	def moded_by(self,other_node):
		if isinstance(other_node,Number):
			return Number(self.value % other_node.value).set_context(self.context), None 
		else:
			return None , Value.illegal_operator_error(other_node)

	def power(self,other_node):
		if isinstance(other_node,Number):
			return Number(self.value ** other_node.value).set_context(self.context), None 
		else:
			return None , Value.illegal_operator_error(other_node)


	def get_comparsion_equals(self,other_node):
		if isinstance(other_node,Number):
			return Number(int(self.value == other_node.value)).set_context(self.context), None 
		else:
			return None , Value.illegal_operator_error(other_node)


	def get_comparsion_not_equals(self,other_node):
		if isinstance(other_node,Number):
			return Number(int(self.value != other_node.value)).set_context(self.context), None 
		else:
			return None , Value.illegal_operator_error(other_node)


	def get_comparsion_less_than(self,other_node):
		if isinstance(other_node,Number):
			return Number(int(self.value < other_node.value)).set_context(self.context), None 
		else:
			return None , Value.illegal_operator_error(other_node)

	def get_comparsion_less_than_equal(self,other_node):
		if isinstance(other_node,Number):
			return Number(int(self.value <= other_node.value)).set_context(self.context), None 
		else:
			return None , Value.illegal_operator_error(other_node)


	def get_comparsion_greater_than(self,other_node):
		if isinstance(other_node,Number):
			return Number(int(self.value > other_node.value)).set_context(self.context), None 
		else:
			return None , Value.illegal_operator_error(other_node)


	def get_comparsion_greater_than_equal(self,other_node):
		if isinstance(other_node,Number):
			return Number(int(self.value >= other_node.value)).set_context(self.context), None 
		else:
			return None , Value.illegal_operator_error(other_node)

	def anded_by(self,other_node):
		if isinstance(other_node,Number):
			return Number(int(self.value and other_node.value)).set_context(self.context), None 
		else:
			return None , Value.illegal_operator_error(other_node)

	def or_by(self,other_node):
		if isinstance(other_node,Number):
			return Number(int(self.value or other_node.value)).set_context(self.context), None 
		else:
			return None , Value.illegal_operator_error(other_node)


	def not_by(self):
		return Number(1 if self.value==0 else 0).set_context(self.context), None 

	def is_true(self):
		return self.value == 1 

	# Create a Copy or Duplicate of the Number 
	def copy(self):
		duplicate = Number(self.value)
		duplicate.set_position(self.position_start,self.position_end)
		duplicate.set_context(self.context)
		return duplicate

	def __repr__(self):
		return f"{self.value}"


class Function(Value):

	def __init__(self,name,args,body_node):
		super().__init__()
		self.name = name or "<anonymous>"
		self.args = args
		self.body_node = body_node
		self.args_size = len(args)

	def execute(self,passed_args,result,interpreter):

		
		new_context = Context(self.name,self.context,self.position_start)		
		new_context.symbol_table = SymbolTable(new_context.parent_context.symbol_table)



		passed_arg_size = len(passed_args)
		if passed_arg_size > self.args_size:
			return result.failure(RuntimeError(f"Too many arguments passed into {self.name} function \nExcepted {self.args_size} arguments ",self.position_start,
				           self.position_end,
				           self.context))
		if passed_arg_size < self.args_size:
			return result.failure(RuntimeError(f"Too few arguments passed into {self.name} function \nExcepted {self.args_size} arguments ",self.position_start,
				           self.position_end,
				           self.context))
		for i in range(passed_arg_size):
			arg_name = self.args[i]
			arg_value = passed_args[i]
			arg_value.set_context(new_context)
			new_context.symbol_table.set(arg_name,arg_value)
		
		return_value = result.register(interpreter.visit(self.body_node,new_context))
		if result.error :
			return result
		return result.success(return_value)


	def copy(self):
		duplicate = Function(self.name,self.args,self.body_node)
		duplicate.set_context(self.context)
		duplicate.set_position(self.position_start,self.position_end)
		return duplicate

	def __repr__(self):
		return f"function {self.name}"


class String(Value):

	def __init__(self,value):
		super().__init__()
		self.value = value 

	def added_to(self,other_node):
		if isinstance(other_node,String):
			return String(self.value+other_node.value).set_context(self.context).set_position(self.position_start,other_node.position_end), None 
		else:
			return None , Value.illegal_operator_error(other_node)
	
	def multiply_by(self,other_node):
		if isinstance(other_node,Number):
			return String(self.value * other_node.value).set_context(self.context).set_position(self.position_start,self.position_end), None 
		else:
			return None, Value.illegal_operator_error(other_node)

	def is_true(self):
		return len(self.value ) > 0
	
	def copy(self):
		duplicate = String(self.value)
		duplicate.set_context(self.context)
		duplicate.set_position(self.position_start,self.position_end)
		return duplicate

	def __repr__(self):
		return f"{self.value}"


class List(Value):

	def __init__(self,elements,print_in_new_line=False):
		super().__init__()
		self.elements = elements
		self.print_in_new_line = print_in_new_line

	def added_to(self,other_node):
		new_list = self.copy()
		new_list.elements.append(other_node)
		return new_list, None

	def multiply_by(self,other_node):
		if isinstance(other_node,List):
			new_list = self.copy()
			new_list.elements.extend(other_node.elements)
			return new_list,None 
		else:
			return None, Value.illegal_operator_error(other_node)

	def subtracted_by(self,other_node):
		if isinstance(other_node,Number):
			new_list = self.copy()
			try:
				other_node.value -=  1 
				new_list.elements.pop(other_node.value)
				return new_list, None 
			except :
				return None, RuntimeError(f"IndexOutOfBound : Element at index {other_node.value} cannot be removed since it is out of bounds",self.position_start,
				           self.position_end,
				           self.context) 


		else:
			return None, Value.illegal_operator_error(other_node)

	def divide_by(self,other_node):
		if isinstance(other_node,Number):
			other_node.value -=  1 
			try:
				return self.elements[other_node.value], None 
			except :
				return None, RuntimeError(f"IndexOutOfBound  : Element at index {other_node.value} cannot be accessed since it is out of bounds",self.position_start,
				           self.position_end,
				           self.context)
		else:
			return None, Value.illegal_operator_error(other_node)


	def copy(self):
		duplicate = List(self.elements[:])
		duplicate.set_context(self.context)
		duplicate.set_position(self.position_start,self.position_end)
		return duplicate
	def __repr__(self):
		
		if self.print_in_new_line:
			output = "\n".join([str(x) for x in self.elements])
			return output
			
		else:
			return f'[{", ".join([str(x) for x in self.elements])}]'