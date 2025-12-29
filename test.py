class test :
    def __init__(self):
        self.input_reciever()
    
    def input(self):
        self.input = input("print")
        return self.input
        
    def input_reciever(self):
        x = self.input()
        print(x , "this is the print")
        
x = test()
x.input_reciever()