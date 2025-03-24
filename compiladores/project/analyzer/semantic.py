from .pr import *  # Se importan listas como palabras_reservadas, funciones_incorporadas, etc.

class AnalizadorSemantico:
    def __init__(self):
        # La pila de ámbitos: el primer ámbito es el global.
        self.scope_stack = [{}]
        # Tabla de funciones global: nombre de función -> lista de parámetros.
        self.funciones = {}
        # Lista de errores semánticos encontrados.
        self.errores = []

    # --- Manejo de ámbitos ---
    def push_scope(self):
        self.scope_stack.append({})

    def pop_scope(self):
        # Evitamos desapilar el ámbito global.
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
        else:
            self.errores.append("Error interno: no se puede desapilar el ámbito global.")

    def agregar_variable(self, nombre, tipo):
        """Agrega la variable al ámbito actual; si ya existe, registra un error."""
        current_scope = self.scope_stack[-1]
        if nombre in current_scope:
            self.errores.append(f"Error: la variable '{nombre}' ya está declarada en el ámbito actual.")
        else:
            current_scope[nombre] = tipo

    def buscar_variable(self, nombre):
        """Busca la variable en la pila de ámbitos (desde lo local a lo global)."""
        for scope in reversed(self.scope_stack):
            if nombre in scope:
                return True
        return False

    def validar_variable(self, nombre):
        """Verifica que la variable esté declarada en algún ámbito."""
        if not self.buscar_variable(nombre):
            self.errores.append(f"Error: la variable '{nombre}' no está declarada.")

    def agregar_funcion(self, nombre, parametros):
        """Registra la función globalmente; si ya existe, registra un error."""
        if nombre in self.funciones:
            self.errores.append(f"Error: la función '{nombre}' ya está declarada.")
        else:
            self.funciones[nombre] = parametros
            # NOTA: No agregamos los parámetros al ámbito global.

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
        Recorre la lista de tokens (tuplas de (valor, tipo)) y realiza validaciones semánticas:
          - Declaración y uso de variables.
          - Definición de funciones y extracción de parámetros.
          - Llamadas a funciones.
        """
        i = 0
        n = len(tokens)
        while i < n:
            valor, tipo = tokens[i]
            # Declaración de variable: "my"
            if valor == "my" and tipo == "palabra reservada":
                if i + 1 < n:
                    next_valor, next_tipo = tokens[i+1]
                    # Caso: declaración de lista, e.g. my ( $a, $b, ... )
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
                    # Caso: declaración individual
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

            # Uso de variable: cualquier token de tipo "variable" se verifica en la pila de ámbitos
            elif tipo == "variable":
                self.validar_variable(valor)
                i += 1

            # Definición de función: "sub" seguido de nombre y bloque
            elif valor == "sub" and tipo == "palabra reservada":
                if i + 1 < n:
                    func_valor, func_tipo = tokens[i+1]
                    if func_tipo == "nombre de función":
                        nombre_funcion = func_valor
                        i += 2  # Saltar "sub" y el nombre de la función
                    else:
                        self.errores.append("Error semántico: se esperaba el nombre de la función después de 'sub'.")
                        i += 1
                        continue
                else:
                    self.errores.append("Error semántico: se esperaba el nombre de la función después de 'sub'.")
                    i += 1
                    continue

                # Se espera el bloque de la función delimitado por '{' y '}'
                parametros = []
                if i < n and tokens[i][0] == "{" and tokens[i][1] == "delimitador":
                    i += 1  # Saltar '{'
                    self.push_scope()  # Nuevo ámbito local para la función
                    # Búsqueda de posibles parámetros declarados con el patrón:
                    # my ( $param1, $param2, ... ) = @_;
                    while i < n and not (tokens[i][0] == "}" and tokens[i][1] == "delimitador"):
                        curr_val, curr_tipo = tokens[i]
                        if curr_val == "my" and curr_tipo == "palabra reservada":
                            if i + 1 < n:
                                nxt_val, nxt_tipo = tokens[i+1]
                                if nxt_val == "(" and nxt_tipo == "delimitador":
                                    i += 2  # Saltar "my" y "("
                                    while i < n and not (tokens[i][0] == ")" and tokens[i][1] == "delimitador"):
                                        if tokens[i][1] == "variable":
                                            param = tokens[i][0]
                                            self.agregar_variable(param, "desconocido")  # Solo en el ámbito local
                                            parametros.append(param)
                                        i += 1
                                    i += 1  # Saltar ')'
                                    # Omitir el posible segmento de asignación (por ejemplo, "= @_;") hasta el ';'
                                    while i < n and tokens[i][0] != ";":
                                        i += 1
                                    if i < n and tokens[i][0] == ";":
                                        i += 1
                                else:
                                    i += 1
                            else:
                                i += 1
                        else:
                            i += 1
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

            # Llamada a función: identificada si el token está clasificado como "llamada a función"
            # o si el siguiente token es "(".
            elif (tipo == "llamada a función") or (i+1 < n and tokens[i+1][0] == "(" and tokens[i+1][1] == "delimitador"):
                nombre_funcion = valor
                argumentos = []
                if i+1 < n and tokens[i+1][0] == "(" and tokens[i+1][1] == "delimitador":
                    i += 2  # Saltamos el nombre y el token '('
                    while i < n and not (tokens[i][0] == ")" and tokens[i][1] == "delimitador"):
                        if tokens[i][1] == "variable":
                            argumentos.append(tokens[i][0])
                        i += 1
                    if i < n and tokens[i][0] == ")" and tokens[i][1] == "delimitador":
                        i += 1  # Saltar ')'
                else:
                    i += 1
                    if i < n and tokens[i][1] == "variable":
                        argumentos.append(tokens[i][0])
                        i += 1
                self.validar_llamada_funcion(nombre_funcion, argumentos)

            else:
                i += 1

    def mostrar_errores(self):
        if self.errores:
            print("\n=== ERRORES SEMÁNTICOS ===")
            for error in self.errores:
                print(error)
        else:
            print("Análisis semántico completado sin errores.")