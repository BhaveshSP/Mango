from include.Token import *
from include.Error import *
from include.Util import *
from include.Constants import * 

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
	 		elif self.current_char == "-":
	 			token = Token(TT_MINUS,self.position)
	 		elif self.current_char == "*":
	 			token = Token(TT_MUL,self.position)
	 		elif self.current_char == "/":
	 			token = Token(TT_DIV,self.position)
	 		elif self.current_char == "(":
	 			token = Token(TT_LPAREN,self.position)
	 		elif self.current_char == ")":
	 			token = Token(TT_RPAREN,self.position)
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
	 	print("")
	 	return tokens,error  

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
