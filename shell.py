import mango 

while True :
	command = input("mango> ")
	if command == "exit" or command == "q" or command == "quit":
		break
	tokens, error = mango.run("<stdin>",command)
	if error :
		print(error.to_string())
	else:
		print(tokens)
