class Rectangle:
    def __init__(self,a,b):
        self.a = a
        self.b = b

    def cal_area(self):
        return self.a*self.b

class Square(Rectangle):
    def __init__(self,length):
        super().__init__(length,length)
