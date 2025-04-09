from .pr import *

class AnalizadorLexico:
    def __init__(self):
        self.tokens = []           # Lista de tokens reconocidos.
        self.warnings = []         # Lista de advertencias.
        self.en_funcion = False    # Estado para detectar nombres de funciones en 'sub'.
        self.dentro_de_hash = False  # Estado para detectar claves dentro de un hash.

    def es_variable_valida(self, token):
        """Verifica si un token es una variable válida en Perl y genera advertencias si no lo es."""
        if token[0] in "$@%":
            if len(token) == 1:
                self.warnings.append(f'WARNING: "{token}" no es un nombre de variable válido.')
                return False

            if not (token[1].isalpha() or token[1] == "_"):
                self.warnings.append(f'WARNING: La variable "{token}" debe comenzar con una letra o guion bajo.')
                return False

            if token[1:] in palabras_reservadas:
                self.warnings.append(f'WARNING: La variable "{token}" no puede llamarse como una palabra reservada.')
                return False

            return True
        return False

    def siguiente_no_espacio(self, codigo, index):
        """
        Retorna el siguiente carácter en 'codigo' a partir de 'index' que no sea un espacio.
        De esta forma podemos ignorar los espacios intermedios al determinar si el token
        actual debería interpretarse como una llamada a función.
        """
        pos = index
        while pos < len(codigo) and codigo[pos].isspace():
            pos += 1
        if pos < len(codigo):
            return codigo[pos]
        return ''

    def analizar(self, codigo):
        """Analiza un fragmento de código Perl y reconoce los tokens sin usar expresiones regulares."""
        palabra = ""
        en_cadena = False
        en_comentario = False

        for i, caracter in enumerate(codigo):
            if en_comentario:
                if caracter == "\n":  # Fin del comentario
                    self.tokens.append((palabra, "comentario"))
                    palabra = ""
                    en_comentario = False
                else:
                    palabra += caracter
                continue

            if en_cadena:
                palabra += caracter
                if caracter == en_cadena:  # Se cierra la cadena
                    self.tokens.append((palabra, "cadena"))
                    palabra = ""
                    en_cadena = False
                continue

            if caracter in "\"'":  # Inicia cadena
                en_cadena = caracter
                palabra += caracter
                continue

            if caracter == "#":  # Inicia comentario
                en_comentario = True
                palabra += caracter
                continue

            if caracter == "{":  # Puede ser inicio de bloque o clave de hash
                self.tokens.append((caracter, "delimitador"))
                if i > 0 and codigo[i - 1] == "%":  # Si el anterior era '%', estamos en un hash
                    self.dentro_de_hash = True
                continue

            if caracter == "}":  # Fin de una clave dentro de un hash
                self.tokens.append((caracter, "delimitador"))
                self.dentro_de_hash = False
                continue

            if caracter.isspace() or caracter in "{}()[],:;=+-*/<>!":
                if palabra:
                    self.procesar_palabra(palabra, codigo, i)
                    palabra = ""
                # Se registra el delimitador u operador actual (si no es espacio)
                if caracter in "{}()[],:;=+-*/<>!":
                    tipo = "operador" if caracter in "=+-*/<>" else "delimitador"
                    self.tokens.append((caracter, tipo))
                continue

            palabra += caracter

        if palabra:
            self.procesar_palabra(palabra, codigo, len(codigo))

    def procesar_palabra(self, palabra, codigo, index):
        """Procesa una palabra y la clasifica como variable, número, palabra reservada, etc."""
        # Si se esperaba el nombre de una función tras 'sub'
        if self.en_funcion:
            self.tokens.append((palabra, "nombre de función"))
            self.en_funcion = False
            return

        # Si estamos dentro de un hash, se trata como clave
        if self.dentro_de_hash:
            self.tokens.append((palabra, "clave de hash"))
            return
        
        # Reconocimiento para el ciclo for.
        if palabra == "for":
            self.tokens.append((palabra, "FOR"))
            return
        
        # Reconocimiento especial para sentencias condicionales
        # Agregamos reconocimiento para switch, case y default.
        if palabra == "switch":
            self.tokens.append((palabra, "SWITCH"))
            return
        elif palabra == "case":
            self.tokens.append((palabra, "CASE"))
            return
        elif palabra == "default":
            self.tokens.append((palabra, "DEFAULT"))
            return
        
        #Sentencia if, elsif y else
        if palabra == "if":
            self.tokens.append((palabra, "IF"))
            return
        elif palabra == "elsif":
            self.tokens.append((palabra, "ELSIF"))
            return
        elif palabra == "else":
            self.tokens.append((palabra, "ELSE"))
            return

        # Reconocimiento de palabras reservadas y funciones incorporadas.
        if palabra == "sub":
            self.tokens.append((palabra, "palabra reservada"))
            self.en_funcion = True  # La siguiente palabra debe ser el nombre de la función.
            return
        elif palabra in palabras_reservadas:
            self.tokens.append((palabra, "palabra reservada"))
            return
        elif palabra in funciones_incorporadas:
            self.tokens.append((palabra, "función incorporada"))
            return
        elif palabra.isdigit():
            self.tokens.append((palabra, "número"))
            return

        # Determinación final: si el siguiente carácter es '(', se clasifica como llamada a función.
        siguiente = self.siguiente_no_espacio(codigo, index)
        if siguiente == "(":
            self.tokens.append((palabra, "llamada a función"))
        else:
            if self.es_variable_valida(palabra):
                self.tokens.append((palabra, "variable"))
            else:
                self.warnings.append(f'WARNING: "{palabra}" no es un token válido.')

    def mostrar_tokens(self):
        """Muestra los tokens reconocidos y las advertencias."""
        print("\n=== TOKENS RECONOCIDOS ===")
        for token, tipo in self.tokens:
            print(f"{token}: {tipo}")
        if self.warnings:
            print("\n=== ADVERTENCIAS ===")
            for warning in set(self.warnings):
                print(warning)