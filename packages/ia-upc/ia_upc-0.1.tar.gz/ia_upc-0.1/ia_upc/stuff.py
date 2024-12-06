def backpropagation():
    '''
    import numpy as np

# We use sigmoid for [0..1] values
# Función de activación sigmoid
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Derivada de la función sigmoid
def sigmoid_derivative(x):
    return x * (1 - x)

# We use tanh for [-1..1] values
# Activation function: Hyperbolic tangent
def tanh(x):
    return np.tanh(x)

# Derivative of tanh
def tanh_derivative(x):
    return 1 - np.tanh(x)**2

class NeuralNetwork:
    def __init__(self, learning_rate):
        input_layer_neurons = X.shape[1]  # Number of input features
        hidden_layer_neurons = 2          # Number of neurons in the hidden layer
        output_neurons = 1                # One output

        self.weights_input_hidden = np.array([[2.0, -2.0],  # Pesos desde X1
                                            [-1.0, -2.0]])  # Pesos desde X2
        self.bias_hidden = np.zeros(shape=(1, hidden_layer_neurons))

        self.weights_hidden_output = np.array([[-1.0],  # Peso desde H1
                                                [-1.0]])  # Peso desde H2

        self.bias_output = np.zeros(shape=(1, output_neurons))


        print(self.weights_input_hidden)
        print(self.weights_hidden_output)
        print(self.bias_hidden)
        print(self.bias_output)

        self.learning_rate = learning_rate

    def train(self, X, y, epochs):
        for epoch in range(epochs):
            # Forward pass
            hidden_layer_input = np.dot(X, self.weights_input_hidden) + self.bias_hidden
            hidden_layer_output = tanh(hidden_layer_input)

            output_layer_input = np.dot(hidden_layer_output, self.weights_hidden_output) + self.bias_output
            predicted_output = tanh(output_layer_input)

            # Compute error
            error = y - predicted_output

            # Backpropagation
            d_predicted_output = error * tanh_derivative(predicted_output)

            error_hidden_layer = d_predicted_output.dot(self.weights_hidden_output.T)
            d_hidden_layer = error_hidden_layer * tanh_derivative(hidden_layer_output)

            # Update weights and biases
            self.weights_hidden_output += hidden_layer_output.T.dot(d_predicted_output) * self.learning_rate
            self.bias_output += np.sum(d_predicted_output, axis=0, keepdims=True) * self.learning_rate

            self.weights_input_hidden += X.T.dot(d_hidden_layer) * self.learning_rate
            self.bias_hidden += np.sum(d_hidden_layer, axis=0, keepdims=True) * self.learning_rate

    def pedict(self, input_data):
        hidden_layer_input = np.dot(input_data, self.weights_input_hidden) + self.bias_hidden
        hidden_layer_output = tanh(hidden_layer_input)

        output_layer_input = np.dot(hidden_layer_output, self.weights_hidden_output) + self.bias_output
        output_layer_output = tanh(output_layer_input)
        return output_layer_output



# Modified XOR dataset with -1 instead of 0
X = np.array([[-1, -1],
              [-1,  1],
              [ 1, -1],
              [ 1,  1]])

y = np.array([[-1], [1], [1], [-1]])

# Hyperparameters
learning_rate = 0.1
epochs = 10000

model  = NeuralNetwork(learning_rate = learning_rate)
model.train(X, y, epochs)

# Predict using the trained model
predicted_output = model.pedict(X)


# Output after training
print("Predicted output after training:")
print(predicted_output)

    '''
    pass


def hopfield():
    '''
    import numpy as np

class HopfieldNetwork:
    def __init__(self, num_neurons):
        self.num_neurons = num_neurons
        self.weights = np.zeros((num_neurons, num_neurons))

    def train(self, patterns):
        for pattern in patterns:
            pattern = np.array(pattern)
            self.weights += np.outer(pattern, pattern)
        np.fill_diagonal(self.weights, 0)

    def run(self, input_pattern, max_iterations=10):
        pattern = np.array(input_pattern)
        for _ in range(max_iterations):
            for i in range(self.num_neurons):
                activation = np.dot(self.weights[i], pattern)
                pattern[i] = 1 if activation > 0 else -1
            print(pattern)
        return pattern


patterns = [
    [-1, 1, 1 ,-1],
    [1, -1, -1, 1]
]

hopfield_net = HopfieldNetwork(num_neurons=4)
hopfield_net.train(patterns)

input_pattern = [-1, 1, -1, 1]
output_pattern = hopfield_net.run(input_pattern)

print("Patrón de entrada:", input_pattern)
print("Patrón recuperado:", output_pattern.tolist())


    '''

    pass



def som():
    '''
    import numpy as np

data = np.array([[-3, 4], [-2, 3], [4, -2], [3, 3], [-4, -3], [-3, -4], [4, 2], [3, -4]])

# Normalización de los datos
def normalize_data(data):
    min_vals = data.min(axis=0)
    max_vals = data.max(axis=0)
    return (data - min_vals) / (max_vals - min_vals)

normalized_data = normalize_data(data)

# Pesos iniciales de las neuronas (4 neuronas)
weights = np.array([[0.5, -0.5], [-1, 0.5], [1.5, -1], [0, 1.5]])


neighborhood = {
    0: [1, 2],  # A ->  B - C
    1: [0, 3],  # B ->  A - D
    2: [0, 3],  # C ->  A - D
    3: [1, 2],  # D ->  B - C
}

def euclidean_distance(x, y):
    return np.sqrt(np.sum((x - y) ** 2))

def learning_rate(bmu_index, current_neuron):
    if bmu_index == current_neuron:
        return 0.4
    elif bmu_index in neighborhood[current_neuron]:
        return 0.2
    return 0

def train_som(data, weights, num_epochs=10):
    for epoch in range(num_epochs):
        for sample in data:
            bmu_index = np.argmin([euclidean_distance(sample, w) for w in weights])

            for i, weight in enumerate(weights):
                # Se actualizan los pesos
                lr = learning_rate(bmu_index, i)
                weights[i] += lr * (sample - weights[i])
        print(f'Epoch {epoch+1}: Weights updated')

    return weights

trained_weights = train_som(normalized_data, weights, num_epochs=10)

print("Pesos finales:")
print(trained_weights)

    '''
    pass


def backdani():
    '''
    import numpy as np

def tanh(x):
    return np.tanh(x)
        #return 1 / (1 + np.exp(-x))


def tanh_derivative(x):
    return 1 - np.tanh(x)**2
        #return x * (1 - x)


def initialize_weights(input_size, hidden_size, output_size, W1_init=None, b1_init=None, W2_init=None, b2_init=None):
    if W1_init is None:
        W1 = np.random.randn(input_size, hidden_size)
    else:
        W1 = W1_init.astype(np.float64)
    if b1_init is None:
        b1 = np.zeros((1, hidden_size))
    else:
        b1 = b1_init.astype(np.float64)
    if W2_init is None:
        W2 = np.random.randn(hidden_size, output_size)
    else:
        W2 = W2_init.astype(np.float64)
    if b2_init is None:
        b2 = np.zeros((1, output_size))
    else:
        b2 = b2_init.astype(np.float64)
    return W1, b1, W2, b2

def train_neural_network(X, y, input_size, hidden_size, output_size, learning_rate, epochs, W1, b1, W2, b2):
    for epoch in range(epochs):
        # Propagación hacia adelante
        Z1 = np.dot(X, W1) + b1
        A1 = tanh(Z1)  # Usamos tanh como función de activación
        Z2 = np.dot(A1, W2) + b2
        A2 = tanh(Z2)  # Salida con activación tanh
        
        # Cálculo del error
        error = y - A2
        if epoch % 1000 == 0:  # Imprimir cada 1000 épocas
            print(f"Epoch {epoch}, Error: {np.mean(np.abs(error))}")
        
        # Backpropagation
        dA2 = error * tanh_derivative(A2)
        dW2 = np.dot(A1.T, dA2)
        db2 = np.sum(dA2, axis=0, keepdims=True)
        
        dA1 = np.dot(dA2, W2.T) * tanh_derivative(A1)
        dW1 = np.dot(X.T, dA1)
        db1 = np.sum(dA1, axis=0, keepdims=True)
        
        # Actualización de pesos
        W1 += learning_rate * dW1
        b1 += learning_rate * db1
        W2 += learning_rate * dW2
        b2 += learning_rate * db2

    return W1, b1, W2, b2, A2

# Datos de entrada y salida (función XOR)
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])  # Entradas
y = np.array([[-1], [1], [1], [-1]])  # Salidas esperadas con valores -1 y 1

# Configuración de la red
input_size = 2  # Número de entradas (x1, x2)
hidden_size = 2  # Número de neuronas en la capa oculta
output_size = 1  # Número de salidas (y)

# Parámetros de entrenamiento
learning_rate = 0.1  # Cambio el learning rate a 0.01
epochs = 10000  # Cambié los epochs a 10,000

# Inicialización con tus propios valores de pesos
W1_init = np.array([[2, -2], [-1, -2]])  # Pesos entre entradas y capa oculta
b1_init = np.array([[0, 0]])  # Sesgos de la capa oculta
W2_init = np.array([[1], [-1]])  # Pesos entre capa oculta y salida
b2_init = np.array([[0]])  # Sesgo de salida

# Usamos los valores inicializados en la red
W1, b1, W2, b2 = initialize_weights(input_size=2, hidden_size=2, output_size=1, W1_init=W1_init, b1_init=b1_init, W2_init=W2_init, b2_init=b2_init)

# Entrenamiento de la red neuronal
W1, b1, W2, b2, A2 = train_neural_network(X, y, input_size, hidden_size, output_size, learning_rate, epochs, W1, b1, W2, b2)

# Predicción final después del entrenamiento
print("\nPredicción final después de entrenamiento:")
print(A2)

    
    
    '''
    pass