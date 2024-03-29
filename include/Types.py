import string
# Token Types
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"
TT_STRING = "STRING"
TT_EQ = "EQ"
TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_LPAREN = "L_PAREN"
TT_RPAREN = "R_PAREN"
TT_LSQUARE = "LSQUARE"
TT_RSQUARE = "RSQUARE"
TT_EE = "EE"
TT_NE = "NE"
TT_LT = "LT"
TT_LTE = "LTE"
TT_GT = "GT"
TT_GTE = "GTE"
TT_EOF = "EOF"
TT_POW = "^"
TT_MOD = "MOD"
TT_IF = "IF"
TT_THEN = "THEN"
TT_ARROW = "ARROW"
TT_COMMA = "COMMA"
TT_NEXTLINE = "NEXTLINE"

# Sets 
DIGITS = "1234567890"
LETTERS = string.ascii_letters
LETTERS_DIGITS =LETTERS + DIGITS 
KEYWORDS = ["set","and","or","not" ,"if","then",
            "elseif","else","for","do","step","with",
            "to","while","function","end","return","break","continue"] 
