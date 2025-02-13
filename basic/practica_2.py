"""
- precio por boleto 50 pesos
- menores de 18 años tienen un 20% de descuento
- si se compran 4 boletos o más se aplica un 10% de descuento
- Funciones proyectadas antes de la 15 horas, se aplica un 15% de descuento
- imprimir los descuentos a los que el usuario tiene derecho
- imprimir el total a pagar
- si el usuario compro mas de 6 boletos y además fue elegible para el descuento de menor de 18 o para la promocion de antes de las 15 horas, se gana un snak gratis
- Si no se cumplen las condiciones anteriores, imprimir en pantalla que el usuario no es elegible para un snack gratis
"""

boleto = 50
print("Bienvenido, llego tu turno en la fila para comprar tus boletos!\n")

edad = int(input("Ingresa tu edad: "))
boletos = int(input("Ingresa la cantidad de boletos a comprar: "))
hora = int(input("Ingresa la hora de tu función(formato de 24 horas): "))

boletos_compra = boletos * boleto

if edad < 18:
    descuento_1 = boletos_compra * 0.20
    boletos_compra_1 = boletos_compra - descuento_1
    print (f"Por ser menor de 18 años tienes un descuento del 20%, total: {boletos_compra_1}")
    print(f"Total a pagar: {boletos_compra_1}")
    if boletos >= 4:
        descuento_2 = boletos_compra_1 * 0.10
        boletos_compra_2 = boletos_compra_1 - descuento_2
        print(f"Total a pagar: {boletos_compra_2}")
        print(f"Por comprar 4 o más boletos tienes un descuento del 10%, total: {boletos_compra_2}")
        if hora < 15:
            descuento_3 = boletos_compra_2 * 0.15
            boletos_compra_3 = boletos_compra_2 - descuento_3
            print(f"Por comprar antes de las 15 horas tienes un descuento del 15%, total: {boletos_compra_3}")
            print(f"Total a pagar: {boletos_compra_3}")
            if boletos > 6:
                print("Felicidades! Has ganado un snack gratis")
            else:
                print("Lo siento, no eres elegible para un snack gratis")

elif boletos >= 4:
    descuento_1 = boletos_compra * 0.10
    boletos_compra_1 = boletos_compra - descuento_1
    print(f"Por comprar 4 o más boletos tienes un descuento del 10%: {boletos_compra_1}")
    print(f"Total a pagar: {boletos_compra_1}")
    if hora < 15:
        descuento_2 = boletos_compra_1 * 0.15
        boletos_compra_2 = boletos_compra_1 - descuento_2
        print(f"Por comprar antes de las 15 horas tienes un descuento del 15%: {boletos_compra_2}")
        print(f"Total a pagar: {boletos_compra_2}")
        if boletos > 6:
            print("Felicidades! Has ganado un snack gratis")
        else:
            print("Lo siento, no eres elegible para un snack gratis")
            
elif hora < 15:
    descuento_1 = boletos_compra * 0.15
    boletos_compra_1 = boletos_compra - descuento_1
    print(f"Por comprar antes de las 15 horas tienes un descuento del 15%: {boletos_compra_1}")
    print(f"Total a pagar: {boletos_compra_1}")
    if boletos > 6:
        print("Felicidades! Has ganado un snack gratis")
    else:
        print("Lo siento, no eres elegible para un snack gratis")

else:
    print(f"El total a pagar es: {boletos_compra}")
    print("Lo siento, no eres elegible para ninguna promoción")
