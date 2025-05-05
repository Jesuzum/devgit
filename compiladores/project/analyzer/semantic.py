from .pr import *  # Se importan listas como palabras_reservadas, funciones_incorporadas, etc.

class AnalizadorSemantico:
    def __init__(self):
        # La pila de ámbitos: el primer ámbito es el global.
        self.scope_stack = [{}]
        # Tabla de funciones global: nombre de función -> lista de parámetros.
        self.funciones = {}
        # Lista de errores semánticos encontrados.
        self.errores = []

    # --- Manejo de Ámbitos ---
    def push_scope(self):
        self.scope_stack.append({})

    def pop_scope(self):
        # Evitamos desapilar el ámbito global.
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
        else:
            self.errores.append("Error interno: no se puede desapilar el ámbito global.")

    # --- Gestión de Variables ---
    def agregar_variable(self, nombre, tipo):
        """Agrega la variable al ámbito actual; si ya existe, registra un error."""
        current_scope = self.scope_stack[-1]
        if nombre in current_scope:
            self.errores.append(f"Error: la variable '{nombre}' ya está declarada en el ámbito actual.")
        else:
            current_scope[nombre] = tipo

    def buscar_variable(self, nombre):
        """Busca la variable en la pila de ámbitos (de lo local a lo global)."""
        for scope in reversed(self.scope_stack):
            if nombre in scope:
                return True
        return False

    def validar_variable(self, nombre):
        """Verifica que la variable esté declarada en algún ámbito."""
        if not self.buscar_variable(nombre):
            self.errores.append(f"Error: la variable '{nombre}' no está declarada.")

    # --- Gestión de Funciones ---
    def agregar_funcion(self, nombre, parametros):
        """Registra la función globalmente; si ya existe, registra un error."""
        if nombre in self.funciones:
            self.errores.append(f"Error: la función '{nombre}' ya está declarada.")
        else:
            self.funciones[nombre] = parametros
            # Nota: Los parámetros se manejan en el ámbito local de la función.

    def validar_llamada_funcion(self, nombre, argumentos):
        """Valida que la función esté declarada y que el número de argumentos concuerde con los parámetros."""
        if nombre not in self.funciones:
            self.errores.append(f"Error: la función '{nombre}' no está declarada.")
            return
        parametros = self.funciones[nombre]
        if len(argumentos) != len(parametros):
            self.errores.append(
                f"Error: la función '{nombre}' esperaba {len(parametros)} argumentos, pero recibió {len(argumentos)}."
            )

    # --- Análisis Semántico ---
    def analizar(self, tokens):
        """
        Recorre la lista de tokens y realiza las validaciones semánticas:
          - Declaración y uso de variables.
          - Definición de funciones (y extracción de parámetros).
          - Llamadas a funciones.
          - Estructuras condicionales (if / elsif / else).
        """
        i = 0
        n = len(tokens)
        while i < n:
            valor, tipo = tokens[i]
            if valor == "my" and tipo == "palabra reservada":
                # Declaración de variable o lista.
                if i + 1 < n:
                    next_valor, next_tipo = tokens[i+1]
                    if next_valor == "(" and next_tipo == "delimitador":
                        i += 2  # Saltar "my" y "("
                        vars_lista = []
                        while i < n and not (tokens[i][0] == ")" and tokens[i][1] == "delimitador"):
                            if tokens[i][1] == "variable":
                                vars_lista.append(tokens[i][0])
                            i += 1
                        i += 1  # Saltar ")"
                        for var in vars_lista:
                            self.agregar_variable(var, "desconocido")
                    elif next_tipo == "variable":
                        self.agregar_variable(next_valor, "desconocido")
                        i += 2
                    else:
                        self.errores.append("Error semántico: se esperaba un nombre de variable o lista de variables después de 'my'.")
                        i += 1
                        continue
                else:
                    self.errores.append("Error semántico: se esperaba un nombre de variable después de 'my'.")
                    i += 1
                    continue
                print("Análisis semántico: Declaración analizada.")

            elif valor == "sub" and tipo == "palabra reservada":
                # Definición de función.
                if i + 1 < n:
                    func_valor, func_tipo = tokens[i+1]
                    if func_tipo == "nombre de función":
                        nombre_funcion = func_valor
                        i += 2  # Saltar "sub" y el nombre de la función.
                    else:
                        self.errores.append("Error semántico: se esperaba el nombre de la función después de 'sub'.")
                        i += 1
                        continue
                else:
                    self.errores.append("Error semántico: se esperaba el nombre de la función después de 'sub'.")
                    i += 1
                    continue
            
                # Se espera el bloque de la función: { ... }
                parametros = []
                if i < n and tokens[i][0] == "{" and tokens[i][1] == "delimitador":
                    i += 1  # Saltar '{'
                    self.push_scope()  # Nuevo ámbito local
                    parametros, i = self._extraer_parametros(tokens, i)
                    if i < n and tokens[i][0] == "}" and tokens[i][1] == "delimitador":
                        i += 1  # Saltar '}'
                    else:
                        self.errores.append("Error semántico: se esperaba '}' para cerrar el bloque de la función.")
                    self.pop_scope()  # Fin del ámbito local
                else:
                    self.errores.append("Error semántico: se esperaba un bloque '{' después de la definición de la función.")
                    i += 1
                    continue

                self.agregar_funcion(nombre_funcion, parametros)
                print("Análisis semántico: Definición de función analizada.")

            elif valor == "while" and tipo == "palabra reservada":
                i = self._analizar_while(tokens, i)
                continue

            elif valor == "for" and tipo == "FOR":
                i = self._analizar_for(tokens, i)
                continue
            # Primero procesamos estructuras condicionales antes que llamadas a función.
            elif valor == "if" and tipo == "IF":
                # Procesa la estructura condicional (if/elsif/else)
                i = self._analizar_condicional(tokens, i)
                # Los mensajes correspondientes se muestran dentro de _analizar_condicional.
            elif valor in ("elsif", "else") and tipo in ("ELSIF", "ELSE"):
                self.errores.append("Error semántico: 'elsif' o 'else' sin que preceda un 'if'.")
                i += 1
            # Despues procesamos la sentencia switch.
            elif valor == "switch" and tipo == "SWITCH":
                i = self._analizar_switch(tokens, i)

            # Luego, procesamos llamadas a función.
            elif (tipo == "llamada a función") or (i+1 < n and tokens[i+1][0] == "(" and tokens[i+1][1] == "delimitador"):
                nombre_funcion = valor
                # Agregamos una condición para omitir palabras reservadas que no deben ser validadas como funciones.
                if nombre_funcion in ["for", "if", "elsif", "else", "switch", "case", "default", "sub", "return"]:
                    # Si se trata de una palabra reservada de control, simplemente saltamos su validación semántica.
                    i += 1
                    print(f"Análisis semántico: Estructura de control '{nombre_funcion}' analizada.")
                else:
                    argumentos = []
                    if i+1 < n and tokens[i+1][0] == "(" and tokens[i+1][1] == "delimitador":
                        i += 2  # Saltamos nombre y "(".
                        while i < n and not (tokens[i][0] == ")" and tokens[i][1] == "delimitador"):
                            if tokens[i][1] in ("variable", "número", "cadena"):
                                argumentos.append(tokens[i][0])
                            i += 1
                        if i < n and tokens[i][0] == ")" and tokens[i][1] == "delimitador":
                            i += 1  # Saltamos ')'
                    else:
                        i += 1
                        if i < n and tokens[i][1] in ("variable", "número", "cadena"):
                            argumentos.append(tokens[i][0])
                            i += 1
                    self.validar_llamada_funcion(nombre_funcion, argumentos)
                    print("Análisis semántico: Llamada a función analizada.")

            elif tipo == "variable":
                # Uso de variable.
                self.validar_variable(valor)
                i += 1
                print("Análisis semántico: Uso de variable analizada.")

            else:
                i += 1

        if not self.errores:
            print("Análisis semántico completado sin errores.")
        else:
            print("Análisis semántico completado con errores.")

    def _extraer_parametros(self, tokens, i):
        """
        Extrae parámetros en el patrón: my ( $param1, $param2, ... ) = @_; 
        Retorna una tupla (lista_de_parametros, nuevo_indice).
        Se espera que se haya consumido ya el token '{' de apertura.
        """
        parametros = []
        n = len(tokens)
        while i < n:
            if tokens[i][0] == "}" and tokens[i][1] == "delimitador":
                break
            # Se busca el patrón "my ( ... )"
            if tokens[i][0] == "my" and tokens[i][1] == "palabra reservada":
                if i+1 < n and tokens[i+1][0] == "(" and tokens[i+1][1] == "delimitador":
                    i += 2  # Saltar los tokens "my" y "("
                    while i < n and not (tokens[i][0] == ")" and tokens[i][1] == "delimitador"):
                        if tokens[i][1] == "variable":
                            param = tokens[i][0]
                            self.agregar_variable(param, "desconocido")  # Se agrega solo al ámbito local.
                            parametros.append(param)
                        i += 1
                    i += 1  # Saltar el token ')'
                    # Saltar tokens hasta llegar a ';'
                    while i < n and tokens[i][0] != ";":
                        i += 1
                    if i < n and tokens[i][0] == ";":
                        i += 1
                    continue
            i += 1
        return (parametros, i)

    def _skip_block(self, tokens, i):
        """
        Avanza el índice 'i' hasta después del bloque delimitado por '{' y '}'.
        Utiliza un contador de niveles de anidamiento.
        """
        depth = 0
        n = len(tokens)
        while i < n:
            if tokens[i][0] == "{" and tokens[i][1] == "delimitador":
                depth += 1
            elif tokens[i][0] == "}" and tokens[i][1] == "delimitador":
                depth -= 1
                if depth == 0:
                    return i + 1
            i += 1
        self.errores.append("Error semántico: bloque no cerrado correctamente.")
        return i

    def _analizar_condicional(self, tokens, i):
        """
        Procesa la estructura condicional:
          if (condición) { bloque }
          [elsif (condición) { bloque }]* 
          [else { bloque }]
        Retorna el nuevo índice después del condicional.
        Durante la condición se valida el uso de variables.
        """
        n = len(tokens)
        # Se espera que tokens[i] sea "if" de tipo IF.
        i += 1  # Saltar "if"
        # Validar que siga '('
        if i < n and tokens[i][0] == "(" and tokens[i][1] == "delimitador":
            i += 1
            # Procesar la condición: validar variables dentro.
            while i < n and not (tokens[i][0] == ")" and tokens[i][1] == "delimitador"):
                if tokens[i][1] == "variable":
                    self.validar_variable(tokens[i][0])
                i += 1
            if i < n and tokens[i][0] == ")" and tokens[i][1] == "delimitador":
                i += 1  # Saltar ')'
            else:
                self.errores.append("Error semántico: se esperaba ')' en la condición del if.")
        else:
            self.errores.append("Error semántico: se esperaba '(' después de 'if'.")
        # Procesar el bloque del if.
        if i < n and tokens[i][0] == "{" and tokens[i][1] == "delimitador":
            i = self._skip_block(tokens, i)
        else:
            self.errores.append("Error semántico: se esperaba bloque '{' tras el if.")
        print("Análisis semántico: Sentencia 'if' analizada.")

        # Procesar cero o más 'elsif'
        while i < n and tokens[i][1] == "ELSIF":
            i += 1  # Saltar 'elsif'
            if i < n and tokens[i][0] == "(" and tokens[i][1] == "delimitador":
                i += 1
                while i < n and not (tokens[i][0] == ")" and tokens[i][1] == "delimitador"):
                    if tokens[i][1] == "variable":
                        self.validar_variable(tokens[i][0])
                    i += 1
                if i < n and tokens[i][0] == ")" and tokens[i][1] == "delimitador":
                    i += 1
                else:
                    self.errores.append("Error semántico: se esperaba ')' en la condición del elsif.")
            else:
                self.errores.append("Error semántico: se esperaba '(' después de 'elsif'.")
            if i < n and tokens[i][0] == "{" and tokens[i][1] == "delimitador":
                i = self._skip_block(tokens, i)
            else:
                self.errores.append("Error semántico: se esperaba bloque '{' tras el elsif.")
            print("Análisis semántico: Sentencia 'elsif' analizada.")

        # Procesar opcional 'else'
        if i < n and tokens[i][1] == "ELSE":
            i += 1  # Saltar 'else'
            if i < n and tokens[i][0] == "{" and tokens[i][1] == "delimitador":
                i = self._skip_block(tokens, i)
            else:
                self.errores.append("Error semántico: se esperaba bloque '{' tras el else.")
            print("Análisis semántico: Sentencia 'else' analizada.")
        return i

    def _analizar_switch(self, tokens, i):
        """
        Procesa la estructura switch:
        switch ( expresión ) {
            { case_clause }*
            [ default_clause ]
        }
        Retorna el nuevo índice después del switch.
        Durante la evaluación se validan las variables en la expresión y en cada caso.
        """
        n = len(tokens)
        # Se asume que tokens[i] es "switch" de tipo SWITCH.
        i += 1  # Saltar "switch"
        
        # Validar la expresión entre paréntesis.
        if i < n and tokens[i][0] == "(" and tokens[i][1] == "delimitador":
            i += 1  # Saltar '('
            # Validar que exista una variable y nada más dentro de los paréntesis:
            if i < n and tokens[i][1] == "variable":
                self.validar_variable(tokens[i][0])
                i += 1  # Procesamos la variable
                # Después de la variable, esperamos de inmediato el token de cierre ')'
                if i < n and tokens[i][0] == ")" and tokens[i][1] == "delimitador":
                    i += 1  # Saltar ')'
                else:
                    self.errores.append("Error semántico: se esperaba ')' después de la variable en switch().")
            else:
                self.errores.append("Error semántico: se esperaba una variable dentro de switch().")
                # Buscamos saltar tokens hasta encontrar el token de cierre para sincronizar
                while i < n and not (tokens[i][0] == ")" and tokens[i][1] == "delimitador"):
                    i += 1
                if i < n:
                    i += 1  # Saltar ')'
        else:
            self.errores.append("Error semántico: se esperaba '(' después de 'switch'.")
        
        # Se espera el bloque de apertura '{'
        if i < n and tokens[i][0] == "{" and tokens[i][1] == "delimitador":
            i += 1  # Saltar '{'
        else:
            self.errores.append("Error semántico: se esperaba '{' tras la expresión switch.")
        
        # Procesar cero o más cláusulas case.
        while i < n and tokens[i][0] == "case" and tokens[i][1] == "CASE":
            i = self._analizar_case_clause(tokens, i)
        
        # Procesar opcional cláusula default.
        if i < n and tokens[i][0] == "default" and tokens[i][1] == "DEFAULT":
            i = self._analizar_default_clause(tokens, i)
        
        # Se espera la llave de cierre '}'.
        if i < n and tokens[i][0] == "}" and tokens[i][1] == "delimitador":
            i += 1
        else:
            self.errores.append("Error semántico: se esperaba '}' para cerrar el switch.")
        
        print("Análisis semántico: Sentencia 'switch' analizada.")
        return i

    
    def _analizar_case_clause(self, tokens, i):
        """
        Procesa una cláusula case:
        case expresión : { bloque }
        Retorna el nuevo índice después del case.
        """
        n = len(tokens)
        # Se asume que tokens[i] es "case" de tipo CASE.
        i += 1  # Saltar "case"
        
        # Procesar la expresión del case.
        while i < n and not (tokens[i][0] == ":" and tokens[i][1] == "delimitador"):
            if tokens[i][1] == "variable":
                self.validar_variable(tokens[i][0])
            i += 1
        if i < n and tokens[i][0] == ":" and tokens[i][1] == "delimitador":
            i += 1  # Saltar ':'
        else:
            self.errores.append("Error semántico: se esperaba ':' tras la expresión del case.")
        
        # Se espera el bloque que inicia con '{'
        if i < n and tokens[i][0] == "{" and tokens[i][1] == "delimitador":
            i = self._skip_block(tokens, i)
        else:
            self.errores.append("Error semántico: se esperaba bloque '{' en el case.")
        
        print("Análisis semántico: Sentencia 'case' analizada.")
        return i
    
    def _analizar_default_clause(self, tokens, i):
        """
        Procesa la cláusula default:
        default : { bloque }
        Retorna el nuevo índice después de default.
        """
        n = len(tokens)
        # Se asume que tokens[i] es "default" de tipo DEFAULT.
        i += 1  # Saltar "default"
        
        if i < n and tokens[i][0] == ":" and tokens[i][1] == "delimitador":
            i += 1  # Saltar ':'
        else:
            self.errores.append("Error semántico: se esperaba ':' tras 'default'.")
        
        if i < n and tokens[i][0] == "{" and tokens[i][1] == "delimitador":
            i = self._skip_block(tokens, i)
        else:
            self.errores.append("Error semántico: se esperaba bloque '{' tras 'default'.")
        
        print("Análisis semántico: Sentencia 'default' analizada.")
        return i
    
    def _analizar_for(self, tokens, i):
        """
        Analiza semánticamente el ciclo for (estilo Perl). Se admiten dos formas:

        1) For clásico:
        for ( inicialización ; condición ; incremento ) { bloque }
        2) For iterativo:
        for VARIABLE ( lista ) { bloque }

        Retorna el nuevo índice tras analizar la estructura.
        """
        n = len(tokens)
        # Se asume que tokens[i] es ("for", "FOR")
        i += 1

        # --- Forma clásica:
        if i < n and tokens[i][0] == "(" and tokens[i][1] == "delimitador":
            i += 1  # Saltar "("
            init_tokens, cond_tokens, incr_tokens = [], [], []
            current_section = init_tokens

            # Recorremos la cabecera hasta encontrar el ')' que cierra la parte entre paréntesis.
            while i < n and not (tokens[i][0] == ")" and tokens[i][1] == "delimitador"):
                if tokens[i][0] == ";" and tokens[i][1] == "delimitador":
                    if current_section is init_tokens:
                        current_section = cond_tokens
                    elif current_section is cond_tokens:
                        current_section = incr_tokens
                    else:
                        self.errores.append("Error semántico (for clásico): Demasiados ';'.")
                    i += 1
                else:
                    current_section.append(tokens[i])
                    i += 1

            if i < n and tokens[i][0] == ")" and tokens[i][1] == "delimitador":
                i += 1  # Saltar ")"
            else:
                self.errores.append("Error semántico (for clásico): Falta ')' en la cabecera.")
                
            # Validar la sección de inicialización.
            if not init_tokens:
                self.errores.append("Error semántico (for clásico): La inicialización está vacía.")
            else:
                if not any(tok[0] == "=" and tok[1] == "operador" for tok in init_tokens):
                    self.errores.append("Error semántico (for clásico): La inicialización debe incluir '='.")
                
            # Validar la condición (por ejemplo, que contenga un operador relacional).
            relational_ops = {"<", ">", "<=", ">=", "==", "!="}
            if not cond_tokens:
                self.errores.append("Error semántico (for clásico): La condición está vacía.")
            else:
                if not any(tok[0] in relational_ops and tok[1] == "operador" for tok in cond_tokens):
                    self.errores.append("Error semántico (for clásico): La condición debe tener un operador relacional.")
                
            # Validar la expresión de incremento.
            if not incr_tokens:
                self.errores.append("Error semántico (for clásico): La expresión de incremento está vacía.")
            else:
                valid_incr = False
                # Opción 1: La expresión de incremento se reconoce en un solo token (por ejemplo, "++", "--", "+=", "-=" o "=").
                if len(incr_tokens) == 1 and incr_tokens[0][1] == "operador" and incr_tokens[0][0] in {"++", "--", "+=", "-=", "="}:
                    valid_incr = True
                # Opción 2: Patrón de post-incremento en tres tokens: variable, '+' y '+'.
                elif len(incr_tokens) == 3:
                    if (incr_tokens[0][1] == "variable" and
                        incr_tokens[1][0] == "+" and incr_tokens[1][1] == "operador" and
                        incr_tokens[2][0] == "+" and incr_tokens[2][1] == "operador"):
                        valid_incr = True
                if not valid_incr:
                    self.errores.append("Error semántico (for clásico): La expresión de incremento no es válida.")
                
            # Procesar el bloque que sigue (se espera que inicie con '{').
            if i < n and tokens[i][0] == "{" and tokens[i][1] == "delimitador":
                i = self._skip_block(tokens, i)
            else:
                self.errores.append("Error semántico (for clásico): Se esperaba '{' después de la cabecera.")
                
            print("Análisis semántico: ciclo for clásico analizado.")
            return i

        # --- Forma iterativa:
        elif i < n and (tokens[i][1] == "variable" or (tokens[i][1] == "llamada a función" and tokens[i][0].startswith('$'))):
            var_token = tokens[i]
            if var_token[1] == "llamada a función":
                var_token = (var_token[0], "variable")
            
            # Si la variable iteradora no existe, la agregamos al ámbito actual.
            if not self.buscar_variable(var_token[0]):
                self.agregar_variable(var_token[0], "iterador")
            
            i += 1
            # Se espera la lista de elementos entre paréntesis:
            if i < n and tokens[i][0] == "(" and tokens[i][1] == "delimitador":
                i += 1
                list_tokens = []
                while i < n and not (tokens[i][0] == ")" and tokens[i][1] == "delimitador"):
                    list_tokens.append(tokens[i])
                    i += 1
                if i < n and tokens[i][0] == ")" and tokens[i][1] == "delimitador":
                    i += 1  # Consumir ')'
                else:
                    self.errores.append("Error semántico (for iterativo): Falta ')' para cerrar la lista.")
                if not list_tokens:
                    self.errores.append("Error semántico (for iterativo): La lista está vacía.")
            else:
                self.errores.append("Error semántico (for iterativo): Se esperaba '(' después de la variable.")
                
            if i < n and tokens[i][0] == "{" and tokens[i][1] == "delimitador":
                i = self._skip_block(tokens, i)
            else:
                self.errores.append("Error semántico (for iterativo): Se esperaba '{' después del encabezado.")
                
            print("Análisis semántico: ciclo for iterativo analizado.")
            return i

        else:
            self.errores.append("Error semántico: Estructura for inválida.")
            return i

    def _analizar_while(self, tokens, i):
        """
        Analiza semánticamente la sentencia while.
        Sintaxis esperada:
        while ( condición ) { bloque }
        
        Retorna el nuevo índice después de procesar el while.
        """
        n = len(tokens)
        # Se asume que tokens[i] es ("while", "palabra reservada")
        i += 1  # Saltar "while"
        
        # Consumir el paréntesis de apertura
        if i < n and tokens[i][0] == "(" and tokens[i][1] == "delimitador":
            i += 1  # Saltar "("
        else:
            self.errores.append("Error semántico: se esperaba '(' después de 'while'.")
        
        # Procesar la condición
        while i < n and not (tokens[i][0] == ")" and tokens[i][1] == "delimitador"):
            # Validamos variables en la condición
            if tokens[i][1] == "variable":
                self.validar_variable(tokens[i][0])
            i += 1
        
        # Consumir el paréntesis de cierre
        if i < n and tokens[i][0] == ")" and tokens[i][1] == "delimitador":
            i += 1
        else:
            self.errores.append("Error semántico: se esperaba ')' para cerrar la condición del while.")
        
        # Procesar el bloque que inicia con '{'
        if i < n and tokens[i][0] == "{" and tokens[i][1] == "delimitador":
            i = self._skip_block(tokens, i)
        else:
            self.errores.append("Error semántico: se esperaba bloque '{' tras el while.")
        
        print("Análisis semántico: Sentencia 'while' analizada.")
        return i