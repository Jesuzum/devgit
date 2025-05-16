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
            elif token[0] == "while":  # <-- Rama para "while"
                self.while_statement()
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
        Se maneja la validación especial:
        - Para arrays (@): la asignación debe ser un literal de lista.
        - Para hashes (%): la asignación debe ser un literal de hash.
        """
        self.match("my", "palabra reservada")
        token = self.current_token()
        var_token = None  # Para almacenar la variable si se declara directamente.
        
        if token[0] == "(":
            # Declaración de lista de variables
            self.match("(", "delimitador")
            self.variable_list()
            self.match(")", "delimitador")
        elif token[1] == "variable":
            var_token = token
            self.advance()
        else:
            self.error("Se esperaba una variable o lista de variables después de 'my'.")
        
        # Asignación opcional: si se detecta "="
        token = self.current_token()
        if token and token[0] == "=":
            self.match("=", "operador")
            if var_token is not None:
                if var_token[0].startswith("@"):
                    # Validación para arrays: se espera un literal de lista
                    next_token = self.current_token()
                    if next_token[0] != "(":
                        self.error("Se esperaba una lista literal para asignar a la variable '" + var_token[0] + "'.")
                    else:
                        self.list_literal()
                elif var_token[0].startswith("%"):
                    # Caso hash: se debe validar con hash_literal()
                    next_token = self.current_token()
                    if next_token[0] != "(":
                        self.error("Se esperaba un literal de hash para asignar a la variable '" + var_token[0] + "'.")
                    else:
                        self.hash_literal()  # Función que consume la estructura del hash
                else:
                    # Para variables escalares, se procesa la expresión
                    self.expression()
        self.match(";", "delimitador")
        print("Declaración analizada.")



    def list_literal(self):
        """
        Procesa un literal de lista para asignación a arrays.
        Se espera la sintaxis:
        ( expresión [ , expresión ]* )
        Esto permite declarar, por ejemplo:
        my @numeros = (10, 20, 30, 40, 50);
        """
        self.match("(", "delimitador")
        # Permite una lista vacía, si así se desea.
        if self.current_token()[0] != ")":
            self.expression()
            # Se permiten cero o más expresiones separadas por coma.
            while self.pos < len(self.tokens) and self.current_token()[0] == ",":
                self.match(",", "delimitador")
                # Aseguramos que no se encuentre inmediatamente el cierre de lista
                if self.current_token()[0] == ")":
                    self.error("Error: se encontró una coma sin un elemento siguiente en la lista.")
                    break
                self.expression()
        self.match(")", "delimitador")


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
        - una variable, número o cadena;
        - una llamada a función (clasificada como 'función incorporada' o 'llamada a función'):
        - o una expresión entre paréntesis.
        
        Se ha agregado un caso específico para detectar el operador de post-incremento '++'
        cuando el término es una variable.
        """
        token = self.current_token()
        if token[1] in ("variable", "número", "cadena"):
            self.advance()  # Consumimos la variable (o número o cadena)
            # Si se trata de una variable, comprobamos si le siguen dos tokens '+' consecutivos.
            if token[1] == "variable":
                # Verificamos que queden al menos dos tokens y que ambos sean "+" de tipo "operador"
                if (self.pos < len(self.tokens) and self.tokens[self.pos][0] == "+" and 
                    self.tokens[self.pos][1] == "operador"):
                    if (self.pos + 1 < len(self.tokens) and self.tokens[self.pos+1][0] == "+" and 
                        self.tokens[self.pos+1][1] == "operador"):
                        # Se reconoce el post-incremento; consumimos ambos tokens.
                        self.advance()  # Consume el primer '+'
                        self.advance()  # Consume el segundo '+'
                        # Opcional: podrías marcar este término como post-incrementado si fuera relevante.
            return

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
            for variable ( lista ) { bloque }
        """
        # Consumir la palabra clave 'for'
        self.match("for", "FOR")
        token = self.current_token()

        # Caso 1: for clásico, se espera que el siguiente token sea "(" (delimitador)
        if token[0] == "(" and token[1] == "delimitador":
            self.match("(", "delimitador")
            # Procesar la parte de inicialización
            self.for_initialization()
            self.match(";", "delimitador")
            # Procesar la condición
            self.for_condition()
            self.match(";", "delimitador")
            # Procesar el incremento
            self.for_increment()
            self.match(")", "delimitador")
            # Procesar el bloque de sentencias
            self.block()
            print("Sentencia 'for' clásica analizada.")
        
        # Caso 2: for iterativo, se espera que el siguiente token sea una variable
        elif token[1] == "variable" or (token[1] == "llamada a función" and token[0].startswith('$')):
            # Si el token se etiquetó como "llamada a función" pero empieza con '$',
            # lo tratamos como variable.
            if token[1] == "llamada a función":
                token = (token[0], "variable")
            self.advance()  # Consume el token del iterador
            self.match("(", "delimitador")
            self.for_list()
            self.match(")", "delimitador")
            self.block()
            print("Sentencia 'for' iterativa analizada.")
        else:
            self.error("Estructura for inválida.")


    def for_initialization(self):
        """
        Procesa la parte de inicialización del for clásico.
        Permite declaraciones del tipo 'my $i = 0' o simples expresiones.
        """
        token = self.current_token()
        # Si la inicialización inicia con "my", lo tratamos como una declaración
        if token[0] == "my" and token[1] == "palabra reservada":
            self.match("my", "palabra reservada")
            token = self.current_token()
            if token[1] == "variable":
                self.advance()  # Consume la variable (ej.: $i)
            else:
                self.error("Se esperaba una variable después de 'my' en la inicialización del for.")
            
            token = self.current_token()
            # Se espera el operador '='
            if token[0] == "=" and token[1] == "operador":
                self.match("=", "operador")
                self.expression()  # Procesa la expresión asignada (ej.: 0)
            else:
                self.error("Se esperaba '=' en la inicialización del for.")
        else:
            # Si no es una declaración, se procesa como una expresión normal.
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


    def while_statement(self):
        """
        Procesa la sentencia while en Perl.
        Sintaxis:
        while ( condición ) { bloque }
        Además, se verifica que dentro del bloque se actualice la variable de control,
        para evitar loops potencialmente infinitos.
        """
        self.match("while", "palabra reservada")
        self.match("(", "delimitador")
        
        # Procesar y capturar la condición.
        start_condition = self.pos
        self.while_condition()
        cond_tokens = self.tokens[start_condition:self.pos]
        
        # Extraer la variable de control (heurística: la primera variable en la condición).
        control_var = self.extract_control_variable(cond_tokens)
        
        self.match(")", "delimitador")
        
        # Procesar el bloque y capturar sus tokens.
        start_block = self.pos
        self.block()
        block_tokens = self.tokens[start_block:self.pos]
        
        # Verificar que la variable de control se actualice en el bloque.
        if control_var and not self.check_while_update(control_var, block_tokens):
            self.error("Error semántico (while): La variable de control '" + control_var + "' no se actualiza en el bloque, posible loop infinito.")
        
        print("Sentencia 'while' analizada.")


    def while_condition(self):
        """
        Procesa y valida la condición del while.
        Verifica que la expresión consumida no esté vacía y,
        si se utiliza un operador relacional (por ejemplo, '<', '>', etc.),
        que éste tenga un operando a continuación.
        """
        start_pos = self.pos
        self.expression()  # Se consume la expresión de la condición.
        cond_tokens = self.tokens[start_pos:self.pos]

        if not cond_tokens:
            self.error("Error semántico (while): La condición está vacía.")
            return

        # Lista de operadores relacionales válidos.
        relational_ops = {"<", ">", "<=", ">=", "==", "!="}
        
        # Recorre los tokens para detectar un operador relacional y validar que tenga operando.
        for idx, token in enumerate(cond_tokens):
            if token[0] in relational_ops and token[1] == "operador":
                # Si el operador es el último token, falta operando.
                if idx == len(cond_tokens) - 1:
                    self.error("Error semántico (while): Falta un operando después del operador relacional.")
                else:
                    siguiente = cond_tokens[idx + 1]
                    if siguiente[1] not in ("variable", "número", "cadena"):
                        self.error("Error semántico (while): Operador relacional sin operando válido.")
                break  # Se asume que solo hay una comparación.


    def extract_control_variable(self, tokens):
        """
        Extrae heurísticamente la primera variable encontrada en los tokens
        (se supone que esa será la variable de control).
        """
        for token in tokens:
            if token[1] == "variable":
                return token[0]
        return None


    def check_while_update(self, control_var, tokens):
        """
        Recorre la lista de tokens del bloque y busca patrones de actualización
        de la variable de control.
        Se consideran válidos:
        - Post-incremento o post-decremento: variable seguida de '++' o '--'.
        - Incremento cuando la tokenización separa los dos signos: 
            (variable, "+", "+") o (variable, "-", "-").
        - Asignación acumulativa: variable seguida de '+=' o '-=' y un valor.
        Retorna True si se detecta la actualización, False en caso contrario.
        """
        for idx, token in enumerate(tokens):
            if token[0] == control_var and token[1] == "variable":
                # Caso 1: Incremento postfijo en 2 tokens.
                if idx + 1 < len(tokens):
                    next_token = tokens[idx + 1]
                    if next_token[0] in {"++", "--"} and next_token[1] == "operador":
                        return True
                # Caso 2: Incremento postfijo cuando se tokeniza en 3 tokens: variable, "+" y "+" o "-" y "-".
                if idx + 2 < len(tokens):
                    t1 = tokens[idx + 1]
                    t2 = tokens[idx + 2]
                    if (t1[0] == "+" and t1[1] == "operador" and 
                        t2[0] == "+" and t2[1] == "operador"):
                        return True
                    if (t1[0] == "-" and t1[1] == "operador" and 
                        t2[0] == "-" and t2[1] == "operador"):
                        return True
                    # Caso 3: Asignación acumulativa: variable, "+=" o "-=" y un valor.
                    if (t1[0] in {"+=", "-="} and t1[1] == "operador" and
                        t2[1] in {"variable", "número", "cadena"}):
                        return True
        return False


    def show_errors(self):
        """Muestra los errores sintácticos encontrados."""
        if self.errors:
            print("\n=== ERRORES SINTÁCTICOS ===")
            for err in self.errors:
                print(err)
        else:
            print("No se encontraron errores sintácticos.")