# import libraries
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline
from sklearn import datasets

boston = datasets.load_boston()

data = np.concatenate((boston["data"], boston["target"].reshape(-1,1)),
                      axis=1)
print(data.shape)
names = list(boston["feature_names"]) + ["MEDV"]
print(names)
corr = np.corrcoef(data, rowvar=False)
print(corr.shape)
print(corr)

plt.imshow(corr)
plt.xticks(np.arange(len(names)), labels=names, rotation=45)
plt.yticks(np.arange(len(names)), labels=names)
plt.title("Correlation of features")
plt.colorbar()
plt.show()

print(names.index("RM"))
x = data[:,names.index("RM")]
medv = boston["target"]

#print(x.shape,data[:,13:14].shape)
#print(data[:,13:14])
plt.scatter(x, data[:,names.index("MEDV")])
plt.title("RM-MEDV-Correlation")
plt.xlabel("average number of rooms per dwelling")
plt.ylabel("Median value of owner-occupied homes in $1000's")
plt.show()

y = data[:,names.index("MEDV")]

x_mean = np.mean(x)
y_mean = np.mean(y)
#print(x_mean, y_mean)

beta_one = np.sum((x-x_mean)*(y-y_mean))/np.sum((x-x_mean)*(x-x_mean))
print(beta_one)

beta_zero = y_mean-beta_one*x_mean
print(beta_zero)

def regress(x):
    return beta_zero+beta_one*x
print(regress(8))

plt.plot(x, regress(x), color="black")
plt.scatter(x, y)
plt.title("RM-MEDV-Correlation")
plt.xlabel("average number of rooms per dwelling")
plt.ylabel("Median value of owner-occupied homes in $1000's")
plt.show()


