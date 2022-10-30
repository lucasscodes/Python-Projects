"""
#1
1200rpm / 60sec/min = 20Hz
=> Abtastrate größer als 2x20Hz
Err: 30fps are not greater 40fps

#2
Man würde alle Formen erkennen, aber die Rotationsgeschwindigkeit wäre abgewandelt, durch die Unterabtastung.

#3
a)      b)      c)      d)
   R       s       R       s
   R       s       R       s
   R       s       R       s
sssssss sssssss sssssss sssssss
   s       R       s       R
   s       R       s       R
   s       R       s       R
Da wir eine Frequenz sin(2*30 Pi x) mit |sin(20 Pi x)|=0 abtasten, kriegen wir pro Frame 1.5 Umdrehungen.
Also sieht man einen still stehenden Propeller und es gibt keine Richtung 

#4
Der Prop. rotiert mit 20Hz, also würden selbst (2*20=)40Fps nicht ausreichen.
"""