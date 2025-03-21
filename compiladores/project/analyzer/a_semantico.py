class AnalizadorSemantico:
    def __init__(self):
        self.tabla_simbolos = {}  # Variables globales y su tipo
        self.funciones = {}  # Funciones con sus parámetros
        self.errores = []  # Lista de errores encontrados

    def agregar_variable(self, nombre, tipo):
        """Registra una variable en la tabla de símbolos."""
        if nombre in self.tabla_simbolos:
            self.errores.append(f"Error: La variable '{nombre}' ya está declarada.")
        else:
            self.tabla_simbolos[nombre] = tipo

    def validar_variable(self, nombre):
        """Verifica si una variable ha sido declarada antes de usarse."""
        if nombre not in self.tabla_simbolos:
            self.errores.append(f"Error: La variable '{nombre}' no está declarada.")

    def agregar_funcion(self, nombre, parametros):
        """Registra una función con su lista de parámetros."""
        if nombre in self.funciones:
            self.errores.append(f"Error: La función '{nombre}' ya está declarada.")
        else:
            self.funciones[nombre] = parametros
            # Registrar parámetros como variables locales
            for param in parametros:
                self.agregar_variable(param, "desconocido")

    def validar_llamada_funcion(self, nombre, argumentos):
        """Verifica que una función exista y tenga el número correcto de argumentos."""
        if nombre not in self.funciones:
            self.errores.append(f"Error: La función '{nombre}' no está declarada.")
            return

        parametros = self.funciones[nombre]
        if len(argumentos) != len(parametros):
            self.errores.append(f"Error: La función '{nombre}' esperaba {len(parametros)} argumentos, pero recibió {len(argumentos)}.")

    def analizar(self, tokens):
        """
        Recorre la lista de tokens generada por el analizador léxico
        y realiza validaciones semánticas en Perl.
        """
        i = 0
        while i < len(tokens):
            token = tokens[i]

            #  Declaración de variables con 'my'
            if token == "my":
                if i + 1 < len(tokens) and tokens[i + 1].startswith(("$", "@", "%")):
                    nombre_variable = tokens[i + 1]
                    self.agregar_variable(nombre_variable, "desconocido")
                    i += 2  # Saltamos 'my' y la variable
                else:
                    self.errores.append("Error: Se esperaba un nombre de variable después de 'my'.")

            #  Uso de variables
            elif token.startswith(("$", "@", "%")):
                self.validar_variable(token)

            #  Definición de funciónc
            elif token == "sub":
                if i + 1 < len(tokens):
                    nombre_funcion = tokens[i + 1]  # El siguiente token debe ser el nombre de la función
                    parametros = []
                    i += 2  # Saltamos sub nombre_funcion {

                    # Buscar parámetros en my ($var1, $var2) = @_;
                    while i < len(tokens) and tokens[i] != "}":
                        if tokens[i] == "my" and i + 1 < len(tokens) and tokens[i + 1].startswith("("):
                            i += 2  # Saltamos my (
                            while i < len(tokens) and tokens[i] != ")":
                                if tokens[i].startswith("$"):
                                    parametros.append(tokens[i])
                                i += 1  # Avanzamos hasta )
                        i += 1  # Continuamos avanzando en el bloque de la función

                    self.agregar_funcion(nombre_funcion, parametros)

                else:
                    self.errores.append("Error: Se esperaba un nombre de función después de 'sub'.")

            #  Llamada a función
            elif i + 1 < len(tokens) and tokens[i + 1] == "(":
                nombre_funcion = token
                argumentos = []
                i += 2  # Saltamos '('

                while i < len(tokens) and tokens[i] != ")":
                    if tokens[i].startswith("$"):
                        argumentos.append(tokens[i])
                    i += 1

                self.validar_llamada_funcion(nombre_funcion, argumentos)

            i += 1  # Avanzar

    def mostrar_errores(self):
        """Muestra los errores semánticos detectados."""
        if self.errores:
            print("\n=== ERRORES SEMÁNTICOS ===")
            for error in self.errores:
                print(error)
        else:
            print("Análisis semántico completado sin errores.")


# Simulación de tokens generados por el analizador léxico
tokens_sin_errores = [
    "use", "strict", ";", "use", "warnings", ";",
    "my", "$nombre", "=", '"Carlos"', ";",
    "my", "$salario", "=", "50000", ";",
    "my", "$bono", "=", "5000", ";",
    "sub", "calcular_salario_final", "{",
    "my", "(", "$base", ",", "$extra", ")", "=", "@_;",
    "return", "$base", "+", "$extra", ";",
    "}",
    "my", "$salario_final", "=", "calcular_salario_final", "(", "$salario", ",", "$bono", ")", ";",
    "print", '"Empleado: "', "$nombre", ";",
    "print", '"Salario final: "', "$salario_final", ";"
]

# Simulación de tokens generados por el analizador léxico con errores semánticos
tokens_con_errores = [
    "use", "strict", ";", "use", "warnings", ";",
    "my", "$nombre", "=", '"Carlos"', ";",
    "my", "$salario", "=", "50000", ";",
    "my", "$bono", "=", "5000", ";",
    "my", "$nombre", "=", '"Pedro"', ";",  #  ERROR: '$nombre' ya fue declarado
    "sub", "calcular_salario_final", "{",
    "my", "(", "$base", ",", "$extra", ")", "=", "@_;",
    "return", "$base", "+", "$extra", ";",
    "}",
    "my", "$salario_final", "=", "calcular_salario_final", "(", "$salario", ")", ";",  #  ERROR: Falta un argumento
    "my", "$impuesto", "=", "calcular_impuestos", "(", "$salario_final", ")", ";",  #  ERROR: Función no declarada
    "my", "$total", "=", "$salario_final", "-", "$descuento", ";",  #  ERROR: '$descuento' no fue declarado
    "print", '"Empleado: "', "$nombre", ";",
    "print", '"Salario final: "', "$total", ";"
]

# Ejecutar análisis semántico con tokens con errores
analizador = AnalizadorSemantico()
analizador.analizar(tokens_sin_errores)
analizador.mostrar_errores()