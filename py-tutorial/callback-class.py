
class A:
    def __init__(self,callback_func):
        self.cb = callback_func

    def work(self):
        self.cb()

def my_function():
    print("A value")

a = A(my_function)
a.work()


