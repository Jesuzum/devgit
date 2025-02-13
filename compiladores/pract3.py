class Automata:
    def __init__(self):
        self.estado = 'inicio'
        self.identificador_actual = ""
        self.identificadores = []
        self.codigo_intermedio = []
        self.bandera = False
    
    def procesar_caracter(self, caracter):
        if self.estado == 'inicio':
            if caracter.isalpha() or caracter == '_':
                self.identificador_actual += caracter
                self.estado = 'en_identificador'
            
        elif self.estado == 'en_identificador':
            if caracter.isalnum() or caracter == '_':
                self.identificador_actual += caracter
                self.estado = 'en_identificador'
            else:
                self.finalizar_identificador()
        else: 
            self.bandera = True
            self.estado = 'error'


    def finalizar_identificador(self):
        if self.identificador_actual and self.bandera == False:
            self.identificadores.append(self.identificador_actual)
            self.codigo_intermedio.append(f'IDENTIFICADOR: {self.identificador_actual}')
            self.identificador_actual = ""
    
    def procesar_entrada(self, entrada):
        for caracter in entrada:
            self.procesar_caracter(caracter)
            if self.estado == 'error':
                return False
        self.finalizar_identificador()  # Asegura que el último identificador se almacene
    
    def get_identificadores(self):
        return self.identificadores
    
    def get_codigo_intermedio(self):
        return self.codigo_intermedio


def main():
    entrada = "variable1 _var2  anotherVar3 var $x"
    automata = Automata()
    automata.procesar_entrada(entrada)
    
    print("Identificadores encontrados:")
    print(automata.get_identificadores())
    
    print("\nCódigo intermedio generado:")
    for linea in automata.get_codigo_intermedio():
        print(linea)

if __name__ == "__main__":
    main()
