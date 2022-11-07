#Again a pyTut

def genericFunction(input1, input2):
    """docstring"""
    # comment
    a = 5
    b = 3
    c = a + b
    return c

def sumOfSquares(a,b):
    # your code here
    return a**2 + b**2

def incrementByOne(a):
    # your code here
    return a+1

def incrementByN(a,n):
    # your code here
    return a+n

def factorial(n):
    if n < 1:
        return False
    if n == 1:
        return n
    return n*factorial(n-1)

def betweenOneAndTen(a):
    # your code here
    return a>1 and a<10

def xGreaterY(x,y):
    # your code here
    return x>y

def xLessThanY(x,y):
    # your code here
    return x<y

def xEqualsY(x,y):
    # your code here
    return x == y

def isPrime(x):
    #dont allow any x<2
    if x < 2:
        return False
    #check that no number in [2,...,x-1] can divide x
    for i in range(2,x):
        #if we got a whole quotient, this cannot be a prime
        if (x/i)-int(x/i) == 0.0:
            return False
    return True

