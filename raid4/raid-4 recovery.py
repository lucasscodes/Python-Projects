import os
path = os.path.dirname(__file__)
#Read all disks
disk0 = open(os.path.join(path,"disk0"), "rb")
disk1 = open(os.path.join(path,"disk1"), "rb")
disk3 = open(os.path.join(path,"disk3"), "rb")
#Create the missing
if os.path.exists(os.path.join(path,"disk2")):
    os.remove(os.path.join(path,"disk2"))
    disk2 = open(os.path.join(path,"disk2"), "xb")
else:
    disk2 = open(os.path.join(path,"disk2"), "xb")
#Try to read from disks
def printAll(len = 0):
    n = 0
    for byte in disk0.read():
        if (len == 0) or (n<len):
            print(byte)
            n += 1
printAll(10)