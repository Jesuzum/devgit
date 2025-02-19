import re

class Automata:
    def __init__(self, archivo):
        self.archivo = archivo
        self.tipos = {"int": "entero corto", "double": "entero largo", "str": "cadena", "bool": "booleano"}

    def extraer_variables(self, lineas):
        variables = []
        dentro_de_main = False

        for linea in lineas:
            linea = linea.strip()

            if "main()" in linea:
                dentro_de_main = True
                continue  

            if dentro_de_main:
                if linea == "}":  
                    break
                if linea: 
                    variables.append(linea)
        
        return variables
    
    def es_tipo_dato(self, token):
        return self.tipos.get(token, None)
    
    def es_variable_valida(self, token):
        return re.fullmatch(r"_?[a-zA-Z]\w*", token) is not None

    def analizar_archivo(self):
        with open(self.archivo, "r") as archivo:
            lineas = archivo.readlines()
        
        variables = self.extraer_variables(lineas)

        for linea in variables:
            tokens = linea.split()
            if len(tokens) != 2:
                print(f"{linea} // no identificado")
                continue
            
            tipo, var = tokens
            descripcion_tipo = self.es_tipo_dato(tipo)
            
            if descripcion_tipo and self.es_variable_valida(var):
                print(f"{linea} // tipo de dato {descripcion_tipo}, variable {var}")
            else:
                print(f"{linea} // no identificado")

if __name__ == "__main__":
    automata = Automata("tokens.txt")
    automata.analizar_archivo()
