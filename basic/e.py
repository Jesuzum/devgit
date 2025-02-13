"""
# Ejercicio 1
print ("Suma de dos numeros")
n1 = 5
n2 = 7
r = n1 + n2
print (r)

# Ejercicio 2
v1 = 7
v2 = 13
r = v1 + v2
print ("El resultado de la suma es:", r)

# Ejercicio 3
m = "En"
m1 = "abril"
m2 = "son"
m3 = "vacaciones"
m4 = " "
print(m + m4 + m1 + m4 + m2 + m4 + m3)

# Ejercicio 4
mensaje = "En abril son vacaciones"
subcad = mensaje[3:8]
print(subcad)

# Ejercicio 5
var = "Me gusta estudiar en UdeG"
subvar = var[3:8]
print(subvar)

# Ejercicio 6
var1 = "Me gusta estudiar en UdeG"
var2 = "Me gusta estudiar en UdeG"
print(var1 == var2)

# Ejercicio 7 
n1 = 13
n2 = 7

print(f"la suma de {n1} y {n2} es: {n1 + n2}")
print(f"la resta de {n1} y {n2} es: {n1 - n2}")
print(f"la multiplicacion de {n1} y {n2} es: {n1 * n2}")
print(f"la division de {n1} y {n2} es: {n1 / n2}")
print(f"el residuo de {n1} y {n2} es: {n1 % n2}")
print(f"la potencia de {n1} y {n2} es: {n1 ** n2}")
print(f"la division entera de {n1} y {n2} es: {n1 // n2}")j

# Ejercicio 8
lista = [1, 2, 3, "Python", True]
print(lista)
lista.append(4)  # Agrega un elemento al final de la lista
print(lista)
lista[0] = 10  # Modifica el primer elemento de la lista
print(lista)  # Salida: [10, 2, 3, 'Python', True, 4]

# Ejercicio 9
lista = [4, 5, "Clase", True, False]
lista.remove(5)
lista.pop()
del lista[0]
print(lista)

# Ejercicio 10
lista = [4, 5, "Clase", 6.7, True, False]
lista.append("Hola")
print(lista[0])

# Ejercicio 11
lista = [4, 5, "Clase", 6.7, True, False]
print(lista[1])
lista.append("Hola")
print(lista)

tupla = (4, 5, 'f', 3.14)
print(tupla[1])

# Ejercicio 12
diccionario = {
    "nombre": "Python",
    "año": 1991,
    "es_interesante": True
}

print(diccionario["nombre"])
print(diccionario["año"])
print(diccionario["es_interesante"])

diccionario["creador"] = "Guido van Rossum"
print(diccionario["creador"])
diccionario["nombre"] = "c"
print(diccionario)

# Ejercicio 13
name = input("What is your name?: ")
print("Hola! ", name)

# Ejercicio 14
n1 = input("Ingrese un numero entre el 1 y el 10: ")
n2 = input("Ingrese otro numero entre el 1 y el 10: ")

print(f"La suma de {n1} y {n2} es: {int(n1) + int(n2)}")
print(f"La resta de {n1} y {n2} es: {int(n1) - int(n2)}")
print(f"La multiplicacion de {n1} y {n2} es: {int(n1) * int(n2)}")
print(f"La division de {n1} y {n2} es: {int(n1) / int(n2)}")
print(f"El residuo de {n1} y {n2} es: {int(n1) % int(n2)}")
print(f"La potencia de {n1} y {n2} es: {int(n1) ** int(n2)}")
print(f"La division entera de {n1} y {n2} es: {int(n1) // int(n2)}")


# Ejercicio 15
n1 = input("Ingrese un numero entre el 1 y el 10: ")
n2 = input("Ingrese otro numero entre el 1 y el 10: ")

print(f"El numero {n1} es igual a {n2}?: {int(n1) == int(n2)}")
print(f"El numero {n1} es diferente a {n2}?: {int(n1) != int(n2)}")
print(f"El numero {n1} es mayor a {n2}?: {int(n1) > int(n2)}")
print(f"El numero {n1} es menor a {n2}?: {int(n1) < int(n2)}")
print(f"El numero {n1} es mayor o igual a {n2}?: {int(n1) >= int(n2)}")
print(f"El numero {n1} es menor o igual a {n2}?: {int(n1) <= int(n2)}")

# Ejercicio 16
var = int(input("Ingrese un numero del 1 al 100: "))
if var >= 60:
    print("Has aprobado")


# Ejercicio 17
password = "tacos123"
user_password = input("Ingrese su contraseña: ")
if password == user_password:
    print("Acceso concedido")
else:
    print("Contraseña incorrecta")


# Ejercicio 18
var = float(input("Ingrese un numero entre 1 y 100: "))

if var >= 60 and var <= 69:
    print("Has aprobado, tu calificación es D")
elif var >= 70 and var <= 79:
    print("Has aprobado, tu calificación es C")
elif var >= 80 and var <= 89:
    print("Has aprobado, tu calificación es B")
elif var >= 90 and var <= 100:
    print("Has aprobado, tu calificación es A")
elif var < 60:
    print("Has reprobado, tu calificación es F")
else:
    print("entrada fuera de rango")

# Ejercicio 19
n1 = "Uno"
n2 = "Dos"
n3 = "Tres"
n4 = "Cuatro"
n5 = "Cinco"

num = input("-convertir numeros a letras-\nIngrese un numero del 1 al 5: ")
if num == "1":
    print(n1)
elif num == "2":
    print(n2)
elif num == "3":
    print(n3)
elif num == "4":
    print(n4)
elif num == "5":
    print(n5)
else:
    print("Numero fuera de rango")

print("Fin")

# Ejercicio 20
est = "estudiante"
tra = "trabajador"
    
edad = int(input("Ingrese su edad: "))

if edad >= 18:
    print("Eres mayor de edad")
    ocupacion = input("Eres estudiante o trabajador?: ")
    ocupacion = ocupacion.lower()
    if ocupacion == est:
        print("Sigue estudiando para un mejor futuro")
    elif ocupacion == tra:
        print("Que tengas exito en el trabajo!")
    else:
        print("Ocupacion no encontrada")

elif edad < 18:
    print("Eres menor de edad")
    if edad < 12 and edad >= 0:
        print("Eres un niño")
    elif edad >= 12:
        print("Eres un adolescente")

else:
    print("Edad no valida")


# Ejercicio 21
cal1 = float(input("Ingrese la calificacion 1: "))
cal2 = float(input("Ingrese la calificacion 2: "))
cal3 = float(input("Ingrese la calificacion 3: "))

promedio = (cal1 + cal2 + cal3) / 3

if cal1 >= 60 and cal2 >= 60 and cal3 >= 60:
    print(f"Has aprobado, tu promedio es: {promedio}")
else:
    print(f"una o mas calificaciones no son aprobatorias, tu promedio es: {promedio}")


# Ejercicio 22
password = "tacos123"
user_password = input("Ingrese su contraseña: ")
if user_password:
    while user_password != password:
        print("Contraseña incorrecta")
        user_password = input("Ingrese su contraseña: ")
    print("Acceso concedido")


# Ejercicio 23
var1 = input("Ingrese una frase: ")
vocales = ['a', 'e', 'i', 'o', 'u']
vocales_M = ['A', 'E', 'I', 'O', 'U']
contador = 0
for letra in var1:
    if letra in vocales or letra in vocales_M:
        contador += 1
print(f"La frase ingresada tiene {contador} vocales")

# Ejercicio 24 
numeros = [15, 8, 22, 52,19,30, 1]
for numero in numeros:
    n1 = numero
    numero2 = 0
    if n1 > numero:
        n1 = numero
    elif n2 < numero:
        n2 = numero2
    
print(f"El numero mayor es:{numero}")


#Ejercicio 25
for i in range(1,6):
    print('*' * i)

#Ejercicio 26

temperatura_celsius = []
def convertir_temp():
    temperaturas_Farenheit = [50,35,15,10,18,150]
    for temperatura in temperaturas_Farenheit:
        temperatura_c = int(5/9*temperatura - 32)
        temperatura_celsius.append(temperatura_c)
    print(temperatura_celsius)

convertir_temp()
"""
