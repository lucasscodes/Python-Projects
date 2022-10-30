"""
1/M * SUM(1,M,f(x)) ist der Durchschnittswert der Funktion f(x) über 1 bis M. 
Also ist g_(x,y)=1/M*SUM(1,M,gm(x,y)=AVG(gm(x,y))
=>AVG(gm(x,y))=AVG(f(x,y)+Rauschen(x,y))
Da wir wissen, dass der Erwartungswert des Rauschens 0 ist, kann man dies ausklammern.
AVG(gm(x,y))=AVG(f(x,y))+0
Da f(x) fix ist, ist AVG(f(x,y)=f(x,y)
=> AVG(gm(x,y))=f(x,y)
Also folgt der Erwartungswert von AVG(gm(x,y)) ist f(x,y)
"""
