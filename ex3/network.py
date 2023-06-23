import numpy as np


class Layer:
    def __init__(self):
        self.inp = None
        self.out = None

    def forward_propagation(self, inp):
        raise NotImplementedError()

    def backward_propagation(self, out_error, learn_rate):
        raise NotImplementedError()


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

    # returns the activated input
    def forward_propagation(self, inp):
        self.inp = inp
        self.out = self.activation(self.inp)
        return self.out

    # Returns input_error=dE/dX for a given output_error=dE/dY.
    # learning_rate is not used because there is no "learnable" parameters.
    def backward_propagation(self, out_error, learn_rate):
        return self.activation_prime(self.inp) * out_error

    def __str__(self):
        return f"[{self.activation.__name__}]"


class Network:
    def __init__(self):
        self.layers = []
        self.loss = None
        self.loss_prime = None

    # add layer to network
    def add(self, layer):
        self.layers.append(layer)

    # set loss to use
    def use(self, loss, loss_prime):
        self.loss = loss
        self.loss_prime = loss_prime

    # predict output for given input
    def predict(self, input_data):
        # sample dimension first
        samples = len(input_data)
        result = []

        # run network over all samples
        for i in range(samples):
            # forward propagation
            output = input_data[i]
            for layer in self.layers:
                output = layer.forward_propagation(output)
            result.append(output)

        return result

    # train the network
    def fit(self, x_train, y_train, epochs, learning_rate):
        # sample dimension first
        samples = len(x_train)

        # training loop
        for i in range(epochs):
            err = 0
            for j in range(samples):
                # forward propagation
                output = x_train[j]
                for layer in self.layers:
                    output = layer.forward_propagation(output)

                # compute loss (for display purpose only)
                err += self.loss(y_train[j], output)

                # backward propagation
                error = self.loss_prime(y_train[j], output)
                for layer in reversed(self.layers):
                    error = layer.backward_propagation(error, learning_rate)

            # calculate average error on all samples
            err /= samples
            print("epoch %d/%d   error=%f" % (i + 1, epochs, err))

    def __str__(self):
        return "inp " + "".join(map(str, self.layers)) + " -> out"
