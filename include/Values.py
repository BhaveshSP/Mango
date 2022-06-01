from include.Error import * 

# Number Data Structure for representing and performing operations 
# on Integers or Floats
class Number:	
	def __init__(self,value):
		self.value = value 
		self.set_position()
		self.set_context()

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

	def subtracted_by(self,other_node):
		if isinstance(other_node,Number):
			return Number(self.value - other_node.value).set_context(self.context), None

	def multiply_by(self,other_node):
		if isinstance(other_node,Number):
			return Number(self.value * other_node.value).set_context(self.context), None
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

	def power(self,other_node):
		if isinstance(other_node,Number):
			return Number(self.value ** other_node.value).set_context(self.context), None 


	def get_comparsion_equals(self,other_node):
		if isinstance(other_node,Number):
			return Number(int(self.value == other_node.value)).set_context(self.context), None 


	def get_comparsion_not_equals(self,other_node):
		if isinstance(other_node,Number):
			return Number(int(self.value != other_node.value)).set_context(self.context), None 


	def get_comparsion_less_than(self,other_node):
		if isinstance(other_node,Number):
			return Number(int(self.value < other_node.value)).set_context(self.context), None 

	def get_comparsion_less_than_equal(self,other_node):
		if isinstance(other_node,Number):
			return Number(int(self.value <= other_node.value)).set_context(self.context), None 


	def get_comparsion_greater_than(self,other_node):
		if isinstance(other_node,Number):
			return Number(int(self.value > other_node.value)).set_context(self.context), None 


	def get_comparsion_greater_than_equal(self,other_node):
		if isinstance(other_node,Number):
			return Number(int(self.value >= other_node.value)).set_context(self.context), None 

	def anded_by(self,other_node):
		if isinstance(other_node,Number):
			return Number(int(self.value and other_node.value)).set_context(self.context), None 

	def or_by(self,other_node):
		if isinstance(other_node,Number):
			return Number(int(self.value or other_node.value)).set_context(self.context), None 


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
