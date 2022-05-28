
# Data Class for Token  
class Token:
	def __init__(self,type_,value=None):
		self.type = type_ 
		self.value = value
	# Create Token in Form of Type:Value if Value if not None 
	def __repr__(self):
		output = f"{self.type}:{self.value}" if self.value or self.value == 0 else f"{self.type}"
		return output 
