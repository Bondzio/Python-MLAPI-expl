#!/usr/bin/env python
# coding: utf-8

# ### Program to implement AND, OR, NAND, NOR, XOR, XNOR and NOT gates using conventional ANN - Artificial Neural Network

# In[ ]:


from math import exp


# In[ ]:


# Calculate neuron activation for an input
def activate(weights, inputs):
	activation = weights[-1]
	for i in range(len(weights)-1):
		activation += weights[i] * inputs[i]
	return activation


# In[ ]:


# Transfer neuron activation
def transfer(activation):
	return 1.0 / (1.0 + exp(-activation))


# In[ ]:


# Forward propagate input to a network output
def forward_propagate(network, row):
	inputs = row
	for layer in network:
		new_inputs = []
		for neuron in layer:
			activation = activate(neuron['weights'], inputs)
			neuron['output'] = transfer(activation)
			new_inputs.append(neuron['output'])
		inputs = new_inputs
	return inputs


# ### NAND gate implementation

# In[ ]:


# test forward propagation
network = [[{'weights': [-20, -20, 30]}]]
row = [[0, 0], [0, 1],[1, 0],[1, 1]]


# In[ ]:


for i in row:
    output = forward_propagate(network, i)
    print("x1 and x2 are {} and {} and the output is {}.".format(i[0], i[1], round(output[0])))


# ### NOR gate implementation

# In[ ]:


# test forward propagation
network = [[{'weights': [-15, -15, 10]}]]
row = [[0, 0], [0, 1],[1, 0],[1, 1]]


# In[ ]:


for i in row:
    output = forward_propagate(network, i)
#     print(type(output))
    print("x1 and x2 are {} and {} and the output is {}.".format(i[0], i[1], round(output[0])))


# ### NOT gate implementation

# In[ ]:


# test forward propagation
network = [[{'weights': [-15, 5]}]]
row = [[0], [1]]
for i in row:
    output = forward_propagate(network, i)
    print("x1 is {} and the output is {}.".format(i, round(output[0])))


# ### AND gate implementation

# In[ ]:


network = [[{'weights': [30, 15, -30]}]]
row = [[0, 0], [0, 1], [1, 0], [1, 1]]
for i in row:
    output = forward_propagate(network, i)
    print("x1 and x2 are {} and {} and the output is {}.".format(i[0], i[1], round(output[0])))


# ### OR gate implementation

# In[ ]:


network = [[{'weights': [-40, -40, 40]}]]
row = [[0, 0], [0, 1], [1, 0], [1, 1]]
for i in row:
    output = forward_propagate(network, i)
    print("x1 and x2 are {} and {} and the output is {}.".format(i[0], i[1], round(output[0])))


# ### XOR gate implementation

# In[ ]:


network = [[{'weights': [10, 10, -10]}]]
row = [[0, 0], [0, 1], [1, 0], [1, 1]]
for i in row:
    output = forward_propagate(network, i)
    if(output[0]==0.5):
        output[0] = 1
    else:
        output[0] = 0
    print("x1 and x2 are {} and {} and the output is {}.".format(i[0], i[1], round(output[0])))


# ### XNOR gate implementation

# In[ ]:


network = [[{'weights': [10, 10, -10]}]]
row = [[0, 0], [0, 1], [1, 0], [1, 1]]
for i in row:
    output = forward_propagate(network, i)
    if(output[0]==0.5):
        output[0] = 0
    else:
        output[0] = 1
    print("x1 and x2 are {} and {} and the output is {}.".format(i[0], i[1], round(output[0])))

