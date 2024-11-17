class Parser:
    def __init__(self, input_string):
        self.input = input_string.replace(" ", "")  
        self.index = 0

    def parse(self):
        return self.S() and self.index == len(self.input)

    def current_char(self):
        if self.index < len(self.input):
            return self.input[self.index]
        return None

    def match(self, char):
        if self.current_char() == char:
            self.index += 1
            return True
        return False

    def S(self):
        return self.C()

    def C(self):
        if self.N():
            if self.match('+') or self.match('-') or self.match('*') or self.match('/'):
                return self.N()
        return False

    def N(self):
        start_index = self.index

        if self.integer_part() and self.match('.') and self.fractional_part():
            return True

        self.index = start_index

        if self.D():
            while self.D():  
                pass
            return True

        self.index = start_index

        return self.D()

    def integer_part(self):
       
        if self.D():
            while self.D():
                pass 
            return True
        return False

    def fractional_part(self):
        
        if self.D():
            while self.D():
                pass 
            return True
        return False

    def D(self):
        if self.current_char() and self.current_char().isdigit():
            self.index += 1
            return True
        return False


if __name__ == "__main__":
    inputs = [
        "123+456",         
        "78.9-34.56",      
        "12*3",            
        "100/25",          
        "12.34+56",        
        "9.9*9.9",         
        "12345",          
        "12..34+56",     
        "12.+34",         
        "78.-34.56",       
    ]

    for input_string in inputs:
        parser = Parser(input_string)
        result = parser.parse()
        print(f"'{input_string}' es {'válido' if result else 'inválido'}")
