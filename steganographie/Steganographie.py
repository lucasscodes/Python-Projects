#Python 3.7.4
import os.path as path

bits = "" #speichert alle LeastSignificantBits
headerRest = 54 #speichert Restlänge des Headers
string = "" #Speichert alle interpretierten Buchstaben
byte = "" #Sammelt für jeden Char das Byte an
byteCounter = 0 #Speichert an welcher Stelle des Bytes man ist

#Tastet alle(1024x853) Pixel ab, dabei hat jedes Pixel 3 Bytes(RGB)
#Header davor wird übersprungen (54Byte)
#Speichert resultierenden LSB-Bitstring in "bits"
for bitbyte in open(path.join(path.dirname(__file__),"Stego.bmp"),"rb").read(): #ließt Byteweise das Bild ein
    if headerRest<1: #wenn HeaderBytes übersprungen sind
        bits += str(bitbyte & 1) #Speicher per Bitmaske extrahiertes LSB
    else: #wenn Bytes noch zum Header gehören
        headerRest -= 1 #dekrementiere Zähler
#Interpretiert das Bitmuster zum String
for bit in bits:
    byte += bit #Füge jedes Bit ans akt. Byte
    if byteCounter < 7: #Falls gerade nicht letztes Bit angefügt wurde,
        byteCounter += 1 #notiere folgende Position
    else:
        byteCounter = 0 #sonst setze Zähler zurück
        if 31 < int(byte,2) and int(byte,2) < 127:#solange ASCII-Range, 
            string += chr(int(byte,2)) #speichere Char
        byte = "" #und setze byte-Speicher zurück
print(string[146978:147000]) #gib gesuchten String aus
input()