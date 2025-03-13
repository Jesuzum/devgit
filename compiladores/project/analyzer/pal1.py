from pr import funciones_incorporadas, palabras_reservadas

class A_lexico:
    def __init__(self):
        self.estado = 'inicio'
        self.funciones_incorporadas = funciones_incorporadas
        self.palabras_reservadas = palabras_reservadas
        self.operadores = {"+", "-", "*", "/", "%", "**", "=", "+=", "-=", "*=", "/=", "==", "!=", "<", ">", "<=", ">=", "&&", "||", "!", "."}
        self.tipo_token = None  # Para almacenar el tipo de token identificado

    def transicion(self, caracter):
        if self.estado == 'inicio':
            if caracter == '$':  
                self.estado = 'variable'
                self.tipo_token = "Variable escalar"
            elif caracter == '@':  
                self.estado = 'arreglo'
                self.tipo_token = "Arreglo"
            elif caracter == '%':  
                self.estado = 'hash'
                self.tipo_token = "Hash"
            elif caracter.isdigit():  
                self.estado = 'numero'
                self.tipo_token = "Número entero"
            elif caracter in self.operadores:  
                self.estado = 'operador'
                self.tipo_token = "Operador"
            else:
                self.estado = 'error'

        elif self.estado in ['variable', 'arreglo', 'hash']:
            if caracter.isalpha() or caracter == '_':
                self.estado = 'identificador'
            else:
                self.estado = 'error'

        elif self.estado == 'identificador':
            if caracter.isalnum() or caracter == '_':
                pass
            else:
                self.estado = 'error'

        elif self.estado == 'numero':
            if caracter.isdigit():
                pass  
            elif caracter == '.':
                self.estado = 'decimal'
                self.tipo_token = "Número decimal"
            elif caracter.lower() == 'e':  
                self.estado = 'exponente'
                self.tipo_token = "Número en notación científica"
            else:
                self.estado = 'error'

        elif self.estado == 'decimal':
            if caracter.isdigit():
                self.estado = 'decimal_ok'
            else:
                self.estado = 'error'

        elif self.estado == 'decimal_ok':
            if caracter.isdigit():
                pass  
            elif caracter.lower() == 'e':
                self.estado = 'exponente'
            else:
                self.estado = 'error'

        elif self.estado == 'exponente':
            if caracter.isdigit() or caracter in ['+', '-']:
                self.estado = 'exponente_ok'
            else:
                self.estado = 'error'

        elif self.estado == 'exponente_ok':
            if caracter.isdigit():
                pass  
            else:
                self.estado = 'error'

        elif self.estado == 'operador':
            if caracter in self.operadores:
                pass  
            else:
                self.estado = 'error'

    def evaluar_cadena(self, cadena):
        self.estado = 'inicio'
        self.tipo_token = None  
        
        for caracter in cadena:
            self.transicion(caracter)
            if self.estado == 'error':
                return False, None  

        if self.estado in ['identificador', 'numero', 'decimal_ok', 'exponente_ok', 'operador']:
            return True, self.tipo_token  
        return False, None  

# Pruebas con tokens válidos e inválidos
analizador = A_lexico()
tokens = [
    # Válidos
    "$var", "@array", "%hash", "42", "3.14", "-7", "2e10", "+", "-", "**", "==", "!=", "$_valid",
    
    # Inválidos
    "$2var",    # No puede empezar con número
    "@array!",  # No puede contener !
    "%hash#",   # No puede contener #
    "3..14",    # No puede tener dos puntos seguidos
    "2e",       # No puede terminar en 'e'
    "5e-",      # No puede terminar en 'e-'
    "***",      # No es un operador válido
    "==!",      # No es un operador válido
    "+-",       # No puede tener dos operadores juntos sin número
    "&nombre",  # El símbolo & no está permitido aquí
    "¿?",       # Símbolos no válidos
    "var$",     # No puede terminar con $
]

for token in tokens:
    es_valido, tipo = analizador.evaluar_cadena(token)
    if es_valido:
        print(f"{token}  es un token válido de tipo: {tipo}")
    else:
        print(f"{token} ERROR: es un token NO válido")
