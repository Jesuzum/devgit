import numpy as np

"""
#Ejercicio 1
lista = [1,2,3,4,5]
arr = np.array([1,2,3,4,5])
print(type(lista))
print(type(arr))


#Ejercicio 2
arr = np.array(10)
arr1 = np.array([1,2,3,4,5])
arr2 = np.array([[1,2,3,4],[5,6,7,8]])

arr3 = np.array([[[1,2,3,4],[5,6,7,8]],
                 [[1,2,3,4],[5,6,7,8]],
                 [[1,2,3,4],[5,6,7,8]]])

print(arr.ndim, arr.shape)
print(arr1.ndim, arr1.shape)
print(arr2.ndim, arr2.shape)
print(arr3.ndim, arr3.shape)


#Ejercico 3
arr = np.zeros([3,2])

arr1 = np.ones([3,2])

arr2 = np.random.rand(3,2)

arr3= np.random.uniform(1,3,[3,3])
print(arr3)


#Ejercicio 4
#Create an arrange with fixed values
arr = np.arange(10,50)
print(arr)

rewarr = arr.reshape(4,10)
print(rewarr)

rewarr = arr.reshape(8,5)
print(rewarr)


#Ejercicio 5
A = np.arange(10,50)
A = A.reshape(4,10)
print(A)

# Extraer la segunda y cuarta fila de la matriz
second_and_fourth_rows = A[[1, 3], :]
print("Segunda y cuarta fila:")
print(second_and_fourth_rows)

# Calcular la media de cada columna
column_means = A.mean(axis=0)
print("Media de cada columna:")
print(column_means)

# ejercicio 6
A = np.random.rand(5, 5)
print(A)

A[A < 0.3] = 0
print("Matriz con valores menores que 0.3 reemplazados por 0:")
print(A)

valores_mayores_0_6 = A[A > 0.6]
print("Valores mayores que 0.6:")
print(len(valores_mayores_0_6))

# Ejercicio 6.1
A = np.random.rand(5, 5)
print(A)

for i in range(A.shape[0]):
    for j in range(A.shape[1]):
        if A[i, j] < 0.3:
            A[i, j] = 0

print("Matriz con valores menores que 0.3 reemplazados por 0:")
print(A)

count = 0
for i in range(A.shape[0]):
    for j in range(A.shape[1]):
        if A[i, j] > 0.6:
            count += 1

print("Valores mayores que 0.6:")
print(count)


# Ejercicio 7
arr = np.random.randint(1, 16, size=(5, 5))
print("Original array:")
print(arr)

for i in range(arr.shape[0]):
    for j in range(arr.shape[1]):
        arr[i, j] = arr[i, j]**2 + 2*arr[i, j] + 1

print("Modified array:")
print(arr)


# Ejercicio 8
#Create array
a = np.array([1,2,3])
b = np.array([4,5,6])

elemento = a * b
dot_product = np.dot(a, b)
dot_product_alt = a @ b

#print results
print(elemento.shape)
print(elemento)
print(dot_product)
print(dot_product_alt)

# Ejercicio 9
#Create matrix (2,2)
A = np.array([[1,2],[3,4]])
B = np.array([[5,6],[7,8]])

elementmatrix = A * B
matrix_product = np.dot(A, B)
matrix_product_alt = A @ B

#print results
print(elementmatrix.shape)
print(elementmatrix)
print(matrix_product)
print(matrix_product_alt)
"""

# Ejercicio 10
A = np.array([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
B = np.array([[5, 6], [9, 11], [15, 18]])
C = np.array([4, 5, 6])


fo = A @ B
so = B @ A
to = B @ C
foo = A @ B @ C
fio = A @ C

print(fo)
print(so)
print(to)
print(foo)
print(fio)
