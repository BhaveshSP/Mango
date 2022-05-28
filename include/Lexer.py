from include.Token import *
from include.Error import *
from include.Grammer import * 
from include.util import *

class Lexer:

	 def __init__(self,file_name,text):
	 	self.text = text 
	 	self.position = Position(-1, 1, 0, file_name)
	 	self.size = len(text)
	 	self.current_char = None 
	 	self.advance()

	 def advance(self):
	 	self.position.advance(self.current_char) 
	 	self.current_char = self.text[self.position.index] if self.position.index < self.size else None 
	 def go_back(self):
	 	self.position.go_back()
	 	self.current_char = self.text[self.position.index] if self.position.index >= 0 else None  
	 def tokenize(self):
	 	tokens = [] 
	 	error = None 
	 	while self.current_char != None :
	 		token = None 
	 		if self.current_char in " \t":
	 			pass
	 		elif self.current_char == "+":
	 			token = Token(TT_PLUS)
	 		elif self.current_char == "-":
	 			token = Token(TT_MINUS)
	 		elif self.current_char == "*":
	 			token = Token(TT_MUL)
	 		elif self.current_char == "/":
	 			token = Token(TT_DIV)
	 		elif self.current_char == "(":
	 			token = Token(TT_LPAREN)
	 		elif self.current_char == ")":
	 			token = Token(TT_RPAREN)
	 		elif self.current_char in DIGITS :
	 			number,type_,temp_error = self.get_number()
	 			if temp_error :
	 				error = temp_error
	 				break 
	 			token = Token(type_,number)
	 		else:
	 			error = IllegalCharError("'" + self.current_char + "'", self.position)
	 			tokens = []
	 			break
	 		self.advance()
	 		if token:
	 			tokens.append(token)
	 	return tokens,error  
	 def get_number(self):
	 	number = ""
	 	dot_count = 0 
	 	error = None 
	 	while self.current_char != None and self.current_char in DIGITS + ".":
	 		if self.current_char == ".":
	 			if dot_count: 
	 				error = IllegalNumberFormat("'" + number+"." + "'", self.position)
	 				break 
	 			dot_count += 1
	 		number += self.current_char 
	 		self.advance()
	 	self.go_back()
	 	if dot_count == 0 :
	 		return int(number),TT_INT,error 
	 	else:
	 		return float(number),TT_FLOAT,error 
