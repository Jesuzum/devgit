# parser.py
from .pr import *
from .lexer import AnalizadorLexico  # Se asume que el lexer revisado está en lexer.py

class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens          # Lista de tokens generada por el analizador léxico.
        self.pos = 0                  # Posición actual en la lista de tokens.
        self.errors = []              # Lista de errores encontrados.

    def current_token(self):
        """
        Devuelve el siguiente token significativo (ignorando comentarios) o EOF.
        Esto permite que los comentarios se salten sin interferir en el análisis.
        """
        while self.pos < len(self.tokens) and self.tokens[self.pos][1] == "comentario":
            self.pos += 1
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ("EOF", "EOF")

    def advance(self):
        """Avanza al siguiente token (recordando que current_token() se salta los comentarios)."""
        self.pos += 1

    def match(self, expected, tipo_esperado=None):
        """
        Consume el token actual si coincide con 'expected' (y opcionalmente con 'tipo_esperado');
        en caso contrario, registra un error con estilo terminal.
        """
        token = self.current_token()
        if token[0] == expected and (tipo_esperado is None or token[1] == tipo_esperado):
            self.advance()
            return token
        else:
            self.error(f"Se esperaba '{expected}' (tipo {tipo_esperado}) pero se encontró {token}")
            return None

    def error(self, mensaje):
        """Registra y muestra un mensaje de error sintáctico con el formato de terminal."""
        error_msg = f"SyntaxError: {mensaje}"
        self.errors.append(error_msg)
        print(error_msg)
        # Opcional: Podríamos implementar una estrategia de sincronización para evitar cascadas de errores.
        # Por ejemplo:
        # while self.pos < len(self.tokens) and self.current_token()[0] not in (";", "}"):
        #     self.advance()
        # self.advance()

    def parse(self):
        """Recorre toda la lista de tokens reconociendo sentencias."""
        print("Iniciando análisis sintáctico...")
        while self.pos < len(self.tokens) and self.current_token()[0] != "EOF":
            self.statement()
        if not self.errors:
            print("Análisis sintáctico completado sin errores.")
        else:
            print("Se encontraron errores en el análisis sintáctico.")

    def statement(self):
        """
        Reconoce una sentencia según el token actual.
        Se distinguen:
          - Sentencias 'use'
          - Declaraciones con 'my'
          - Definiciones de funciones con 'sub'
          - Sentencias 'return'
          - O expresiones (como asignaciones o llamadas a función)
        """
        token = self.current_token()
        if token[1] == "palabra reservada":
            if token[0] == "use":
                self.use_statement()
            elif token[0] == "my":
                self.declaration_statement()
            elif token[0] == "sub":
                self.function_definition()
            elif token[0] == "return":
                self.return_statement()
            else:
                self.expression_statement()  # Para otras palabras reservadas.
        else:
            self.expression_statement()

    def use_statement(self):
        # Regla: use <módulo> ;
        self.match("use", "palabra reservada")
        token = self.current_token()
        if token[1] in ("palabra reservada", "variable"):
            self.advance()
        else:
            self.error("Se esperaba un módulo (ej., 'strict' o 'warnings') después de 'use'.")
        self.match(";", "delimitador")
        print("Sentencia 'use' analizada.")

    def declaration_statement(self):
        """
        Regla: my ( variable | ( lista_de_variables ) ) [= expresión] ;
        Se permite declarar una variable o una lista, seguida opcionalmente de asignación.
        """
        self.match("my", "palabra reservada")
        token = self.current_token()
        if token[0] == "(":
            self.match("(", "delimitador")
            self.variable_list()
            self.match(")", "delimitador")
        elif token[1] == "variable":
            self.advance()
        else:
            self.error("Se esperaba una variable o lista de variables después de 'my'.")
        # Asignación opcional
        token = self.current_token()
        if token and token[0] == "=":
            self.match("=", "operador")
            self.expression()
        self.match(";", "delimitador")
        print("Declaración analizada.")

    def variable_list(self):
        """Procesa una lista de variables separadas por comas."""
        token = self.current_token()
        if token[1] == "variable":
            self.advance()
        else:
            self.error("Se esperaba una variable en la lista de variables.")
            return
        while self.pos < len(self.tokens) and self.current_token()[0] == ",":
            self.match(",", "delimitador")
            token = self.current_token()
            if token[1] == "variable":
                self.advance()
            else:
                self.error("Se esperaba una variable después de ','.")
        # El token ")" se consume en declaration_statement.

    def function_definition(self):
        # Regla: sub <nombre_de_función> <bloque>
        self.match("sub", "palabra reservada")
        token = self.current_token()
        if token and token[1] == "nombre de función":
            self.advance()
        else:
            self.error("Se esperaba el nombre de la función después de 'sub'.")
        self.block()
        print("Definición de función analizada.")

    def block(self):
        # Regla: { sentencias* }
        self.match("{", "delimitador")
        while self.pos < len(self.tokens) and self.current_token()[0] != "}":
            self.statement()
        self.match("}", "delimitador")
        print("Bloque analizado.")

    def return_statement(self):
        # Regla: return <expresión> ;
        self.match("return", "palabra reservada")
        self.expression()
        self.match(";", "delimitador")
        print("Sentencia 'return' analizada.")

    def expression_statement(self):
        """Regla: expresión ;"""
        self.expression()
        self.match(";", "delimitador")
        print("Sentencia de expresión analizada.")

    def expression(self):
        """
        Expresión simplificada que procesa un término y, opcionalmente,
        operadores (+, -, *, /) seguidos de otro término.
        Si se encuentra un delimitador natural (')', ',' o ';') se finaliza.
        """
        if self.pos < len(self.tokens) and self.current_token()[0] in (")", ",", ";"):
            return
        self.term()
        while self.pos < len(self.tokens) and self.current_token()[0] in ("+", "-", "*", "/"):
            self.advance()
            self.term()

    def term(self):
        """
        Procesa un término, que puede ser:
          - una variable, número o cadena,
          - una llamada a función (ya clasificada como 'función incorporada' o 'llamada a función'),
          - o una expresión entre paréntesis.
        """
        token = self.current_token()
        if token[1] in ("variable", "número", "cadena"):
            self.advance()
        elif token[1] in ("función incorporada", "llamada a función"):
            nombre_funcion = token[0]
            self.advance()
            self.parse_function_call(nombre_funcion)
        elif token[0] == "(":
            self.match("(", "delimitador")
            self.expression()
            self.match(")", "delimitador")
        else:
            if token[0] in (")", ";", ","):
                return
            self.error(f"Token inesperado en la expresión: {token}")
            self.advance()

    def parse_function_call(self, nombre_funcion):
        """
        Procesa una llamada a función con o sin paréntesis.
        Ejemplo: print "texto";  o  print("texto");
        """
        if self.pos < len(self.tokens) and self.current_token()[0] == "(":
            self.match("(", "delimitador")
            if self.current_token()[0] != ")":
                self.arguments()
            self.match(")", "delimitador")
        else:
            if self.pos < len(self.tokens) and self.current_token()[0] not in (";", ",", ")"):
                self.expression()

    def arguments(self):
        """
        Procesa la lista de argumentos: expresión ( , expresión )*
        """
        self.expression()
        while self.pos < len(self.tokens) and self.current_token()[0] == ",":
            self.match(",", "delimitador")
            self.expression()

    def show_errors(self):
        """Muestra los errores sintácticos encontrados."""
        if self.errors:
            print("\n=== ERRORES SINTÁCTICOS ===")
            for err in self.errors:
                print(err)
        else:
            print("No se encontraron errores sintácticos.")