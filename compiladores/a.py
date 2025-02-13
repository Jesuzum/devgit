class ParserTree:
    def __init__(self):
        self.estado = 'inicio'
    
    def action(self, caracter):
        exp_init = '('
        exp_end = ')'
        operator = ['+', '-', '*', '/']
        lista = []

        if self.estado == 'inicio':
            if caracter.isnumeric() or caracter == exp_init:
                if caracter.isnumeric():
                    print("num")
                    self.estado = 'valido'
                elif caracter == exp_init:
                    print("<expr>")
                    self.estado = 'capturando'
        elif self.estado == 'capturando':
            if caracter.isnumeric() or caracter in operator:
                if caracter.isnumeric():
                    lista.append("num")
                    self.estado = 'capturando'
                elif caracter in operator:
                    lista.append("<op>")
                    self.estado = 'capturando'
                elif caracter == exp_end:
                    print(lista)
                    self.estado = 'valido'
                    lista.clear()
        elif self.estado == 'valido':
            if caracter.isnumeric() or caracter in operator:
                if caracter.isnumeric():
                    print("num")
                    self.estado = 'valido'
                elif caracter in operator:
                    print("<op>")
                    self.estado = 'valido'
            elif caracter == exp_init:
                print("<expr>")
                self.estado = 'capturando'
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
        elif self.estado == 'capturando':
            print("Cargando lista")
        else:
            print("Expresion no valida")

tree = ParserTree()
tree.evaluate_expresion("(2+3)*4")