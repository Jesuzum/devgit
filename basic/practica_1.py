def convertir_a_entero(valor):
    try:
        num = float(valor)  # Intentar convertir a float
        return int(num)  # Convertir a entero truncando decimales
    except ValueError:
        return None  # Si falla, retornar None

num1 = input("Ingrese un número: ")
num2 = input("Ingrese otro número: ")

num1 = convertir_a_entero(num1)
num2 = convertir_a_entero(num2)

if num1 is None:
    print("El primer valor no es un número")
    exit("Programa terminado")

elif num2 is None:
    print("El segundo valor no es un número")
    exit("Programa terminado")

else:
    if num1 % num2 == 0 and num1 != 0:
        print(f"El número {num1} es múltiplo de {num2}")
    else:
        print(f"El número {num1} no es múltiplo de {num2}")
