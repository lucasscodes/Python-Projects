import hashlib
import os

#Lädt das Wörterbuch mit beliebten Passwörtern
path = os.path.join(os.path.dirname(__file__),"Top12Thousand-probable-v2.txt")

#Speichert zu knackende Hashes in einer Stringliste, Format: "Name;Salt:Hash"
ziele = ["DonaldChicken;SuperLongSpecialSalt:63e6bd0c8348f7113400ccb5d26df0565dc56c447905ed05fbc80094d5320af0",
"Penny;AlwaysUseADifferentSalt:b998c2aeb78ed8948976a7c8e3317b16ba8a7ad45764520a672c684929f51f90",
"Lulu;WowThisSaltingIsBrilliant:aa24f11386c683e7536e3052ad2928503655497643b1572f9af08e2a605e0141",
"Dagobart;OhNoHeDidnt:7e80081b46537ce6c78846db4acd7e67944df8082131c637d6a4ed4d2215160c",
"Dog;SuchWowSalt:dcdf36dbf3aa9a98b25e8f5814dcede3af2df3ddbc96c869fcb29cb2e0e7de9f"]

for target in ziele:
    #Parse den Zielstring:
    #"a;b:c" => ["a","b:c"] => "a"
    name = target.split(";")[0]
    #"a;b:c" => ["a;b",c"] => "a;b" => ["a","b"] => b
    salt = target.split(":")[0].split(";")[1]
    #"a;b:c" => ["a;b","c"] => "c"
    hash = target.split(":")[1]
    print("Name: "+name)


    #Öffne Wörterbuch neu, da es sonst nur einmal traversiert werden kann
    wörterbuch = open(path)
    #Initialisiere Flag um Fehlschalg zu erkennen
    gefunden = False

    #Teste für jedes Passwort, ob es den selben Hash berechnet
    for passwort in wörterbuch:
        if hash == hashlib.sha3_256(bytes(salt + passwort.split("\n")[0],"utf-8")).hexdigest():
            print("Passwort: " + passwort)
            gefunden = True
            break
    if not gefunden:
        print("Passwort nicht gefunden!")