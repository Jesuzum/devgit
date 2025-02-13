
print("Seleccione la opcion que desea realizar.\n1. Suma\n2. Resta\n3. Multiplicacion\n4. Division\n5. Residuo\n6. Potencia")
num = int(input("Seleccion: "))

if num == 1:
    print("Suma")
    num = int(input("Ingrese el primer numero: "))
    num += int(input("Ingrese el segundo numero: "))
    print(f"La suma es: {num}")
elif num == 2:
    print("Resta")
    num = int(input("Ingrese el primer numero: "))
    num -= int(input("Ingrese el segundo numero: "))
    print(f"La resta es: {num}")
elif num == 3:
    print("Multiplicacion")
    num = int(input("Ingrese el primer numero: "))
    num *= int(input("Ingrese el segundo numero: "))
    print(f"La multiplicacion es: {num}")
elif num == 4:
    print("Division")
    num = int(input("Ingrese el primer numero: "))
    num /= int(input("Ingrese el segundo numero: "))
    print(f"La division es: {num}")
elif num == 5:
    print("Residuo")
    num = int(input("Ingrese el primer numero: "))
    num %= int(input("Ingrese el segundo numero: "))
    print(f"El residuo es: {num}")
elif num == 6:
    print("Potencia")
    num = int(input("Ingrese el primer numero: "))
    num **= int(input("Ingrese el segundo numero: "))
    print(f"La potencia es: {num}")
else:
    print("Opcion no valida")