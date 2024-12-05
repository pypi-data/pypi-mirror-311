from math import sqrt

class sujith:
    def __init__(self,a):
        self.a = a
    def mysqrt(self):
        for i in range(self.a):
            res  = sqrt(i)
            print(res)

a = 5
obj = sujith(a)
obj.mysqrt()