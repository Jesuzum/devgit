from pr import *

class AnalizadorLexico:
    def __init__(self):
        self.tokens = []  # Lista de tokens reconocidos
        self.warnings = []  # Lista de advertencias
        self.en_funcion = False  # Estado para detectar nombres de funciones en `sub`
        self.dentro_de_hash = False  # Estado para detectar claves dentro de un hash
        self.ultima_palabra = ""  # Guarda el último token para saber si es una llamada a función

    def es_variable_valida(self, token):
        """Verifica si un token es una variable válida en Perl y genera advertencias en caso de error."""
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

    def analizar(self, codigo):
        """Analiza un fragmento de código Perl y reconoce los tokens sin expresiones regulares."""
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
                if caracter == en_cadena:  # Cierra la cadena
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

            if caracter == "{":  # Puede ser inicio de bloque o de clave de hash
                self.tokens.append((caracter, "delimitador"))
                if i > 0 and codigo[i - 1] == "%":  # Si el anterior era `%`, estamos en un hash
                    self.dentro_de_hash = True
                continue

            if caracter == "}":  # Fin de una clave dentro de un hash
                self.tokens.append((caracter, "delimitador"))
                self.dentro_de_hash = False
                continue

            if caracter.isspace() or caracter in "{}()[],;=+-*/<>!":
                if palabra:
                    self.procesar_palabra(palabra, codigo, i)
                    palabra = ""

                if caracter in "{}()[],;=+-*/<>!":
                    self.tokens.append((caracter, "operador" if caracter in "=+-*/<>" else "delimitador"))

                continue

            palabra += caracter

        if palabra:
            self.procesar_palabra(palabra, codigo, len(codigo))

    def procesar_palabra(self, palabra, codigo, index):
        """Procesa una palabra y la clasifica como variable, número, palabra reservada, etc."""
        if self.en_funcion:  # Si viene después de `sub`, es un nombre de función
            self.tokens.append((palabra, "nombre de función"))
            self.en_funcion = False
            return

        if self.dentro_de_hash:  # Si estamos dentro de un hash, es una clave de hash
            self.tokens.append((palabra, "clave de hash"))
            return

        # Si la siguiente palabra es un `(`, asumimos que es una llamada a función
        if index < len(codigo) - 1 and codigo[index] == "(":
            self.tokens.append((palabra, "llamada a función"))
            return

        if palabra == "sub":
            self.tokens.append((palabra, "palabra reservada"))
            self.en_funcion = True  # La siguiente palabra debe ser un nombre de función
        elif palabra.isdigit():
            self.tokens.append((palabra, "número"))
        elif palabra in palabras_reservadas:
            self.tokens.append((palabra, "palabra reservada"))
        elif palabra in funciones_incorporadas:
            self.tokens.append((palabra, "función incorporada"))
        elif self.es_variable_valida(palabra):
            self.tokens.append((palabra, "variable"))
        else:
            self.warnings.append(f'WARNING: "{palabra}" no es un token válido.')

    def mostrar_tokens(self):
        """Muestra los tokens reconocidos y advertencias."""
        print("\n=== TOKENS RECONOCIDOS ===")
        for token, tipo in self.tokens:
            print(f"{token}: {tipo}")

        if self.warnings:
            print("\n=== ADVERTENCIAS ===")
            for warning in set(self.warnings):
                print(warning)


# =======================
#   PRUEBA DEL CÓDIGO
# =======================
codigo_prueba = """
use strict;
use warnings;

my $nombre = "Carlos";
my $salario = 50000;
my $bono = 5000;

sub calcular_salario_final {
    my ($base, $extra) = @_;
    return $base + $extra;
}

my $salario_final = calcular_salario_final($salario, $bono);

print "Empleado: $nombre\n";
print "Salario final: $salario_final\n";

"""

analizador = AnalizadorLexico()
analizador.analizar(codigo_prueba)
analizador.mostrar_tokens()