import re

class Automata:
    def __init__(self, archivo):
        self.archivo = archivo
        self.tipos = {"int": "entero corto", "double": "entero largo", "str": "cadena", "bool": "booleano"}
    
    def es_tipo_dato(self, token):
        return self.tipos.get(token, None)
    
    def es_variable_valida(self, token):
        return re.fullmatch(r"_?[a-zA-Z]\w*", token) is not None
    
    def analizar_archivo(self):
        with open(self.archivo, "r") as archivo:
            lineas = archivo.readlines()
        
        for linea in lineas:
            tokens = linea.strip().split()
            if len(tokens) != 2:
                print(f"{linea.strip()} // no identificado")
                continue
            
            tipo, var = tokens
            descripcion_tipo = self.es_tipo_dato(tipo)
            
            if descripcion_tipo and self.es_variable_valida(var):
                print(f"{linea.strip()} // tipo de dato {descripcion_tipo}, variable {var}")
            else:
                print(f"{linea.strip()} // no identificado")

# Ejecutar el análisis sobre el archivo de prueba
if __name__ == "__main__":
    automata = Automata("tokens.txt")
    automata.analizar_archivo()
