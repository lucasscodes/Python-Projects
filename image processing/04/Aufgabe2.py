import numpy as np
import math

#1 a)
print("Aufgabenteil 1 a)")
start = np.array([-1,-1,1])
#print(start)
#in den Ursprung
mat1 = np.matrix([[1,0,1],
                  [0,1,1],
                  [0,0,1]])
zeroed = mat1.dot(start)
#gespiegelt
mat2 = np.matrix([[-1,0,0],
                  [0,1,0],
                  [0,0,1]])
#mirrored2 = mat2.dot(np.asarray(zeroed).reshape(-1))
#ins Ziel
mat3 = np.matrix([[1,0,1],
                  [0,1,2],
                  [0,0,1]])
#end = mat3.dot(np.asarray(mirrored).reshape(-1))
#print(start,"1")
#print(zeroed, "2")
#print(mirrored, "3")
#print(end, "4")
combined = mat3.dot(mat2.dot(mat1))
print("Verschobene Punkte")
print(combined.dot(np.array([-1,-1,1])))
print(combined.dot(np.array([-2,-1,1])))
print(combined.dot(np.array([-2,-3,1])))
print(combined.dot(np.array([-4,-3,1])))

#1 b)
print("Aufgabenteil 1 b)")
#start2 = np.array([2,0,1])
#print(start2)
#Vergrößern
mat21 = np.matrix([[2,0,0],
                   [0,2,0],
                   [0,0,1]])
#scaled = mat21.dot(start2)
#print(scaled)
#Verzerren
mat22 = np.matrix([[1,0.5,0],
                   [0,1,0],
                   [0,0,1]])
#skewed = mat22.dot(np.asarray(scaled).reshape(-1))
#print(skewed)
#Ins Ziel verschieben
mat23 = np.matrix([[1,0,2],
                   [0,1,0],
                   [0,0,1]])
#shifted = mat23.dot(np.asarray(skewed).reshape(-1))
#print(shifted)
combined2 = mat23.dot(mat22.dot(mat21))
print("Verschobene Punkte")
print(combined2.dot(np.array([0,0,1])))
print(combined2.dot(np.array([2,0,1])))
print(combined2.dot(np.array([2,2,1])))
print(combined2.dot(np.array([0,2,1])))

#1 c)
print("Aufgabenteil 1 c)")
start3 = np.array([2.5,2.5,1])
#print(start3)
#In Ursprung ziehen
mat31 = np.matrix([[1,0,-2.5],
                   [0,1,-1.5],
                   [0,0,1]])
#zeroed2 = mat31.dot(start3)
#print(zeroed2)
#Drehen
mat32 = np.matrix([[np.cos(np.radians(45)),-np.sin(np.radians(45)),0],
                   [np.sin(np.radians(45)),np.cos(np.radians(45)),0],
                   [0,0,1]])
#turned = mat32.dot(np.asarray(zeroed2).reshape(-1))
#print(turned)
#Größe anpassen mit gegebenen Faktor
mat33 = np.matrix([[1/math.sqrt(2),0,0],
                   [0,1/math.sqrt(2),0],
                   [0,0,1]])
#Wieder in Startpos ziehen
mat34 = np.matrix([[1,0,2.5],
                   [0,1,1.5],
                   [0,0,1]])
#target = mat33.dot(np.asarray(turned).reshape(-1))
#print(target)
combined3 = mat34.dot(mat33.dot(mat32.dot(mat31)))
print("Verschobene Punkte")
print(combined3.dot(np.array([2.5,0.5,1])))
print(combined3.dot(np.array([3.5,1.5,1])))
print(combined3.dot(np.array([2.5,2.5,1])))
print(combined3.dot(np.array([1.5,1.5,1])))


#Zerlege Transformationssequenzen
#2 a)
target1 = np.matrix([[.5,0,2],
                     [0,2,3],
                     [0,0,1]])
skalierung = np.matrix([[0.5,0,0],
                        [0,2,0],
                        [0,0,1]])
translation = np.matrix([[1,0,2],
                         [0,1,3],
                         [0,0,1]])
combined4 = translation.dot(skalierung)
combined4 = np.round(combined4, decimals=1)
#Zwei Transformationen, Reihenfolge irrelevant:
#   1. Skalierung mit x*0.5, y*2
#   2. Translation um Vektor (2,3)
print("2 a) erzeugt:")
print(combined4)
print(target1 == combined4)

#2 b)
target2 = np.matrix([[1.414,-1.414,0],
                  [.707,.707,0],
                  [0,0,1]])
drehung = np.matrix([[np.cos(np.radians(45)),-np.sin(np.radians(45)),0],
                     [np.sin(np.radians(45)),np.cos(np.radians(45)),0],
                     [0,0,1]])
skalierung = np.matrix([[2,0,0],
                        [0,1,0],
                        [0,0,1]])
combined5 = skalierung.dot(drehung)
combined5 = np.round(combined5, decimals=3)
#Zwei Reihenfolgeabhängige Transformationen
#   1. Zuerst wird um 45° gegen den Uhzeigersinn gedreht
#   2. Danach wird die x*2 Skaliert
print("2 b) erzeugt:")
print(combined5)
print(target2 == combined5)


#2 c)
target3 = np.matrix([[3,2,5],
                  [0,1,6],
                  [0,0,1]])
translation = np.matrix([[1,0,5],
                         [0,1,6],
                         [0,0,1]])
skalierung = np.matrix([[3,0,0],
                        [0,1,0],
                        [0,0,1]])
scherung = np.matrix([[1,2,0],
                      [0,1,0],
                      [0,0,1]])
combined6 = translation.dot(scherung.dot(skalierung))
combined6 = np.round(combined6)
#Hier sind 3 Reihenfolgeabhängige Transformationen abgelaufen.
#   1. Es wurde skaliert mit x*3
#   2. Danach wurde geschert mit x*2
#   3. Zuletzt wurde eine Translation mit dem Vektor (5,6) durchgeführt
print("2 c) erzeugt:")
print(combined6)
print(target3 == combined6)
