import numpy as np
from scipy import special
import matplotlib.pyplot


class Nnfromsctretch:

    def __init__(self, inputnodes, hiddennodes, outputnodes, learning_rate):
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes
        self.lr = learning_rate
        self.w1 = np.random.normal(0.0, 1 / np.sqrt(self.inodes), (self.inodes, self.hnodes))
        self.w2 = np.random.normal(0.0, 1 / np.sqrt(self.hnodes), (self.hnodes, self.onodes))
        self.activation_func = lambda x: special.expit(x)

        pass

    def train(self, input_list, target_list):
        inputs = np.array(input_list, ndmin=2).T
        target_label = np.array(target_list, ndmin=2).T

        hidden_input = np.dot(self.w1, inputs)
        hidden_output = self.activation_func(hidden_input)

        final_input = np.dot(self.w2, hidden_output)
        final_output = self.activation_func(final_input)

        output_errors = target_label - final_output
        hidden_errors = np.dot(self.w2, output_errors)

        # update the weights between hidden and output
        self.w2 += self.lr * np.dot(output_errors * final_output * (1 - final_output), hidden_output)

        # update the weights between input and hidden
        self.w1 += self.lr * np.dot(hidden_errors * hidden_output * (1 - hidden_output), inputs)

    def query(self, input_list):
        inputs = np.array(input_list, ndmin=2).T

        hidden_input = np.dot(self.w1, inputs)
        hidden_output = self.activation_func(hidden_input)

        final_input = np.dot(self.w2, hidden_output)
        final_output = self.activation_func(final_input)

        return final_output

train_file = open('mnist_train_100.csv', 'r', encoding="utf-8")
train_data = train_file.readlines()
train_file.close()

target_label = []
for i in range(len(train_data)):
    
