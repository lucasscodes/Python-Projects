#https://en.wikipedia.org/wiki/Ensemble_learning

# Load libraries
import numpy as np
from sklearn import datasets
from sklearn import metrics
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier

# Additional imports here, if needed
import matplotlib.pyplot as plt

np.random.seed(42)

digits = datasets.load_digits()

print("\nLabels und Vorkommensanzahl:")
print(np.reshape(np.unique(digits["target"], return_counts=True),(2,10)))
print("\nBeschreibung:")
print(digits.DESCR)

for i in range(3):
    plt.title(digits["target"][i+1600])
    plt.imshow(digits["data"][i+1600].reshape(8,8),cmap="gray_r")
    plt.show()

print("\n",digits["feature_names"])


X = digits["data"]
y = digits["target"]

n=3
offset = int(np.random.rand()*(len(y)-1)-n)

for i in range(n):
    plt.title(str(i+offset)+":"+str(y[i+offset]))
    plt.imshow(X[i+offset].reshape(8,8),cmap="gray_r")
    plt.show()

#Berechne Schnittstelle
n = int((len(y)-1)*.7)

X_train = X[:n+1]
X_test = X[n+1:]
y_train = y[:n+1] 
y_test = y[n+1:]

bc = BaggingClassifier(n_estimators=256,max_samples=1.5*(256/len(y_train)))

bc_model = bc.fit(X_train,y_train)

y_pred = bc_model.predict(X_test)

bc_accuracy = bc_model.score(X_test,y_test)#np.sum(np.equal(y_pred,y_test))/y_test.size

print("Accuracy of Bagging Classifier on Digits Dataset: %.4f" % bc_accuracy)

abc = AdaBoostClassifier(n_estimators=512,learning_rate=3.5,random_state=0)

abc_model = abc.fit(X_train,y_train)

y_pred = abc_model.predict(X_test)

abc_accuracy = abc_model.score(X_test,y_test)#np.sum(np.equal(y_pred,y_test))/y_test.size

print("Accuracy of AdaBoost Classifier on Digits Dataset: %.4f" % abc_accuracy)

