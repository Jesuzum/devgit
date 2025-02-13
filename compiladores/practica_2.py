class ParserTree:
    def __init__(self):
        self.estado = 'inicio'
    
    def action(self, caracter):
        exp_init = '('
        exp_end = ')'
        operator = ['+', '-', '*', '/']

        if self.estado == 'inicio':
            if caracter.isnumeric() or caracter == exp_init:
                if caracter.isnumeric():
                    print("num")
                    self.estado = 'valido'
                elif caracter == exp_init:
                    print("<expr>")
                    self.estado = 'valido'
        elif self.estado == 'valido':
            if caracter.isnumeric() or caracter in operator:
                if caracter.isnumeric():
                    print("num")
                    self.estado = 'valido'
                elif caracter in operator:
                    print("<op>")
                    self.estado = 'valido'
            elif caracter == exp_end:
                print("")
                self.estado = 'valido'
        else:
            print("Cadena no valida")
            self.estado = 'error'
    
    def evaluate_expresion(self, expr):
        self.estado = 'inicio'
        for caracter in expr:
            self.action(caracter)
            if self.estado == 'error':
                break
        if self.estado == 'valido':
            print("Expresion valida")
        else:
            print("Expresion no valida")

tree = ParserTree()
tree.evaluate_expresion("(2+3)*4")