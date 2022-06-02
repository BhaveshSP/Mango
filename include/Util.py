
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

# Used to Keep track of the context. Useful in Generating Error Traceback 
class Context:
	def __init__(self,display_name,parent_context=None,parent_entry_position=None):
		self.display_name = display_name
		self.parent_context = parent_context
		self.parent_entry_position = parent_entry_position
		self.symbol_table = None 
	
# Used to Store the Varible and their values as a Key-Pair format in Dictionary
class SymbolTable:
	
	def __init__(self,parent=None):
		self.symbol_table = {}
		self.parent = parent
	
	def get(self,var_name):
		value = self.symbol_table.get(var_name,None)
		
		if value == None and self.parent :
			value = self.parent.get(var_name)
		return value 

	def set(self,var_name,var_value):
		self.symbol_table[var_name] = var_value
		
	def remove(self,var_name):
		del self.symbol_table[var_name]
		
	def __repr__(self):
		return f"{self.symbol_table}"
