
# Error Handling
# Define a Parent Class for Sub Error Types 
class Error:
	# Initialize the Error Name and Error Message 
	def __init__(self,name,message,position):
		self.name = name 
		self.message = message 
		self.position = position 
	# Print Error in User Defined Format 
	def to_string(self):
		error_output = f"{self.name} : {self.message} \n"
		error_output += f"File {self.position.file_name} : Line No {self.position.line} on Position {self.position.col}"
		return error_output

# Handle Unknown Char 
class IllegalCharError(Error):
	# Call __init__ In parent Errro class to Initialize the 
	# Error with name  IllegalCharError and pass a Message 
	def __init__(self,message,position):
		super().__init__("IllegalCharError",message,position)

class IllegalNumberFormat(Error):
	# Call __init__ In parent Errro class to Initialize the 
	# Error with name  IllegalNumberFormat and pass a Message 
	def __init__(self,message,position):
		super().__init__("IllegalNumberFormat",message,position)

