operadores = ['+', '-', '*', '/', '%', '^']

class Nodo:
    def __init__(self, valor=None):
        self.valor = valor
        self.hijos = []

class arbolParseo:
    def __init__(self, expresionInicial):
        self.valor = expresionInicial
        self.raiz = Nodo()  # Nodo raíz del árbol
        self.niveles = 0
        self.construirArbol()
        
    def construirArbol(self):
        stack = [self.raiz]
        num = ''
        curr_nivel = 0

        for caracter in self.valor:
            nodo_actual = stack[-1]
            if caracter.isnumeric():
                num += caracter  # Acumular número si es dígito
            else:
                if num:
                    nodo_actual.hijos.append(Nodo(valor=num))
                    num = ''
                    
                if caracter == '(':
                    curr_nivel += 1
                    nuevo_nodo = Nodo()
                    nodo_actual.hijos.append(nuevo_nodo)
                    stack.append(nuevo_nodo)
                elif caracter == ')':
                    curr_nivel -= 1
                    if stack:
                        stack.pop()
                elif caracter in operadores:
                    nodo_actual.hijos.append(Nodo(valor=caracter))

            self.niveles = max(self.niveles, curr_nivel)
        
        if num:
            stack[-1].hijos.append(Nodo(valor=num))  # Agregar número al último nodo
        
    def imprimirArbol(self):
        tmp = self.raiz.hijos.copy()
        print("Niveles:", self.niveles)

        for _ in range(self.niveles + 1):
            i = 0
            while i < len(tmp):
                nodo = tmp[i]
                if nodo.valor is None:
                    print("<exp>", end=" ")
                    hijos = nodo.hijos
                    tmp.pop(i)  
                    tmp[i:i] = hijos  
                    i += len(hijos)
                else:
                    if str(nodo.valor).isnumeric():
                        print("<num>", end=" ")
                    else:
                        print("<op>", end=" ")
                    i += 1
            print()

# Ejemplo de uso
expresion = "((3+5)*(2-4))"
arbol = arbolParseo(expresion)
arbol.imprimirArbol()
