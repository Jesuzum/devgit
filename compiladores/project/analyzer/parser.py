from .pr import *

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
        en caso contrario, registra un error y fuerza un avance para evitar ciclos.
        """
        token = self.current_token()
        if token[0] == expected and (tipo_esperado is None or token[1] == tipo_esperado):
            self.advance()
            return token
        else:
            self.error(f"Se esperaba '{expected}' (tipo {tipo_esperado}) pero se encontró {token}")
            # Forzamos avanzar para no quedar atrapados
            self.advance()
            return None

    def error(self, mensaje):
        """Registra y muestra un mensaje de error sintáctico."""
        error_msg = f"SyntaxError: {mensaje}"
        self.errors.append(error_msg)
        print(error_msg)

    def parse(self):
        """Recorre la lista de tokens reconociendo sentencias."""
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
          - O expresiones (por ejemplo, asignaciones o llamadas a función)
          - Construcciones condicionales: if / elsif / else
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

        elif token[1] == "FOR":
            self.for_statement()

        elif token[1] in ("IF", "ELSIF", "ELSE"):
            self.conditional_statement()
        elif token[1] == "SWITCH":
            self.switch_statement()
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
        Permite declarar una variable o una lista, con asignación opcional.
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
        operadores (+, -, *, /, >, <) seguidos de otro término.
        Finaliza si se encuentra un delimitador natural (')', ',' o ';').
        """
        if self.pos < len(self.tokens) and self.current_token()[0] in (")", ",", ";"):
            return
        self.term()
        while self.pos < len(self.tokens) and self.current_token()[0] in ("+", "-", "*", "/", ">", "<"):
            self.advance()
            self.term()


    def term(self):
        """
        Procesa un término que puede ser:
          - una variable, número o cadena,
          - una llamada a función (clasificada como 'función incorporada' o 'llamada a función'),
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
        Procesa una llamada a función, con o sin paréntesis.
        Por ejemplo: print "texto";  o  print("texto");
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
        """Procesa la lista de argumentos: expresión ( , expresión )*."""
        self.expression()
        while self.pos < len(self.tokens) and self.current_token()[0] == ",":
            self.match(",", "delimitador")
            self.expression()

    def conditional_statement(self):
        """
        Procesa la estructura condicional:
          if (condición) { bloque }
          [elsif (condición) { bloque }]* 
          [else { bloque }]
        """
        # Procesar el 'if'
        self.match("if", "IF")
        self.match("(", "delimitador")
        self.expression()
        self.match(")", "delimitador")
        self.block()
        print("Sentencia 'if' analizada.")

        # Procesar cero o más 'elsif'
        while self.pos < len(self.tokens) and self.current_token()[1] == "ELSIF":
            self.match("elsif", "ELSIF")
            self.match("(", "delimitador")
            self.expression()
            self.match(")", "delimitador")
            self.block()
            print("Sentencia 'elsif' analizada.")

        # Procesar el 'else', si existe
        if self.pos < len(self.tokens) and self.current_token()[1] == "ELSE":
            self.match("else", "ELSE")
            self.block()
            print("Sentencia 'else' analizada.")
            
    def switch_statement(self):
        """
        Procesa la estructura switch:
        switch ( expresión ) {
            case expresión : { bloque }
            [ case expresión : { bloque } ]*
            [ default : { bloque } ]
        }
        """
        # Procesar 'switch'
        self.match("switch", "SWITCH")
        self.match("(", "delimitador")
        self.expression()
        self.match(")", "delimitador")
        self.match("{", "delimitador")
        
        # Procesar los casos 'case'
        while self.pos < len(self.tokens) and self.current_token()[0] == "case" and self.current_token()[1] == "CASE":
            self.case_clause()
        
        # Procesar la cláusula opcional 'default'
        if self.pos < len(self.tokens) and self.current_token()[0] == "default" and self.current_token()[1] == "DEFAULT":
            self.default_clause()
        
        self.match("}", "delimitador")
        print("Sentencia 'switch' analizada.")

    def case_clause(self):
        """
        Procesa una cláusula 'case':
        case expresión : { bloque }
        """
        self.match("case", "CASE")
        self.expression()
        # Se espera el delimitador ':'; asumiendo que el lexer lo genera como token delimitador ":".
        self.match(":", "delimitador")
        self.match("{", "delimitador")
        # Procesa las sentencias dentro del bloque del case.
        while self.pos < len(self.tokens) and self.current_token()[0] != "}":
            self.statement()
        self.match("}", "delimitador")
        print("Sentencia 'case' analizada.")

    def default_clause(self):
        """
        Procesa la cláusula 'default':
        default : { bloque }
        """
        self.match("default", "DEFAULT")
        self.match(":", "delimitador")
        self.match("{", "delimitador")
        # Procesa las sentencias dentro del bloque por defecto.
        while self.pos < len(self.tokens) and self.current_token()[0] != "}":
            self.statement()
        self.match("}", "delimitador")
        print("Sentencia 'default' analizada.")
        
    def for_statement(self):
        """
        Procesa la estructura for (estilo Perl). Se admiten dos formas:

        1) For clásico:
            for ( inicialización ; condición ; incremento ) { bloque }
            
        2) For iterativo:
            for VARIABLE ( lista ) { bloque }
        """
        # Procesar la palabra clave for.
        self.match("for", "FOR")
        
        # Comprobar si se trata de la forma clásica:
        if self.current_token()[0] == "(" and self.current_token()[1] == "delimitador":
            # Forma clásica
            self.match("(", "delimitador")
            
            # Inicialización (p.ej., my $i = 0)
            self.for_initialization()
            self.match(";", "SEMICOLON")
            
            # Condición (p.ej., $i < 10)
            self.for_condition()
            self.match(";", "SEMICOLON")
            
            # Incremento (p.ej., $i++)
            self.for_increment()
            self.match(")", "delimitador")
            
            # Bloque
            self.block()
            print("Sentencia 'for' clásica analizada.")
        
        # Sino, forma iterativa: for VARIABLE ( lista ) { bloque }
        elif self.current_token()[1] == "VARIABLE":
            # Se procesa la variable iteradora.
            self.match_type("VARIABLE")
            
            # La lista de elementos debe estar entre paréntesis.
            self.match("(", "delimitador")
            self.for_list()
            self.match(")", "delimitador")
            
            # Bloque
            self.block()
            print("Sentencia 'for' iterativa analizada.")
        
        else:
            self.error("Estructura for inválida.")

    def for_initialization(self):
        """
        Procesa la parte de inicialización del for clásico.
        Se asume que es una expresión, que puede incluir, por ejemplo, la palabra "my".
        """
        self.expression()

    def for_condition(self):
        """
        Procesa la condición del for clásico, que debe evaluar a un valor booleano.
        """
        self.expression()

    def for_increment(self):
        """
        Procesa la parte de incremento del for clásico.
        Se espera una expresión que modifique la variable iteradora (por ejemplo: $i++ o $i += 1).
        """
        self.expression()

    def for_list(self):
        """
        Procesa la lista para el for iterativo.
        Se asume que es una lista de elementos separados por comas.
        """
        # Procesar el primer elemento de la lista.
        self.expression()
        # Mientras se encuentre la coma, se consumen y se procesa el siguiente elemento.
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