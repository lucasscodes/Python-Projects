import binascii
import re

path = "/**/ /"
block = 4096

'''
print("Lese Daten ein...")
list0 = ""
list1 = ""
list3 = ""
with(open(path + "disk0", "rb")) as file0:
    list0 = binascii.hexlify(file0.read())
with(open(path + "disk1", "rb")) as file1:
    list1 = binascii.hexlify(file1.read())
with(open(path + "disk3", "rb")) as file3:
    list3 = binascii.hexlify(file3.read())
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

print("Berechne fehlenden Bitstring...")
#Leerer String für Zwischenergebnisse
string = ""
#Schreibe die fehlenden Bits von Disk2 in den String
for h1, h2, h3 in zip(list0, list1, list3):
    #print(swapper[str(b1)])
    for b1, b2, b3 in zip(swapper[str(h1)], swapper[str(h2)], swapper[str(h3)]):
        string = string + str((b1 + b2 + b3) % 2)
        #print(str((b1 + b2 + b3) % 2))

print("Übersetze in Hexstring...")
stringHex = ""
liste = re.findall("....",string)
for nibble in liste:
    stringHex = stringHex + swapperRev[nibble]

print("Konvertiere Hexstring in Bytes...")
myBytes = bytes.fromhex(stringHex)

print("Speichere als fehlende Disk2...")
file2 = open(path + "disk2", "wb")
file2.write(myBytes)
file2.close()
'''

print("Füge Datei aus Disks zusammen...")
#Lade die drei Disks
with(open(path + "disk0", "rb")) as helper:
    disk0 = helper.read()
with(open(path + "disk1", "rb")) as helper:
    disk1 = helper.read()
with(open(path + "disk2", "rb")) as helper:
    disk2 = helper.read()

#Initialisiere Speicher
list1 = []
list2 = []
list3 = []
masterlist = []
counter = 1
mastercounter = 0
for byte1, byte2, byte3 in zip(disk0, disk1, disk2):
    mastercounter = mastercounter + 1
    
    if counter <= block:
        #Solange nicht genug Bytes für Block zusammen, hole noch ein Byte pro Disk
        #Speichere sie in den Blockspeichern list1/2/3
        list1.append(byte1)
        list2.append(byte2)
        list3.append(byte3)
        counter = counter + 1
    #Falls akt. Byte den Block füllt, sende die drei gefüllten Blöcke an den Hauptspeicher
    else:
        masterlist = masterlist + list1 + list2 + list3
        #Setze Blockzaehler und Blockspeicher zurück
        list1 = []
        list2 = []
        list3 = []
        counter = 1

#Falls Reste verbleiben, füge sie hinzu
masterlist = masterlist + list1 + list2 + list3

print("Speichere die Datei ab...")
pic = open(path + "picture.jpg", "wb")
pic.write(bytearray(masterlist))
pic.close()

print("Fertig! Schleife hat " + str(3*mastercounter*4096/1024) + " kiloBytes zusammengefügt!")