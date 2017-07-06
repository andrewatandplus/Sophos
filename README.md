# Sophos

This is a repository designed to facilitate the understanding of artificial neural networks. The entire framework is written in python so that it is easy to understand how each component works.

## General Structure
The general use of Sophos is based on the Keras framework. Different objects can be created and added to the model to form a network for data to flow through

Import the library
```python
import SophosNet as sn
```

## Layers
There are two types of objects currently available - Fully Connected Layers and Activation Layers
Fully connected layers are feed forward layers in which the input size and number of neurons are specified.
Activation Layers specify an activation function. Currently the implemented functions are Heaviside, ReLU and Sigmoid.

Example:
```python
# Create a fully connected layer
l1 = sn.Layer()
# Create an activation layer with a Sigmoid activation
a1 = sn.Activation('sigmoid')
# Create an activation layer with a ReLU activation
a2 = sn.Activation('relu')
# Create an activation layer with a Heaviside activation
a3 = sn.Activation('step')
```

## Models
A model contains a sequence of layers. When you train or run the model it feeds data from layer to layer in order to generate an output.

```python
# Create a new model
model = sn.Model()
# Add layers created before to the model
model.add(l1)
model.add(a1)
```