x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0

x = 5
y = "John"
print(type(x))
print(type(y))

x = "John"
# is the same as
x = 'John'

a = 4
A = "Sally"
#A will not overwrite a

#legal variable names
myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"

#illegal names
# 2myvar = "John"
# my-var = "John"
# my var = "John"

# multiple names
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)

x = y = z = "Orange"
print(x)
print(y)
print(z)

#unpack a list
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x.split('e'))
print(y.split('n'))
print(z)

#Global variables
x = "awesome"

def myfunc():
  print("Python is " + x)

myfunc()