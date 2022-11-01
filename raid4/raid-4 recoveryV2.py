import binascii
import re
import os

path = os.path.dirname(__file__)

#Calculate disk2 with disk0+1+parity
def getDisk():
    if False: #Enable for Tests
        testString = ""
        for h1,h2,h3 in zip(list0, list1, list3):
            """stats = [0 for i in range(256)]
            for a,b,c in zip(list0, list1, list3):
                stats[a] += 1
                stats[b] += 1
                stats[c] += 1
            print(stats) #all found in slots 48-57 + 97-102"""
            #print(f'Default: {h1},{h2},{h3}')
            #print("Swapped:",swapper[str(h1)],swapper[str(h2)],swapper[str(h3)])
            #input()
            for b1, b2, b3 in zip(swapper[str(h1)], swapper[str(h2)], swapper[str(h3)]):
                testString += str(b3)
                #print(b1,b2,str((b1 + b2 + b3) % 2),"Parität:",b3)
                #print(swapper[str(h1)],swapper[str(h2)],swapper[str(h3)],b1,b2,b3)
        testHex = ""
        testListe = re.findall("....",testString)
        for nibble in testListe:       
            testHex += swapperRev[nibble]
        testBytes = bytes.fromhex(testHex)
        test = open(path + "/disk3test", "wb")
        test.write(testBytes)
        test.close()
        if True: #Want to test a new disk3 against the old one?
            with(open(path + "/disk3", "rb")) as helper:
                disk3 = helper.read()
            with(open(path + "/disk3test", "rb")) as helper:
                disk3t = helper.read()
            for byteA, byteB in zip(disk3, disk3t):
                if (byteA != byteB):
                    print("Error!!!"); input()
            print("Test passed, disks are the same!"); input()
            os.remove(os.path.join(path,"disk3test"))
    
    print("Lese Daten ein...")
    with(open(path + "/disk0", "rb")) as file0:
        list0 = binascii.hexlify(file0.read())
    with(open(path + "/disk1", "rb")) as file1:
        list1 = binascii.hexlify(file1.read())
    with(open(path + "/disk3", "rb")) as file3:
        list3 = binascii.hexlify(file3.read())

    #crazy ints(48-57 + 97-102) to hexnibble, see line12 for cause
    swapper =	{
    "48" : [0,0,0,0],
    "49" : [0,0,0,1],
    "50" : [0,0,1,0],
    "51" : [0,0,1,1],
    "52" : [0,1,0,0],
    "53" : [0,1,0,1],
    "54" : [0,1,1,0],
    "55" : [0,1,1,1],
    "56" : [1,0,0,0],
    "57" : [1,0,0,1],
    "97" : [1,0,1,0],
    "98" : [1,0,1,1],
    "99" : [1,1,0,0],
    "100" : [1,1,0,1],
    "101" : [1,1,1,0],
    "102" : [1,1,1,1]
    }
    #hexnibble to hexchar
    swapperRev = {
        "0000" : "0",
        "0001" : "1",
        "0010" : "2",
        "0011" : "3",
        "0100" : "4",
        "0101" : "5",
        "0110" : "6",
        "0111" : "7",
        "1000" : "8",
        "1001" : "9",
        "1010" : "a",
        "1011" : "b",
        "1100" : "c",
        "1101" : "d",
        "1110" : "e",
        "1111" : "f"
    }

    print("Calc missing bits from disk2 as string...")
    string = "" #to accumulate the calculated bits
    #Write missing bits from disk2(for each 3 hexvalues inside the disks)
    for h1, h2, h3 in zip(list0, list1, list3): 
        #For each bitTriple aaa,bbb,ccc,ddd [a,b,c,d],[a,b,c,d],[a,b,c,d]
        for b1, b2, b3 in zip(swapper[str(h1)], swapper[str(h2)], swapper[str(h3)]):
            #Bitwise: (b1+b2+?)mod2=b3 => (b1+b2+b3)mod2=?
            string += str((b1 + b2 + b3) % 2)

    print("Translate into hexstring...")
    stringHex = ""
    liste = re.findall("....",string) #For each bit-nibble
    for nibble in liste:
        stringHex += swapperRev[nibble]
 
    print("Convert hexstring to bytes...")
    myBytes = bytes.fromhex(stringHex)

    print("Save bytes as missing disk2...")
    file2 = open(path + "/disk2", "wb")
    file2.write(myBytes)
    file2.close()

def extractPic():

    block = 4096 #Blocksize in bytes
    print("Füge Datei aus Disks zusammen...")
    #Load the three disks
    with(open(path + "/disk0", "rb")) as helper:
        disk0 = helper.read()
    with(open(path + "/disk1", "rb")) as helper:
        disk1 = helper.read()
    with(open(path + "/disk2", "rb")) as helper:
        disk2 = helper.read()

    #Initialize 3 vars to accumulate blocks, and one to store the unblocked file
    list1, list2, list3, blocklist = [],[],[],[]
    counter, bytecounter = 0, 0 #pointer inside block and how many bytes got processed
    for byte1, byte2, byte3 in zip(disk0, disk1, disk2):
        bytecounter += 3 #Just for information later on
        #print(byte1,byte2,byte3);input() Seems to create ints 0-255 => 2^8 => bytes
        if counter < block:
            #While blocks arent filled, get more bytes and put em inside
            list1.append(byte1); list2.append(byte2); list3.append(byte3)
            counter += 1 #the blocks store 1 byte more now
        #If there are 3 full blocks, add them to the blocklist
        else: 
            blocklist += list1 + list2 + list3
            #Reset blockpointer and blockvars
            counter, list1, list2, list3 = 0,[],[],[]

    #Are the blocks empty?
    if list1 == [] and list2 == [] and list3 == []:
        print("No bytes remaining!")
    else: #If there are unfilled blocks left, add the remaining
        """#Do I need pading?
        padding = False
        if (padding == True):
            padding = 0
            while counter < block:
                list1.append(0) #Padding with empty bytes
                list2.append(0)
                list3.append(0)
                counter += 1
                padding += 1
            print(f'Padded with {padding}Bytes on each of the last 3 blocks!')"""
        blocklist += list1 + list2 + list3
        #counter, list1, list2, list3 = 0,[],[],[] #useless, last iteration
        print("Disks with blocks merged inside a single file!")

    print("Save the file...")
    pic = open(path + "/picture.jpg", "wb")
    pic.write(bytearray(blocklist))
    pic.close()

    print(f'Done! Saved {bytecounter/(1024*1024):.2f}megaBytes!')


#getDisk() #Tested @1/11/2022(d/m/y), seems to work great
extractPic() #TODO: Error inside this function? Resulting jpg seems to be broken...
             #But the logic seems good inside @1/11/2022(d/m/y)