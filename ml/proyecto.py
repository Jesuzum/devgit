import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# 1. Cargar el dataset y seleccionar dos variables independientes
df = pd.read_csv("DataTitanic.csv")

X = df[['Pclass', 'Age']]  # Por ejemplo, clase del pasajero y edad
y = df['Survived']

# 2. Mostrar porcentaje de datos inválidos
invalid_data_percentage = df.isnull().sum() / len(df) * 100
print("Porcentaje de datos inválidos:")
print(invalid_data_percentage)

# Manejo de valores nulos
X.loc[:, 'Age'] = X['Age'].fillna(X['Age'].mean())

# 3. Graficar histogramas con matplotlib
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.hist(X['Pclass'], bins=3, color='blue', alpha=0.7)
plt.xlabel('Pclass')
plt.ylabel('Frecuencia')
plt.title('Histograma de Pclass')

plt.subplot(1, 2, 2)
plt.hist(X['Age'], bins=10, color='green', alpha=0.7)
plt.xlabel('Age')
plt.ylabel('Frecuencia')
plt.title('Histograma de Age')

plt.tight_layout()
plt.show()

# 4. Dividir en entrenamiento y prueba (80%-20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Entrenar el modelo de regresión logística
logistic_model = LogisticRegression()
logistic_model.fit(X_train, y_train)

# 6. Evaluar el modelo
y_pred_train = logistic_model.predict(X_train)
y_pred_test = logistic_model.predict(X_test)

r2 = r2_score(y_test, y_pred_test)
mae = mean_absolute_error(y_test, y_pred_test)
mse = mean_squared_error(y_test, y_pred_test)

print(f"R^2 Score: {r2:.4f}")
print(f"MAE: {mae:.4f}")
print(f"MSE: {mse:.4f}")

# 7. Obtener intercepto y pendientes
print("Intercepto del modelo:", logistic_model.intercept_)
print("Pendientes del modelo (coeficientes):", logistic_model.coef_)

# 8. Graficar el MSE para cada muestra del conjunto de prueba
errors = (y_test - y_pred_test) ** 2
plt.figure()
plt.plot(range(len(errors)), errors, label="MSE por muestra", color='purple')
plt.xlabel("Índice de muestra")
plt.ylabel("MSE")
plt.title("MSE en las muestras de prueba")
plt.legend()
plt.show()

# 9. Graficar datos reales vs predicción
plt.figure()
plt.scatter(y_test, y_pred_test, color='red', alpha=0.6)
plt.xlabel("Valores reales (Survived)")
plt.ylabel("Predicción (Survived)")
plt.title("Datos Reales vs Predicciones")
plt.show()