import math
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline
from sklearn import datasets

iris = datasets.load_iris()

features = iris.feature_names
print(features)

classes = iris.target_names
print(classes)

print(iris.DESCR)

from sklearn import tree

X, y = iris.data, iris.target
dt = tree.DecisionTreeClassifier(criterion='entropy', random_state=42)
dt = dt.fit(X, y)

tree.plot_tree(dt)
plt.show()

plt.figure(figsize=(30, 10))
_ = tree.plot_tree(dt, feature_names=features, class_names=classes, filled=True, fontsize=14)
plt.show()

def entropy(value_arr):
    (_, counts) = np.unique(value_arr, return_counts=True)

    entropy = 0.0
    for count in counts:
        p = count / len(value_arr)
        entropy -= p * math.log2(p)
    return entropy

def avg_info(attr_values, labels):
    (partitions, counts) = np.unique(attr_values, return_counts=True)

    avg_info = 0.0

    for (attr, count) in zip(partitions, counts):
        related_labels = []
        for i in range(0, len(labels)):
            if attr_values[i] == attr:
                related_labels.append(labels[i])

        avg_info += count / len(attr_values) * entropy(related_labels)

    return avg_info
print(avg_info(np.array([1,1,1,1,1,2,2,2,2,3,3,3,3,3]),
               np.array([True,True,False,False,False,True,True,True,True,True,True,True,False,False])))
print("Entspricht Lec.07,p.35,Info_age(D) = 0.694")

def info_gain(info, attr_info):
    return np.vectorize(lambda avg_info: info - avg_info)(attr_info)

def get_split_attr(gain_arr):
    return np.argmax(gain_arr)

#
# TEST CODE / MAIN FUNCTION
#


# Step 1: Calculate Information (Entropy)
info = entropy(iris.target)

# Step 2: Calculate Average Information of all Attributes
attr_info = [avg_info(attr, iris.target) for attr in iris.data.T]

# Step 3: Calculate Information Gain
gain = info_gain(info, attr_info)

# Step 4: Determine Split Attribute based on Information Gain
attr_pos = get_split_attr(gain)
attr_name = iris.feature_names[attr_pos]

# Step 5: Some fancy output for debugging
print('The next attribute to use for splitting is {}.'.format(attr_name))