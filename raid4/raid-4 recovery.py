import os
path = os.path.dirname(__file__)
#Stelle alle Disks zu Verfügung
disk0 = open(os.path.join(path,"disk0"), "rb")
disk1 = open(os.path.join(paths,"disk1"), "rb")
disk3 = open(os.path.join(path,"disk3"), "rb")
#Stelle leere 2te bereit
if os.path.exists(os.path.join(path,"disk2")):
    os.remove(os.path.join(path,"disk2"))
    disk2 = open(os.path.join(path,"disk2"), "xb")
else:
    disk2 = open(os.path.join(path,"disk2"), "xb")

def printAll(len = 0):
    n = 0
    for byte in disk0.read():
        if (len == 0) or (n<len):
            print(byte)
            n = n + 1
printAll(10)

#In V2
#Berechne Disk2
#n = 0
#for b1, b2, b3 in zip(disk0.read(), disk1.read(), disk3.read()):
#    n = n + 1
#    workOnBytes
#    if n<11:
#        print(b1)
#    print(b2)
#    print(b3)
#    #cut1stBytesFromDisk1Disk3 orIncreasePointer
#    #HowTF do I use a Pointer to access specific parts in the data
#
#for e in range(len(disk0)):
#    print(disk0[e])

#shuffle blocks
#blockgroesse = int(4096) #Bytes

#save jpg