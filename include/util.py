class Position:
	def __init__(self, index, line, col, file_name):
		self.index = index 
		self.line = line 
		self.col = col 
		self.file_name = file_name 
	def advance(self,current_char):
		self.index += 1 
		self.col += 1 
		if current_char == "\n":
			self.line+=1 
			self.col = 0
		return self 
	def go_back(self):
		self.index -= 1 
		self.col -= 1
		 
	def copy(self):
		return Position(self,self.index,self.line,self.col,self.file_name)