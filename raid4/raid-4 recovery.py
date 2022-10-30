import os
path = "/**/ /"
#Stelle alle Disks zu Verfügung
disk0 = open(path + "disk0", "rb")
disk1 = open(path + "disk1", "rb")
disk3 = open(path + "disk3", "rb")
#Stelle leere 2te bereit
if os.path.exists("/**/ /disk2"):
    os.remove("/**/ /disk2")
    disk2 = open("/**/ /disk2", "xb")
else:
    disk2 = open("/**/ /disk2", "xb")

print(disk0.decode())
n = 0
for byte in disk0.read():
    if n<1:
        print(byte)
        n = n + 1

#Berechne Disk2
#n = 0
#for b1, b2, b3 in zip(disk0.read(), disk1.read(), disk3.read()):
    #n = n + 1
    #workOnBytes
    #if n<11:
        #print(b1)
    #print(b2)
    #print(b3)
    #cut1stBytesFromDisk1Disk3 orIncreasePointer
    #HowTF do I use a Pointer to access specific parts in the data

#for e in range(len(disk0)):
#    print(disk0[e])

#shuffle blocks
#blockgroesse = int(4096) #Bytes

#save jpg