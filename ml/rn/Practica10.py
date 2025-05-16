import numpy as np
import matplotlib.pyplot as plt

class Perceptron:
    def __init__(self, input_size, learning_rate=0.1):
        """
        Inicializa el perceptrón
        
        Args:
            input_size: Número de neuronas en la capa de entrada
            learning_rate: Tasa de aprendizaje para actualizar los pesos
        """
        # Inicializar pesos aleatoriamente (incluyendo sesgo)
        self.weights = np.random.randn(input_size)
        self.bias = np.random.randn()
        self.learning_rate = learning_rate
    
    def heaviside(self, x):
        """
        Función de activación Heaviside (escalón)
        
        Args:
            x: Valor de entrada
        
        Returns:
            1 si x >= 0, 0 en caso contrario
        """
        return 1 if x >= 0 else 0
    
    def predict(self, inputs):
        """
        Realiza la predicción para un conjunto de entradas
        
        Args:
            inputs: Vector de entradas
            
        Returns:
            Salida del perceptrón después de aplicar la función de activación
        """
        # Calcular la suma ponderada: v_n = w_n^T * x + b_n
        summation = np.dot(inputs, self.weights) + self.bias
        
        # Aplicar la función de activación: y_n = φ(v_n)
        return self.heaviside(summation)
    
    def train(self, training_inputs, labels, epochs):
        """
        Entrena el perceptrón utilizando el conjunto de datos proporcionado
        
        Args:
            training_inputs: Matriz con los datos de entrada
            labels: Vector con las etiquetas esperadas
            epochs: Número de iteraciones completas sobre el conjunto de datos
            
        Returns:
            history: Diccionario con historial de pesos, salidas y errores
        """
        history = {
            'weights': [], 
            'bias': [],
            'outputs': [],
            'errors': []
        }
        
        for epoch in range(epochs):
            total_error = 0
            outputs = []
            
            print(f"\nÉpoca {epoch+1}/{epochs}")
            print("-" * 50)
            
            for inputs, label in zip(training_inputs, labels):
                # Realizar predicción
                output = self.predict(inputs)
                outputs.append(output)
                
                # Calcular error
                error = label - output
                total_error += abs(error)
                
                # Actualizar pesos solo si hay error
                if error != 0:
                    # Ecuación (9): Δw = η * e * x
                    delta_weights = self.learning_rate * error * inputs
                    
                    # Ecuación (10): Δb = η * e
                    delta_bias = self.learning_rate * error
                    
                    # Actualizar pesos y sesgo
                    self.weights += delta_weights
                    self.bias += delta_bias
                
                # Imprimir actualizaciones
                print(f"Entrada: {inputs}, Salida: {output}, Esperada: {label}, Error: {error}")
                print(f"Pesos actualizados: {self.weights}, Sesgo: {self.bias}")
                print("-" * 30)
            
            # Guardar historial
            history['weights'].append(self.weights.copy())
            history['bias'].append(self.bias)
            history['outputs'].append(outputs.copy())
            history['errors'].append(total_error)
            
            print(f"Error total en época {epoch+1}: {total_error}")
            
            # Si no hay error, detener el entrenamiento
            if total_error == 0:
                print("\n¡Convergencia alcanzada!")
                break
                
        return history

    def visualize_decision_boundary(self, X, y, title):
        """
        Visualiza la frontera de decisión del perceptrón
        
        Args:
            X: Datos de entrada
            y: Etiquetas
            title: Título del gráfico
        """
        # Crear figura
        plt.figure(figsize=(10, 6))
        
        # Graficar puntos
        for i in range(len(y)):
            if y[i] == 1:
                plt.plot(X[i, 0], X[i, 1], 'bo', markersize=10)
            else:
                plt.plot(X[i, 0], X[i, 1], 'ro', markersize=10)
        
        # Crear malla para visualizar frontera
        x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
        y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01),
                             np.arange(y_min, y_max, 0.01))
        
        # Si w1*x + w2*y + b = 0, entonces y = (-w1*x - b) / w2
        if self.weights[1] != 0:  # Evitar división por cero
            slope = -self.weights[0] / self.weights[1]
            intercept = -self.bias / self.weights[1]
            x_vals = np.array([x_min, x_max])
            y_vals = slope * x_vals + intercept
            plt.plot(x_vals, y_vals, 'g-', linewidth=2)
        
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.grid(True)
        plt.title(title)
        plt.xlabel('X1')
        plt.ylabel('X2')
        plt.legend(['Clase 1 (1)', 'Clase 0 (0)', 'Frontera de decisión'])
        plt.show()


# Datos de entrada para las compuertas lógicas (2 entradas)
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

# Etiquetas para AND y OR
y_and = np.array([0, 0, 0, 1])
y_or = np.array([0, 1, 1, 1])

# Entrenar para la compuerta AND
print("\n" + "="*50)
print("ENTRENAMIENTO PARA COMPUERTA AND")
print("="*50)
perceptron_and = Perceptron(input_size=2, learning_rate=0.1)
history_and = perceptron_and.train(X, y_and, epochs=100)

# Prueba final para AND
print("\nPrueba final para compuerta AND:")
for inputs in X:
    output = perceptron_and.predict(inputs)
    print(f"Entrada: {inputs}, Salida: {output}")

# Visualizar frontera de decisión para AND
perceptron_and.visualize_decision_boundary(X, y_and, "Frontera de decisión para compuerta AND")

# Entrenar para la compuerta OR
print("\n" + "="*50)
print("ENTRENAMIENTO PARA COMPUERTA OR")
print("="*50)
perceptron_or = Perceptron(input_size=2, learning_rate=0.1)
history_or = perceptron_or.train(X, y_or, epochs=100)

# Prueba final para OR
print("\nPrueba final para compuerta OR:")
for inputs in X:
    output = perceptron_or.predict(inputs)
    print(f"Entrada: {inputs}, Salida: {output}")

# Visualizar frontera de decisión para OR
perceptron_or.visualize_decision_boundary(X, y_or, "Frontera de decisión para compuerta OR")