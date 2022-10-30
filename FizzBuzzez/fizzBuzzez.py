def fizzBuzz(n,ret=[]):
    if(n > 0):
        if(not(n%3) and not(n%5)):
            res = "fizzBuzz"
        elif(not(n%5)):
            res = "buzz"
        elif(not(n%3)):
            res = "fizz"
        else:
            res = str(n)
        fizzBuzz(n-1,ret+[res])
    elif(n == 0): #Da sonst (0%3 && 0%5)=>True gilt!
        ret.reverse() #Da man beim Spiel hochzählt
        return " ".join(ret) #Aus der Liste wird ein String und die enthaltenen Objekte sind durch " " getrennt!
    else:
        print("Input integer größer 0!")
    
def fizzBuzz2(n):
    i = 1
    while i<=n:
        if i%3 == 0 and i%5 == 0:
            print("FizzBuzz",end=" ")
        elif i%5 == 0:
            print("buzz", end=" ")
        elif i%3 == 0:
            print("fizz", end=" ")
        else:
            print(str(i), end=" ")
        i += 1

def fizzBuzzFunc(n):
    if n>1:
        if n%5 == 0 and n%3 == 0:
            return fizzBuzzFunc(n-1)+" FizzBuzz"
        if n%5 == 0:
            return fizzBuzzFunc(n-1)+" buzz"
        if n%3 == 0:
            return fizzBuzzFunc(n-1)+" fizz"
        else:
            return fizzBuzzFunc(n-1)+" "+str(n)
    if n==1:
        return "1"

if fizzBuzz2(15) ==  fizzBuzz(15):
    print("Test1 passed!")
if fizzBuzz(15) ==  fizzBuzzFunc(15):
    print("Test2 passed!")