# -*- coding: utf-8 -*-
# Name: Don Cruver, Bill O'Keefe
# Date: May 15, 2018
# Course: CPSC51100 - Statistical Programming, Lewis University
# Term: Summer 2018
# Assignment Name: Programming Assignment 3 – Nearest Neighbors

import numpy as np

if __name__ == "__main__":
    print("CPSC-51100, Summer 2018")
    print("NAME: Don Cruver, Bill OKeefe")
    print( "PROGRAMMING ASSIGNMENT #3 \n")


train_file = 'iris-training-data.csv'
test_file = 'iris-testing-data.csv'

# gather necessary data
train_data = np.loadtxt(train_file, delimiter = ",", usecols = (0, 1, 2, 3))
train_classes = np.loadtxt(train_file, delimiter = ",", usecols = (4),
                           dtype = str)
test_data = np.loadtxt(test_file, delimiter = ",", usecols = (0, 1, 2, 3))
test_classes = np.loadtxt(test_file, delimiter = ",", usecols = (4),
                          dtype = str)
predicted_classes = []

def distance(x, y):
    """
    Computes the distance between two vectors, x and y.
    
    params:
        x: vector, floats
        y: vector, floats
    
    returns:
        float
    """
    
    return np.sqrt(np.sum((x-y)**2)) # euclidean distance

for row in test_data:
    # find distance between this row and every row in training
    distances = [distance(row, x) for x in train_data]
    predicted_class = np.argmin(distances) 
    predicted_classes.append(train_classes[predicted_class])

accuracy = ((sum(predicted_classes == test_classes) / test_classes.shape[0]) 
                * 100)

print("#, True, Predicted")
[print(x, y, z) for x, y, z in zip(range(1, 76), test_classes, predicted_classes)]
print("Accuracy: %f%% " % accuracy)


