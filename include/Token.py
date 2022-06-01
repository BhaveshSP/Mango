
# Data Class for Token  
class Token:
	def __init__(self,type_,position_start=None,position_end=None,value=None):
		self.type = type_ 
		self.value = value
		if position_start :
			self.position_start = position_start 
			self.position_end = position_start.copy().advance()
		if position_end :
			self.position_end = position_end 
	# Create Token in Form of Type:Value if Value if not None 
	def matches(self,type_,value):
		return self.type == type_ and self.value == value 

	def __repr__(self):
		output = f"{self.type}:{self.value}" if self.value or self.value == 0 else f"{self.type}"
		return output 
