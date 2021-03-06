
# coding: utf-8

# Setup import
import numpy as np


""" Model Class
    Contains a linear sequence of all the layers in the model
"""
class Model():
    
    # Model will contain sequence of layers to feed data 
    def __init__(self):
        self.components = list()
        self.lr = 0.5
    
    # Add a layer to the model
    def add(self, component):
        self.components.append(component)
        
    # Feed Data and Learn
    def train(self, X, Y):
        lastOut = X
        # Feed Data
        for layer in self.components:
            lastOut = layer.feed(lastOut)
        # Set the prediction
        pred = lastOut
        
        # Verify that output layer is an activation function
        if type(self.components[len(self.components)-1]) != Activation:
            raise ValueError("Output layer must have activation function")
        
        # Optimize
        components = self.components
        # Store the total error
        error_total = np.sum(0.5 * np.square(Y-pred))
        self.error_total = error_total
        # Get error for output layer
        

        last_dE = 0
        last_delta = 0
        error = list()
        last_weights = 0
        # Iterate over every neuron to compute delta 
        for i in range(len(components)):
            # Set the current component
            current_component_index = len(components) - i -1
            current_component = components[current_component_index]

            layer_output = pred
            # If the component is a layer adjust neuron weights
            if type(current_component) is Layer:
                # Calculate dE/dw
                
                # No cached value - back of net
                if last_dE is 0:
                    # dE/dOut
                    dEdOut = layer_output - Y
                    last_dE = dEdOut
                # print("dE/dOut: ", dEdOut)

                # Calculate dOut/dNet
                activation_layer = components[current_component_index + 1]
                dOutdNet = activation_layer.d_feed(activation_layer.getOutput())
                # print("dOut/dNet: ", dOutdNet)

                # Calculate dNet/dW
                if current_component_index == 0:
                    dNetdW = X
                    # Add Bias
                    dNetdW = np.insert(dNetdW, 0, 1, axis=1)
                else:
                    dNetdW = components[current_component_index-1].getOutput()
                    # Add Bias
                    dNetdW = np.insert(dNetdW, 0, 1, axis=1)
                # print("dNet/dW: ", dNetdW)
                
                if current_component_index + 2 < len(components):
                    prev_weights = last_weights
                    prev_weights = prev_weights[1:]
                    dEdOut = last_delta * prev_weights.T
                    # print("new dEdOut: ", dEdOut)

                delta = np.multiply(dEdOut, dOutdNet)
                # print("Delta: ", delta)
                # dEdW = np.multiply(delta, dNetdW)
                dEdW = np.multiply(dNetdW.T, delta)
                # print("dE/dw: ", dEdW)
                last_weights = current_component.getWeights()
                # Update Weights
                current_component.updateWeights(dEdW, self.lr)
                last_delta = delta
                # print("Updated Weights: ", current_component.getWeights())
                # print("delta: ", last_delta)

        
        return lastOut
    
    def show(self):
        model_display = ""
        for component in self.components:
            model_display += 'Type: {}'.format(component.getType())
            model_display += ' - Size: {}\n'.format(component.getShape())
        model_display += "---------------"
        return model_display

    def feed(self, X):
        lastOut = X
        for layer in self.components:
            lastOut = layer.feed(lastOut)
        return lastOut

    def getTotalError(self):
        return self.error_total

    def predictStep(self, X):
        # Step Function for prediction
        lastOut = X
        for layer in self.components:
            lastOut = layer.feed(lastOut)
        if lastOut > .5:
            return 1
        return 0

    def setLearningRate(self, lr):
        self.lr = lr


# In[525]:


class Layer():
    
    def __init__(self, num_inputs, num_neurons):
        self.num_neurons = num_neurons
        self.num_inputs = num_inputs
        # Build Psi - Random Weights
        self.W = np.random.random_sample((num_inputs + 1, num_neurons))
        self.last_output = 0
        self.learning_rate = 0.5
        
    def feed(self, X):
        biases = np.ones(X.shape[0])
        # Add bias
        X = np.insert(X, 0, biases, axis=1)
        # Error checking
        if X.shape[1] != self.W.shape[0]:
            raise ValueError("Wrong input shape")
        # Remember Last Output
        last_output_no_bias = X * self.W
        self.last_output = X * self.W

        
        # Multiply
        return X * self.W
    
    def getShape(self):
        return [self.num_inputs + 1, self.num_neurons]
        
    def getWeights(self):
        return self.W
    
    def setWeights(self, X):
        # Set all of the weights to a new value
        self.W = X
        
    def updateWeights(self, X, lr):
        # Adjust Weights by a value
        self.W = self.W - np.multiply(lr, X)
        pass
    
    def getOutput(self):
        return self.last_output
    
    def getType(self):
        return "Dense Layer"


# In[526]:


class Activation():
    
    # Activation Functions
    def __init__(self, activation):
        self.activation_function = activation
    
    def feed(self, X):
        if self.activation_function == 'step':
            out = np.piecewise(X, [X < 0, X >= 0], [0, 1])
        if self.activation_function == 'sigmoid':
            out = 1/(1 + np.exp(-X))
            # self.d_output = np.multiply(X, (-X + 1))
        if self.activation_function == 'relu':
            np.maximum(X, 0, X)
            out =  X
        self.last_output = out
        return out

    # Derivative of activation
    def d_feed(self, X):
        if self.activation_function == 'sigmoid':
            out = np.multiply(X, (-X + 1))
        if self.activation_function == 'relu':
            out = np.piecewise(X, [X < 0, X >= 0], [0, 1])
        self.d_output = out
        return out


    def getType(self):
        return "Activation Function {fxn}".format(fxn=self.activation_function)

    def getOutput(self):
        return self.last_output

    def getDerivativeOutput(self):
        return self.d_output

# In[529]:


class Optimizer():
    
    def __init__(self, lr):
        self.lr = lr
    
    # Define Optimizers
    def grad(self, X, Y):
        # Define error and loss
        error = pred-Y
        loss = np.sum(error ** 2)
        
        # Calculate Gradient
        gradient = X.T.dot(error) / X.shape[0]
        
        return gradient