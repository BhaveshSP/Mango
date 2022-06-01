
# Error Handling
# Define a Parent Class for Sub Error Types 
class Error:
	# Initialize the Error Name and Error Message 
	def __init__(self,name,message,position_start,position_end):
		self.name = name 
		self.message = message 
		self.position_start = position_start
		self.position_end = position_end  
	# Print Error in User Defined Format 
	def to_string(self):
		error_output = f"{self.name} : {self.message} \n"
		error_output += f"File {self.position_start.file_name} : Line No {self.position_start.line} on Position {self.position_start.col}\n"
		return error_output + self.error_with_arrows(self.position_start.text,self.position_start,self.position_end)
	def error_with_arrows(self,text,position_start,position_end):
		lines = text.split("\n") 
		error_line  = lines[position_start.line-1]
		arrow_string = "\n" + error_line + "\n"
		start_index = position_start.col - 3 if position_start.col > 2 else position_start.col 
		arrow_string += " "*(start_index)  
		return arrow_string + "^" +  ("^"*(position_end.col - position_start.col ))

# Handle Unknown Char 
class IllegalCharError(Error):
	# Call __init__ In parent Errro class to Initialize the 
	# Error with name  IllegalCharError and pass a Message 
	def __init__(self,message,position_start,position_end):
		super().__init__("IllegalCharError",message,position_start,position_end)

class IllegalNumberFormat(Error):
	# Call __init__ In parent Errro class to Initialize the 
	# Error with name  IllegalNumberFormat and pass a Message 
	def __init__(self,message,position_start,position_end):
		super().__init__("IllegalNumberFormat",message,position_start,position_end)

class InvalidSyntaxError(Error):
	# Call __init__ In parent Errro class to Initialize the 
	# Error with name  IllegalSyntaxError and pass a Message 
	def __init__(self,message,position_start,position_end):
		super().__init__("InvalidSyntaxError",message,position_start,position_end)

class ExpectedCharError(Error):
	# Call __init__ In parent Errro class to Initialize the 
	# Error with name  ExpectedCharError and pass a Message 
	def __init__(self,message,position_start,position_end):
		super().__init__("ExpectedCharError: Expected a ",message,position_start,position_end)



class RuntimeError(Error):
	# Call __init__ In parent Errro class to Initialize the 
	# Error with name  IllegalSyntaxError and pass a Message 
	def __init__(self,message,position_start,position_end,context):
		super().__init__("Runtime Error ",message,position_start,position_end)
		self.context = context 

	# Overwrites the Parent to_string() method 
	# To Give a Custom Error message with arrows 
	# pointing out to the origin of the error 
	def to_string(self):
		error_output = self.generate_traceback()
		error_output += f"{self.name} : {self.message} \n"
		return error_output + self.error_with_arrows(self.position_start.text,self.position_start,self.position_end)

	# Generates the Traceback to the origin of the error 
	def generate_traceback(self):
		result = ""
		current_pos = self.position_start
		current_context = self.context
		while current_context :
			result += f"File {current_pos.file_name}, Line No {current_pos.line} , in {current_context.display_name}\n"
			current_pos = current_context.parent_entry_position
			current_context = current_context.parent_context 
		return result 

	# Generate a string with arrows below the error location 
	def error_with_arrows(self,text,position_start,position_end):
		lines = text.split("\n") 
		error_line  = lines[position_start.line-1]
		arrow_string = "\n" + error_line + "\n"
		start_index = position_start.col - 3 if position_start.col > 2 else position_start.col 
		arrow_string += " "*(start_index)  
		return arrow_string + "^" +  ("^"*(position_end.col - position_start.col ))
