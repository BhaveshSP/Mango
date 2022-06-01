import mango 

while True :
	command = input("mango> ")
	if command == "exit" or command == "q" or command == "quit":
		break
	output, error = mango.run("<stdin>",command)
	if error :
		print(error.to_string())
	else:		
		print("Output:")
		print(output)
		print()
