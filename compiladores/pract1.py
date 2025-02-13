class Automata: 
    def __init__(self):
        self.estado = 'inicio'  # Estado inicial
    
    def transicion(self, caracter):
        if self.estado == 'inicio':
            if caracter.isalpha() or caracter == '_':  # Comienza con letra o guion bajo
                self.estado = 'valido'
            else:
                self.estado = 'invalido'
        elif self.estado == 'valido':
            if caracter.isalnum() or caracter == '_':  # Permite letras, números o guion bajo
                self.estado = 'valido'  # Permanece en válido
            else: 
                self.estado = 'invalido'  # Si encuentra un carácter no válido
    
    def evaluar_cadena(self, cadena):
        self.estado = 'inicio'  
        for caracter in cadena:
            self.transicion(caracter)
            if self.estado == 'invalido':  
                return False
        return self.estado == 'valido' 


automata = Automata()
palabras = ["1haha", "clear", "ajaQ@", "_ja"]

for palabra in palabras:
    if automata.evaluar_cadena(palabra):
        print(f"La palabra '{palabra}' es válida.")
    else:
        print(f"La palabra '{palabra}' no es válida.")