from include.Error import * 
from include.Util import * 
import mango  
import os 
import sys 
import math 


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
		elif isinstance(other_node,String):
			return String(self.value * other_node.value).set_context(self.context).set_position(self.position_start,self.position_end), None 
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

Number.null = Number(0)
Number.true = Number(1)
Number.false = Number(0)
Number.MAX_INT = Number(sys.maxsize)
Number.MIN_INT = Number(-sys.maxsize-1)
Number.MATH_PI = Number(math.pi)



class BaseFunction(Value):

	def __init__(self,name):
		super().__init__()
		self.name = name or "<anonymous>"

	def generate_context(self):

		new_context = Context(self.name,self.context,self.position_start)		
		new_context.symbol_table = SymbolTable(new_context.parent_context.symbol_table)

		return new_context 

	def check_args(self,result,arg_names,agrs):
		passed_arg_size = len(agrs)
		args_size = len(arg_names)

		if passed_arg_size > args_size:
			return result.failure(RuntimeError(f"Too many arguments passed into {self.name} function \nExcepted {args_size} arguments ",self.position_start,
				           self.position_end,
				           self.context))
		
		if passed_arg_size < args_size:
			return result.failure(RuntimeError(f"Too few arguments passed into {self.name} function \nExcepted {args_size} arguments ",self.position_start,
				           self.position_end,
				           self.context))
		return result.success(None)

	def populate_args(self,result,arg_names,args,execution_context):
		passed_arg_size = len(args)
		for i in range(passed_arg_size):
			arg_name = arg_names[i]
			arg_value = args[i]
			arg_value.set_context(execution_context)
			execution_context.symbol_table.set(arg_name,arg_value)
		return result.success(None)

	def check_and_populate_args(self,result,arg_names,args,execution_context):

		result.register(self.check_args(result,arg_names,args))
		if result.error :
			return result 

		self.populate_args(result,arg_names,args,execution_context)
		return result.success(None)




class Function(BaseFunction):

	def __init__(self,name,arg_names,body_node,should_auto_return):
		super().__init__(name)
		self.arg_names = arg_names
		self.body_node = body_node
		self.args_size = len(arg_names)
		self.should_auto_return = should_auto_return



	def execute(self,passed_args,result,interpreter):
		
		execution_context = self.generate_context()
		result.register(self.check_and_populate_args(result,self.arg_names,passed_args,execution_context))
		
		if result.should_return() :
			return result 

		return_value = result.register(interpreter.visit(self.body_node,execution_context))
		if result.should_return() and result.function_return_value == None :
			return result
		return_value = (value if self.should_auto_return else None ) or result.function_return_value or Number.null
		
		return result.success(return_value)


	def copy(self):
		duplicate = Function(self.name,self.arg_names,self.body_node,self.should_auto_return)
		duplicate.set_context(self.context)
		duplicate.set_position(self.position_start,self.position_end)
		return duplicate

	def __repr__(self):
		return f"<function {self.name}>"

class BuiltInFunction(BaseFunction):

	def __init__(self,name):
		super().__init__(name)

	def execute(self,passed_args,result,interpreter):
		execution_context = self.generate_context()
		method_name = f"execute_{self.name}"
		method = getattr(self,method_name,self.no_execution_method)

		result.register(self.check_and_populate_args(result,method.arg_names,passed_args,execution_context))
		if result.error :
			return result 

		result_value = result.register(method(result,execution_context))
		if result.error :
			return result 

		return result.success(result_value)

	def no_execution_method(self,result,context):
		raise Exception(f"No execute_{self.name} method defined")


	def copy(self):
		duplicate = BuiltInFunction(self.name)
		duplicate.set_context(self.context)
		duplicate.set_position(self.position_start,self.position_end)
		return duplicate


	def execute_print(self,result,context):
		print(str(context.symbol_table.get("value")))
		return result.success(Number.null)

	execute_print.arg_names = ["value"]


	def execute_return(self,result,context):
		return result.success(String(str(context.symbol_table.get("value"))))
	execute_return.arg_names = ["value"]


	def execute_clear(self,result,context):
		os.system("cls" if os.name == "nt" else "clear")
		return result.success(Number.null)
	execute_clear.arg_names = []


	def execute_input(self,result,context):
		text = input("Input:\n")
		return result.success(String(text))
	execute_input.arg_names = []


	
	def execute_input_number(self,result,context):
		while True :
			text = input("Input Number:\n")
			try :
				number = int(text)
				break
			except ValueError:
				print(f"'{text}' must be a Number. Try again :)!")
		return result.success(Number(number))
	execute_input_number.arg_names = []



	def execute_is_number(self,result,context):
		is_number = isinstance(context.symbol_table.get("value"),Number)
		return result.success(Number.true if is_number else Number.false)
	execute_is_number.arg_names = ["value"]


	def execute_is_string(self,result,context):
		is_number = isinstance(context.symbol_table.get("value"),String)
		return result.success(Number.true if is_number else Number.false)
	execute_is_string.arg_names = ["value"]


	def execute_is_list(self,result,context):
		is_number = isinstance(context.symbol_table.get("value"),List)
		return result.success(Number.true if is_number else Number.false)
	execute_is_list.arg_names = ["value"]

	def execute_is_function(self,result,context):
		is_number = isinstance(context.symbol_table.get("value"),BaseFunction)
		return result.success(Number.true if is_number else Number.false)
	execute_is_function.arg_names = ["value"]

	def execute_insert(self,result,context):
		l = context.symbol_table.get("list")	
		value = context.symbol_table.get("value")
		if not isinstance(l,List):
			return result.failure(RuntimeError(f"For method Insert(List,Any) first argument must be a List",self.position_start,
				           self.position_end,
				           self.context))
		l.elements.append(value)
		return result.success(Number.null)
	execute_insert.arg_names = ["list","value"]

	def execute_pop(self,result,context):
		l = context.symbol_table.get("list")	
		value = context.symbol_table.get("value")
		if not isinstance(l,List):
			return result.failure(RuntimeError(f"For method Pop(List,IndexOfElement) first argument must be a List",self.position_start,
				           self.position_end,
				           self.context))
		if not isinstance(value,Number):
			return result.failure(RuntimeError(f"For method Pop(List,IndexOfElement) second argument must be a Number",self.position_start,
				           self.position_end,
				           self.context))

		try:
			element = l.elements.pop(value.value-1)
		except :
			return result.failure(RuntimeError(f"IndexOutOfBound : Element at index {value.value} cannot be removed since it is out of bounds ",self.position_start,
				           self.position_end,
				           self.context))

		return result.success(element)


	execute_pop.arg_names = ["list","value"]

	def execute_extend(self,result,context):
		list_a = context.symbol_table.get("listA")	
		list_b = context.symbol_table.get("listB")
		if not isinstance(list_a,List):
			return result.failure(RuntimeError(f"For method Extend(List,List) first argument must be a List",self.position_start,
				           self.position_end,
				           self.context))

		if not isinstance(list_b,List):
			return result.failure(RuntimeError(f"For method Extend(List,List) second argument must be a List",self.position_start,
				           self.position_end,
				           self.context))
		list_a.elements.extend(list_b.elements)
		return result.success(Number.null)

	execute_extend.arg_names = ["listA","listB"]


	def execute_length(self,result,context):
		value = context.symbol_table.get("value")
		if isinstance(value,String) :
			return result.success(Number(len(value.value)))
		elif isinstance(value,List):
			return result.success(Number(len(value.elements)))
		else:
			return result.failure(self.illegal_operator_error())
	execute_length.arg_names = ["value"]


	def execute_run(self,result,context):

		file_name = context.symbol_table.get("file_name")
		if not isinstance(file_name,String):
			return result.failure(RuntimeError(f"File Name Must be a String for method Run(filename)",self.position_start,
				           self.position_end,
				           self.context))
		file_name = file_name.value 
		try:
			with open(file_name,"r") as f:
				script = f.read()
		except Exception as e:
			return result.failure(RuntimeError(f"Failed to load Script\n",self.position_start,
				           self.position_end,
				           self.context))
		output, error = mango.run(file_name,script)
		if error :
			print(error.to_string())
			return result.failure(RuntimeError(f"Failed to finish executing the script {file_name} \n",self.position_start,
				           self.position_end,
				           self.context))
		return result.success(Number.null)


	execute_run.arg_names = ["file_name"]
	
	def __repr__(self):
		return f"<built-function {self.name}>"


BuiltInFunction.print = BuiltInFunction("print")
BuiltInFunction.return_ = BuiltInFunction("return")
BuiltInFunction.clear = BuiltInFunction("clear")
BuiltInFunction.input_ = BuiltInFunction("input")
BuiltInFunction.input_number = BuiltInFunction("input_number")
BuiltInFunction.is_number = BuiltInFunction("is_number")
BuiltInFunction.is_string = BuiltInFunction("is_string")
BuiltInFunction.is_list = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.insert = BuiltInFunction("insert")
BuiltInFunction.pop = BuiltInFunction("pop")
BuiltInFunction.extend = BuiltInFunction("extend")
BuiltInFunction.length = BuiltInFunction("length")
BuiltInFunction.run = BuiltInFunction("run")


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
		return f'"{self.value}"'

	def __str__(self):
		return f"{self.value}"


class List(Value):

	def __init__(self,elements,print_in_new_line=False):
		super().__init__()
		self.elements = elements
		self.print_in_new_line = print_in_new_line

	def added_to(self,other_node):
		new_list = self.copy() 
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
			value = other_node.value -  1 
			try:
				return self.elements[value], None 
			except :
				return None, RuntimeError(f"IndexOutOfBound  : Element at index {value} cannot be accessed since it is out of bounds",self.position_start,
				           self.position_end,
				           self.context)
		else:
			return None, Value.illegal_operator_error(other_node)


	def copy(self):
		duplicate = List(self.elements)
		duplicate.set_context(self.context)
		duplicate.set_position(self.position_start,self.position_end)
		return duplicate
	def __repr__(self):
		
		if self.print_in_new_line:
			output = "\n".join([str(x) for x in self.elements])
			return output
			
		else:
			return f'[{", ".join([str(x) for x in self.elements])}]'

	def __str__(self):
		return f'{", ".join([str(x) for x in self.elements])}'
