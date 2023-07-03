from typing import Protocol

import numpy as np


class Layer(Protocol):
    def forward_propagation(self, inp):
        ...

    def backward_propagation(self, out_error, learn_rate):
        ...


class FCLayer(Layer):
    def __init__(self, inp_size, out_size):
        self.inp_size = inp_size
        self.out_size = out_size
        self.weights = np.random.rand(inp_size, out_size) - 0.5
        self.bias = np.random.rand(1, out_size) - 0.5

    def forward_propagation(self, inp):
        self.inp = inp
        self.out = np.dot(self.inp, self.weights) + self.bias
        return self.out

    def backward_propagation(self, out_error, learn_rate):
        inp_error = np.dot(out_error, self.weights.T)
        weights_error = np.dot(self.inp.T, out_error)

        self.weights -= learn_rate * weights_error
        self.bias -= learn_rate * out_error
        return inp_error

    def __str__(self):
        return f"-> {self.inp_size}:{self.__class__.__name__}:{self.out_size}"


class ActivationLayer(Layer):
    def __init__(self, activation, activation_prime):
        self.activation = activation
        self.activation_prime = activation_prime

    def forward_propagation(self, inp):
        self.inp = inp
        self.out = self.activation(self.inp)
        return self.out

    def backward_propagation(self, out_error, learn_rate):
        return self.activation_prime(self.inp) * out_error

    def __str__(self):
        return f"[{self.activation.__name__}]"


class Network:
    def __init__(self):
        self.layers = []
        self.loss = None
        self.loss_prime = None

    def add(self, layer):
        self.layers.append(layer)

    def use(self, loss, loss_prime):
        self.loss = loss
        self.loss_prime = loss_prime

    def predict(self, input_data):
        samples = len(input_data)
        result = []

        for i in range(samples):
            output = input_data[i]
            for layer in self.layers:
                output = layer.forward_propagation(output)
            result.append(output)

        return result

    def fit(self, x_train, y_train, epochs, learning_rate):
        error_rates = []
        samples = len(x_train)

        for i in range(epochs):
            err = 0
            for j in range(samples):
                output = x_train[j]
                for layer in self.layers:
                    output = layer.forward_propagation(output)

                err += self.loss(y_train[j], output)

                error = self.loss_prime(y_train[j], output)
                for layer in reversed(self.layers):
                    error = layer.backward_propagation(error, learning_rate)

            err /= samples
            error_rates.append(err)
            print("epoch %d/%d   error=%f" % (i + 1, epochs, err))
        return error_rates

    def __str__(self):
        return "inp " + "".join(map(str, self.layers)) + " -> out"
