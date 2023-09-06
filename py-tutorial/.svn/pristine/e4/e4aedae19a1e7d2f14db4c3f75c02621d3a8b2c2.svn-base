def callbackFunc(s):
    print('Length of the text file is : ', s)

def printFileLength(path, callback):
    f = open(path, "r")
    length = len(f.read())
    f.close()
    callback(length)

if __name__ == '__main__':
    printFileLength("sample.txt", callbackFunc)