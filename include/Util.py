
# Position Class helps to keep track of the current pointer 
# in the sentence for showing error at specific location 
class Position:
	# Initialize the values 
	def __init__(self, index, line, col, file_name,text):
		self.index = index 
		self.line = line 
		self.col = col 
		self.text = text 
		self.file_name = file_name 
	# Set the values for the next character  
	def advance(self,current_char=None):
		# Increment the Character index and Column Index 
		self.index += 1 
		self.col += 1 
		# If the Current Char is a next line character 
		# increment the line index 
		if current_char == "\n":
			self.line+=1 
			self.col = 0
		return self 
	# Go back to the Previous Character 
	def go_back(self):
		self.index -= 1 
		self.col -= 1
		 
	# Create a Copy of the Current Instance of the Position Class 
	# so that it can assigned to multiple variables 
	# and there individual modification doesn't change any other Instance 
	# of the Position class 
	def copy(self):
		return Position(self.index,self.line,self.col,self.file_name,self.text)

