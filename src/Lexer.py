from include.Token import *
from include.Error import *
from include.Util import *
from include.Types import * 

# Lexer Tokenizes a Text String or Sentence into Tokens 
class Lexer:

	# Initialize the Values 
	 def __init__(self,file_name,text):
	 	self.text = text 
	 	# Set the position as Position Class to Keep Track of the 
	 	# position for Error Handling   
	 	self.position = Position(-1, 1, 0, file_name,text)
	 	self.size = len(text)
	 	self.current_char = None 
	 	self.advance()

	 # Advances the Current Character to Next Char in the Sentence 
	 def advance(self):
	 	self.position.advance(self.current_char) 
	 	self.current_char = self.text[self.position.index] if self.position.index < self.size else None 
	 # Sets the Current Character to the Previous Char in the Sentence  
	 def go_back(self):
	 	self.position.go_back()
	 	self.current_char = self.text[self.position.index] if self.position.index >= 0 else None  
	 # Tokenize the Sentence into List of Tokens 
	 def tokenize(self):
	 	tokens = [] 
	 	error = None 
	 	# While not the End of the Sentence Loop 
	 	while self.current_char != None :
	 		token = None 
	 		# If Space or Tabs in the Sentence Ignore 
	 		if self.current_char in " \t":
	 			pass
	 		# Create Token for Respective Operation Type 
	 		elif self.current_char == "+":
	 			token = Token(TT_PLUS,self.position)
	 		# Create token is a letter 
	 		# then it is either a keyword or variable name 
	 		elif self.current_char in LETTERS:
	 			token = self.make_identifier()
	 		# Create token for TT_MINUS
	 		elif self.current_char == "-":
	 			token = Token(TT_MINUS,self.position)
	 		# Create token for TT_MUL
	 		elif self.current_char == "*":
	 			token = Token(TT_MUL,self.position)
	 		# Create token for TT_DIVminus
	 		elif self.current_char == "/":
	 			token = Token(TT_DIV,self.position)
	 		# Create token for TT_LPAREN
	 		elif self.current_char == "(":
	 			token = Token(TT_LPAREN,self.position)
	 		# Create token for TT_RPAREN
	 		elif self.current_char == ")":
	 			token = Token(TT_RPAREN,self.position)
	 		# Create token for TT_POW
	 		elif self.current_char == "^":
	 			token = Token(TT_POW,self.position)
	 		# Create token for TT_COMMA
	 		elif self.current_char == ",":
	 			token = Token(TT_COMMA,self.position)
	 		# Create token for Not Equals
	 		elif self.current_char == "!":
	 			token, error = self.make_not_equal()
	 			if error:
	 				tokens = [] 
	 				break
	 		# Create token for Equals or Double Equals 
	 		elif self.current_char == "=":
	 			token = self.make_equals() 
	 		# Create token for Less than or Less Than Equals
	 		elif self.current_char == "<":
	 			token = self.make_less_than() 
	 		# Create token for Greater than or Greater Than Equals
	 		elif self.current_char == ">":
	 			token = self.make_greater_than()

	 		# If Current Char is a Digit 
	 		# Convert to Number and then create Token 
	 		# of Respective Data Type  
	 		elif self.current_char in DIGITS :
	 			token,temp_error = self.get_number()
	 			if temp_error :
	 				error = temp_error
	 				break 
	 		else:
	 			# Unknown Character Found Show IllegalCharError 
	 			# with the Unknown Character with Position 
	 			error = IllegalCharError("'" + self.current_char + "'", self.position,self.position.copy().advance())
	 			tokens = []
	 			break
	 		# Go to Next Character 
	 		self.advance()
	 		# If Token not None Add to the List 
	 		if token:
	 			tokens.append(token)
	 	tokens.append(Token(TT_EOF,self.position))
	 	return tokens,error  

	 # Create token for Not Equals
	 def make_not_equal(self):
	 	position_start = self.position.copy()
	 	self.advance()
	 	if self.current_char == "=":
	 		return Token(TT_NE,position_start,self.position) , None 
	 	else:
	 		self.go_back()
	 	return None , ExpectedCharError("'='",position_start,self.position)
	 
	 # Create token for Equals
	 def make_equals(self):
	 	position_start = self.position.copy()
	 	self.advance()
	 	type_ = TT_EQ
	 	if self.current_char == "=":
	 		type_ = TT_EE 
	 	elif self.current_char == ">":
	 		type_ = TT_ARROW
	 	else:
	 		self.go_back()
	 	return Token(type_,position_start,self.position)

	 # Create token for Less than or Less Than Equals
	 def make_less_than(self):
	 	position_start = self.position.copy()
	 	self.advance()
	 	type_ = TT_LT
	 	if self.current_char == "=":
	 		type_ = TT_LTE
	 	else:
	 		self.go_back()
	 	return Token(type_,position_start,self.position)

	 # Create token for Greater than or Greater Than Equals
	 def make_greater_than(self):
	 	position_start = self.position.copy()
	 	self.advance()
	 	type_ = TT_GT
	 	if self.current_char == "=":
	 		type_ = TT_GTE
	 	else:
	 		self.go_back()
	 	return Token(type_,position_start,self.position)

	 # Create token for identifier
	 def make_identifier(self):
	 	identifier_string = ""
	 	position_start = self.position.copy()
	 	while self.current_char!= None and self.current_char in LETTERS_DIGITS + "_":
	 		identifier_string += self.current_char 
	 		self.advance()
	 	self.go_back()
	 	# If not in keywords its a variable  
	 	type_ = TT_KEYWORD if identifier_string in KEYWORDS else TT_IDENTIFIER
	 	return Token(type_,position_start,self.position,identifier_string)


	 # Extract the Number From the Sentence 
	 def get_number(self):
	 	position_start = self.position.copy()
	 	number = ""
	 	dot_count = 0 
	 	error = None 
	 	# While not End of the Sentence or Current Char is Digit Loop 
	 	while self.current_char != None and self.current_char in DIGITS + ".":
	 		# If Floating Point Found 
	 		if self.current_char == ".":
	 			# If the Dot Count greater than one show 
	 			# IllegalNumberFormat Error and break 
	 			if dot_count: 
	 				error = IllegalNumberFormat("'" + number+"." + "'", self.position,self.position.copy().advance())
	 				break 
	 			# Increament the Dot Count 
	 			dot_count += 1
	 		# Add the Digit to the Number String 
	 		number += self.current_char 
	 		# Go to next Character 
	 		self.advance()
	 	# Go back one Character since last character was not part of a number 
	 	self.go_back()
	 	# If Dot Count Equals to Zero 
	 	# the number is of format Int 
	 	if not dot_count:
	 		return Token(TT_INT,position_start,self.position,int(number)), error 
	 	else:
	 		# Otherwise if the Number is valid 
	 		# its a float 
	 		return Token(TT_FLOAT,position_start,self.position,float(number)), error 
