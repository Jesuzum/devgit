operadores = ['+', '-', '*', '/', '%', '^']

class arbolParseo:
    def _init_(self, expresionInicial):
        #self.niveles = [] # Lista de listas
        self.valor = expresionInicial
        self.raiz = Nodo() # nodo inicial
        self.niveles = 0
        self.construirArbol()
        
    
    def construirArbol(self):
        stack = []
        stack.append(self.raiz)
        num = ''
        curr_nivel = 0
        for caracter in self.valor:
            nodo_actual = stack[-1]
            if not caracter.isnumeric():
                if(num != ''):
                    nodo_actual.hijos.append(Nodo(valor=num))
                    num = ''
            if(caracter == '('):
                curr_nivel += 1
                nodo_actual.hijos.append(Nodo())
                stack.append(nodo_actual.hijos[-1])
            elif(caracter == ')'):
                curr_nivel -= 1
                stack.pop()
            elif caracter in operadores:
                nodo_actual.hijos.append(Nodo(valor=caracter))
            else:
                num += caracter
            self.niveles = max(self.niveles, curr_nivel)
        if(num != ''):
            nodo_actual.hijos.append(Nodo(valor=num))


    def imprimirArbol(self):
        tmp = self.raiz.hijos.copy()
        print(self.niveles)
        for n in range(self.niveles + 1):
            i = 0
            #tmp_2 = tmp.copy()
            while i < len(tmp):
                if tmp[i].valor == None:
                    print("<exp>", end="")
                    hijos = tmp[i].hijos
                    tmp.pop(i)  # Eliminamos el nodo actual
                    tmp[i:i] = hijos  # Insertamos sus hijos en su lugar
                    i += len(hijos)
                else:
                    if(tmp[i].valor.isnumeric()):
                        print("<num>", end="")
                    else:
                        print("<op>", end="")
                    i += 1
            print()
    


class Nodo:
    def _init_(self, valor = None):
        self.valor = valor
        self.hijos = []