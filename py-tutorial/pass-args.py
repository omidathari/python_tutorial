import sys

print("Number of arguments:", len(sys.argv), "arguments.")
print('Argument List:', str(sys.argv))
print("Arg list size:",sys.argv.__len__())
print("First arg is always the name of the program: ",sys.argv[0])

arg_list = sys.argv

print("Argument list again:",arg_list)

# try the following
# python pass-args.py arg1 arg2 arg3