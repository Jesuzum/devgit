from pr import funciones_incorporadas, palabras_reservadas

class A_lexico:
    def __init__(self):
        self.estado = 'inicio'
        self.funciones_incorporadas = funciones_incorporadas
        self.palabras_reservadas = palabras_reservadas

    def transicion(self, caracter):
        # Analiza el primer caracter para saber si es una variable, arreglo o hash
        if self.estado == 'inicio':
            if caracter == '$':  # comienza con $ que en perl guarda un solo valor
                self.estado = 'variable'
            elif caracter == '@':  # comienza con @ que en perl guarda un array
                self.estado = 'arreglo'
            elif caracter == '%':  # comienza con % que en perl guarda un hash
                self.estado = 'hash'
            else:
                self.estado = 'error'
        # Analiza el segundo caracter para saber si es una variable, arreglo o hash validos
        elif self.estado == 'variable':
            if caracter.isalpha() or caracter == '_':
                self.estado = 'variableValida'
            else:
                self.estado = 'error'
        elif self.estado == 'arreglo':
            if caracter.isalpha() or caracter == '_':
                self.estado = 'arregloValido'
            else:
                self.estado = 'error'
        elif self.estado == 'hash':
            if caracter.isalpha() or caracter == '_':
                self.estado = 'hashValido'
            else:
                self.estado = 'error'
        # Termina de validar la palabra
        elif self.estado == 'variableValida' or self.estado == 'arregloValido' or self.estado == 'hashValido':
            if caracter.isalnum() or caracter == '_':
                # Sigue permitiendo caracteres alfanuméricos o guión bajo
                pass
            else:
                self.estado = 'error'

    def evaluar_cadena(self, cadena):
        self.estado = 'inicio'
        for caracter in cadena:
            self.transicion(caracter)
            if self.estado == 'error':
                return False
        # Asegúrate de que el estado final sea uno de los válidos
        if self.estado in ['variableValida', 'arregloValido', 'hashValido']:
            return True
        return False

    def es_funcion_o_reservada(self, palabra):
        if palabra in self.funciones_incorporadas:
            return "funcion incorporada"
        elif palabra in self.palabras_reservadas:
            return "palabra reservada"
        else:
            return "ninguna"

    def es_valida(self, palabra):
        # Primero, valida la palabra con el analizador léxico
        if not self.evaluar_cadena(palabra):
            return False
        
        # Luego, verifica si la palabra es una función o palabra reservada
        tipo_palabra = self.es_funcion_o_reservada(palabra)
        if tipo_palabra != "ninguna":
            return False
        
        # Verifica si la palabra es válida: empieza con $/@/% pero no es palabra reservada ni función
        if palabra[0] in ['$','@','%']:
            if palabra[1:] in self.funciones_incorporadas or palabra[1:] in self.palabras_reservadas:
                return False
        
        return True

# Probar el código
analizador = A_lexico()
palabras = ["$variable", "@arreglo", "%hash", "@2arreglo", "$_variable", "%_hash", "$_2variable", "%_2hash", "int", "exit", "@int", "$rand"]

for palabra in palabras:
    if analizador.es_valida(palabra):
        print(f"{palabra} es una palabra valida")
    else:
        print(f"{palabra} es una palabra no valida")
