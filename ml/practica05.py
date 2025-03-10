import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Cargar el dataset
df = pd.read_csv(r"C:\Users\sofia\Desktop\octavo\aprendizaje maquina\05.03\Productos.csv")

# Eliminar filas con valores nulos
df = df.dropna(subset=['Horas Trabajadas', 'Productos Terminados'])

# Convertir las columnas a tipo float, reemplazando comas por puntos
df['Horas Trabajadas'] = df['Horas Trabajadas'].astype(str).str.replace(',', '.').astype(float)
df['Productos Terminados'] = df['Productos Terminados'].astype(str).str.replace(',', '.').astype(float)

# Definir variables independientes (X) y dependientes (Y)
X = df[['Horas Trabajadas']].values  # Convertir a matriz 2D
y = df[['Productos Terminados']].values  # Convertir a matriz 2D

# Dividir el conjunto de datos en entrenamiento (70%) y prueba (30%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Crear y entrenar el modelo de regresión lineal
model = LinearRegression()
model.fit(X_train, y_train)

# Hacer predicciones en el conjunto de prueba
y_pred = model.predict(X_test)

# Calcular el error medio cuadrático
mse = mean_squared_error(y_test, y_pred)
print(f"Coeficiente m: {model.coef_[0][0]}")
print(f"Intercepto b: {model.intercept_[0]}")
print(f"Ecuación de la recta: y = {model.coef_[0][0]}x + {model.intercept_[0]}")
print(f'Error Medio Cuadrático: {mse:.2f}')

# Graficar los datos de prueba y la regresión lineal
plt.scatter(X_test, y_test, color='blue', label='Real Data')
plt.scatter(X_test, y_pred, color='green', label='Prediction')
plt.plot(X_test, y_pred, color='red', linewidth=2, label='Linear Regression')
plt.xlabel('Horas Trabajadas')
plt.ylabel('Productos Terminados')
plt.legend()
plt.show()

# Predecir la cantidad de productos terminados para nuevas horas trabajadas
nuevas_horas = np.array([20, 38, 42, 55, 80, 14]).reshape(-1, 1)
predicciones = model.predict(nuevas_horas)
print("Predicciones para nuevas horas trabajadas:", predicciones.flatten())