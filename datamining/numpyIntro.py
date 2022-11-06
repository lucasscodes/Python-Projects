import numpy as np
#pip install numpy==1.20.2

sevens_vector = np.ones(3) * 7
print(sevens_vector)

print(sevens_vector.shape)

sevens_matrix = np.ones((4,3)) * 7
print(sevens_matrix)

print(sevens_matrix.shape)

l = [[1,2,3], [4,5,6]]
x = np.array(l)
print(x)

x[1,1] = 1337
print(x)

# sample matrix a
a = np.array([[2, 3.2, 5.5, -6.4, -2.2, 2.4], [1, 22, 4, 0.1, 5.3, -9],
                [3, 1, 2.1, 21, 1.1, -2]])
print(a)

# sample matrix b
b = np.array([range(6), range(10, 16)])
print(b)

sol_4_1 = a[1]
print(sol_4_1)

sol_4_2 = a[-(len(a)-1):]
print(sol_4_2)

sol_4_3 = a[:,4] 
print(sol_4_3)

sol_4_4 = a[1:,2]
print(sol_4_4)

sol_4_5 = np.absolute(a)
print(sol_4_5)

sol_4_6 = np.shape(b)
print(sol_4_6)

sol_4_7 = np.max(b)
print(sol_4_7)

sol_4_8 = np.min(b)
print(sol_4_8)

sol_4_9 = np.transpose(b)
print(sol_4_9)


