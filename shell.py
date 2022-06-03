import mango 

while True :
	command = input("mango> ")
	if command.strip() == "":
		continue 
	if command == "exit" or command == "q" or command == "quit":
		break
	print("\nProgram Output:")
	output, error = mango.run("<stdin>",command)

	if error :
		print(error.to_string())
	else:		
		print("\nSystem Output:")
		print(repr(output))
		print()

