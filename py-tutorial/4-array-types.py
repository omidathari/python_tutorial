import platform as pf
import pdb
from array import array, ArrayType
import numpy as np

#create array of arrays
all_arrays = np.array([[10, 20, 30, 40, 50],
                       [60, 70, 80, 90, 100],
                       [110, 120, 130, 140, 150]])


x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0

arr_B = array('i',[123,123])
arr_float = array('f',[1.2,2.2,2.3])
arr_float = array('f',[1.2,2.2,2.3])
arr_float = array('f',[1.2,2.2,2.3])

class myclass:
    def __init__(self):
        self.x = 10
        print(hex(id(self.x)))

        self.y = 9
        print(hex(id(self.y)))

        self.z = 9
        print(hex(id(self.z)))

        self.z = 8
        print(hex(id(self.z)))

        print(hex(id(self)))

c = myclass()

# print(all_arrays)
# print(all_arrays.shape)
# print(all_arrays.size)
