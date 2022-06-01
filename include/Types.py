import string
# Token Types
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"
TT_EQ = "EQ"
TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_LPAREN = "L_PAREN"
TT_RPAREN = "R_PAREN"
TT_EE = "EE"
TT_NE = "NE"
TT_LT = "LT"
TT_LTE = "LTE"
TT_GT = "GT"
TT_GTE = "GTE"
TT_EOF = "EOF"
TT_POW = "^"
TT_IF = "IF"
TT_THEN = "THEN"

# Sets 
DIGITS = "1234567890"
LETTERS = string.ascii_letters
LETTERS_DIGITS =LETTERS + DIGITS 
# Built in Keywords for the Language 
# let - Variable Assignment 
# and - AND operator 
# or - OR operator 
# not - NOT operator 
# Names can be changed to anything 
KEYWORDS = ["let","and","or","not" ,"if","then","elseif","else"] 
