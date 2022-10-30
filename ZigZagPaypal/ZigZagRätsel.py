import math

class ZigZag:    
    def __init__(self, text: str, height: int):
        self.text = text
        self.length = len(text)
        if height < 1: #Catch to small inputs
            self.height = 1
        else :
            self.height = height
        self.width = self.getWidth()
        self.list = self.createList() #Create multidimList
        self.fillList() #Set the List
        self.string = self.walkList() #Extract the String
        
    def getWidth(self) -> int:
        flag = 0 #downwards==0 upDiagonal==1
        width = 0 #counter
        if self.height == 1: #edgeCase
            return self.length
        elif self.height == 2: #edgeCase
            return math.ceil(self.length/2)
        else: #defaultCase
            length = self.length
            while length>0:
                if flag == 0:
                    width += 1
                    length - self.height
                    flag = 1
                else:
                    width += self.height-2
                    length -= self.height-2
                    flag = 0
        return width    
    
    def createList(self) -> list:
        res = []
        width = self.width
        while width > 0: #while Collumns are missing
            column = [] #create the column
            height = self.height
            while height > 0: #fill the collumn
                column.append(None)
                height -= 1
            res.append(column)
            width -= 1       
        return res
    
    def fillList(self):
        x, y = 0, 0
        flag = 1 #downwards==1, upDiagonal==0
        char = 0 #Stringpointer
        while char < len(self.text): #While Chars are left
            #Move
            if flag == 1: #GoDown
                self.list[x][y] = self.text[char]
                y += 1
            else: #Go Up+Right
                self.list[x][y] = self.text[char]
                y -= 1
                x += 1
            #Correct overflows and switch directions
            if self.height == 1: #Catch edgecase without ZigZag
                x += 1
                y -= 1 #Just walk right
            elif y == self.height: #Catch edge bottom
                x += 1
                y -= 2
                flag = 0
            elif y == -1: #Catch edge at top
                x -= 1
                y += 2
                flag = 1
            char += 1 #nextChar
            
    def walkList(self) -> str:
        x, y = 0, 0
        res = []
        while y < self.height: #forEachRow
            while x < self.width:#ForEachElem
                if self.list[x][y] != None: #Catch None's
                    res.append(self.list[x][y]) #Get Elem
                x += 1
            y += 1
            x = 0
        return "".join(res) #build res-string
    
    def getString(self) -> str:
        return self.string


#Tests
#testdataList: (input1, input2, output)
pp = "PAYPALISHIRING"
io = [(pp, -1, pp),
      (pp, 0, pp),
      (pp, 1, pp),
      ("A", 1, "A"),
      ("A,", 1, "A,"),
      ("A.", 1, "A."),
      ("THISSTRING", 10, "THISSTRING"),
      (pp, 2, "PYAIHRNAPLSIIG"),
      (pp, 3, "PAHNAPLSIIGYIR"),
      (pp, 4, "PINALSIGYAHRPI"),
      (pp, len(pp), pp),
      (pp, len(pp)+2, pp),
      (pp, len(pp)-1, "PAYPALISHIRIGN")]
#Test-Loop
for n in range(0,len(io)):
    akt = ZigZag(io[n][0],io[n][1]) #ini
    try:
        print("Test"+str(n+1)+": "+str(io[n][2]==akt.getString()))
    except:
        print("Test"+str(n+1)+": "+"False")
    