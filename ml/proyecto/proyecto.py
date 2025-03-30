import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.impute import SimpleImputer
import seaborn as sns

# 1. Cargar el dataset y seleccionar dos variables independientes
df = pd.read_csv("DataTitanic.csv")

x = df[['Pclass', 'Age']].values.reshape((-1,2))  # Por ejemplo, clase del pasajero y edad
y = df['Survived'].values.reshape((-1,1))

# 2. Mostrar porcentaje de datos inválidos
invalid_data_percentage = df.isnull().sum() / len(df) * 100
print("Porcentaje de datos inválidos:")
print(invalid_data_percentage)

# Manejo de valores nulos
imputer = SimpleImputer(strategy='median')
x[:, 1] = imputer.fit_transform(x[:, 1].reshape(-1, 1)).flatten()

# 3. Graficar histogramas con matplotlib
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.hist(x[:, 0], bins=3, color='blue', alpha=0.7) 
plt.xlabel('Pclass')
plt.ylabel('Frecuencia')
plt.title('Histograma de Pclass')

plt.subplot(1, 2, 2)
plt.hist(x[:, 1], bins=10, color='green', alpha=0.7)
plt.xlabel('Age')
plt.ylabel('Frecuencia')
plt.title('Histograma de Age')

plt.tight_layout()
plt.show()

# 4. Dividir en entrenamiento y prueba (80%-20%)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# 5. Entrenar el modelo de regresión logística
logistic_model = LogisticRegression()
logistic_model.fit(x_train, y_train)

# 6. Evaluar el modelo
y_pred_train = logistic_model.predict(x_train)
y_pred_test = logistic_model.predict(x_test)

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
plt.plot(range(len(errors)), errors, color='purple')
plt.xlabel("Índice de muestra")
plt.ylabel("MSE")
plt.title("MSE en las muestras de prueba")
plt.legend()
plt.show()

# 9. Graficar datos reales vs predicción
fig = plt.figure()
plt.rcParams['figure.figsize'] = (10,10)
ax = fig.add_subplot(111, projection='3d')
# Print class 0 of y test  #
ax.scatter(x_test[np.where(y_test == 0)[0],0], x_test[np.where(y_test == 0)[0],1], 0, s=85, c='crimson', alpha=0.5, label = "0 - Test")
# Print class 1 of y test #
ax.scatter(x_test[np.where(y_test == 1)[0],0], x_test[np.where(y_test == 1)[0],1], 1, s=85, c='lime', alpha=1, label = "1 - Test")
# Print class 0 of y predicted  #
ax.scatter(x_test[np.where(y_pred_test == 0)[0],0], x_test[np.where(y_pred_test == 0)[0],1], 0, s=35, c='gold', alpha=1, label = "0 - Predicted")
# Print class 1 of y predictet #
ax.scatter(x_test[np.where(y_pred_test == 1)[0],0], x_test[np.where(y_pred_test == 1)[0],1], 1, s=35, c='purple', alpha=1, label = "1 - Predicted")
ax.set_xlabel("Edad")
ax.set_ylabel("Colesterol")
ax.set_zlabel("Probabilidad")
plt.legend(fontsize=20, loc="lower left")
plt.show()