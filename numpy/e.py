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
"""

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