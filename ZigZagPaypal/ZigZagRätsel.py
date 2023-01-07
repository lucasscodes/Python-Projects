class Solution:
    def convert(self, s: str, numRows: int) -> str:
        s, res = list(s), ["" for i in range(numRows)]
        def upwards():
            for i in range(numRows-2,0,-1): res[i] += s.pop(0)
        def downwards():
            for i in range(numRows): res[i] += s.pop(0)
        try: 
            while True: downwards(); upwards() #Do the ZigZag until s is empty
        except IndexError: return "".join(res) #then combine strings to res
