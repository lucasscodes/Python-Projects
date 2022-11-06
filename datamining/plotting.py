import matplotlib.pyplot as plt
import numpy as np #numpy will always have our back

#pip install scikit-learn==0.24.1

from sklearn import datasets
boston = datasets.load_boston()

print(boston["data"].shape)

print(boston["feature_names"])

print(boston["DESCR"])

#print(boston["data"][:,5:6].shape)
rm = boston["data"][:,5:6]
#rm = boston["data"][:,5]
#print(rm)
print(rm.shape)

# attribute type: its a avg_counter => ratio
#print(rm)
rm_mean =  np.mean(rm)
print(rm_mean)
rm_median = np.median(rm)
print(rm_median)
rm_max =  np.max(rm)
rm_min =  np.min(rm)
print(rm_min, rm_max)
#print(rm-rm_mean)
#print(np.array([1,2,3,4])*np.array([1,2,3,4]))
rm_var =  np.var(rm)
print(rm_var)

plt.hist(rm,)# 6)
plt.xlabel('avgRooms')
plt.ylabel('Percentile')
plt.title('Histogram of avgRooms')
plt.show()

# it looks like a gaussian distribution

plt.boxplot(rm)#, 0, "")
plt.title("Box and Whiskers Plot")
plt.ylabel("avgRooms")
plt.xlabel("Distribution")
plt.show()

# I get a plot with values between 3.5-9
#the plot contains min=q0, q1, median=q2, q3 & max=q4
#50% of the homes seem to have 5.9-6.6 Rooms with median 6.3

#Dots are outliers

digits = datasets.load_digits()
print(digits.keys())
#print(digits)

print(digits["data"].shape)

print(digits["feature_names"])

im_vec = digits["data"][0,:]
print(im_vec.shape)

im = im_vec.reshape((8,8))
print(im.shape)

plt.imshow(im) #result is "plottingOutput.png"!