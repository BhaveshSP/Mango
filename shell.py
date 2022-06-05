import mango 
import pyfiglet 
print("###################################################################")
print("")
print("Welcome to Mango(Aam) Programming Language ")
print("Feel free to Play Around!!")
print("")
print("###################################################################")
print("")
print("")

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

