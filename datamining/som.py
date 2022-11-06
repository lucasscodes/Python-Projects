
# Load libraries
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.preprocessing import StandardScaler

np.random.seed(42)

iris = datasets.load_iris()
iris_data = iris.data
#iris.keys() #=> ['data', 'target', 'frame', 'target_names', 'DESCR', 'feature_names', 'filename']

print(iris.DESCR)

scaler = StandardScaler()
iris_scaled = scaler.fit_transform(iris_data)

iris_data[0]

iris_scaled[0]

class SOM:
    
    
    def __init__(self, rows, columns, dim, lr): # Map Initialization (10, 10, iris_data.shape[1]=4, 0.5)
        self.size = rows * columns
        self.sigma = 1
        self.nodes = np.random.normal(size=(rows * columns, dim)) #=> shape(100,4)
        
        # learning rate
        self.lr = lr
        
    def neighborhood_function(self, v, n_b):
        res = np.linalg.norm(v-self.nodes[n_b]) #hole Distanz
        res = -(np.power(res,2)/(2*np.power(self.sigma,2))) #berechne Term in -exp(...) fertig
        res = -(np.exp(res)) #berechne äußeres -exp() auch
        return res
    
    def find_winner(self, x):
        dists = np.linalg.norm(x-self.nodes,axis=1)
        n_b = np.argmin(dists)
        return n_b
    
    def update_network(self, x, n_b):
        n = self.nodes.shape[0]
        for i in range(n): #Für jeden Knoten
            #Passe nach Formel an
            self.nodes[i] = (self.nodes[i]+
                             self.lr*
                             self.neighborhood_function(self.nodes[i],n_b)*
                             np.linalg.norm(x-self.nodes[i]))
     
    def plot(self, title):
        # definitions for the axes
        left, width = 0.1, 0.65
        bottom, height = 0.1, 0.65
        spacing = 0.005

        rect_scatter = [left, bottom, width, height]
        rect_histx = [left, bottom + height + spacing, width, 0.2]
        rect_histy = [left + width + spacing, bottom, 0.2, height]

        # start with a rectangular Figure
        plt.figure(figsize=(8, 8))
        #plt.title(title)

        ax_scatter = plt.axes(rect_scatter)
        ax_scatter.tick_params(direction='in', top=True, right=True)
        ax_histx = plt.axes(rect_histx)
        ax_histx.tick_params(direction='in', labelbottom=False)
        ax_histy = plt.axes(rect_histy)
        ax_histy.tick_params(direction='in', labelleft=False)

        # the scatter plot:
        ax_scatter.scatter(self.nodes[:,0], self.nodes[:,1], s=5)

        # now determine nice limits by hand:
        binwidth = 0.05
        lim = np.ceil(np.abs([self.nodes[:,0], self.nodes[:,1]]).max() / binwidth) * binwidth
        ax_scatter.set_xlim((-lim, lim))
        ax_scatter.set_ylim((-lim, lim))
        
        ax_scatter.set_xlabel("Erste Dimension")
        ax_scatter.set_ylabel("Zweite Dimension")

        bins = np.arange(-lim, lim + binwidth, binwidth)
        ax_histx.hist(self.nodes[:,0], bins=bins)
        ax_histy.hist(self.nodes[:,1], bins=bins, orientation='horizontal')

        ax_histx.set_xlim(ax_scatter.get_xlim())
        ax_histy.set_ylim(ax_scatter.get_ylim())
        
        ax_histx.set_title(title)
        
        plt.show()

# Step 1: Initialize Network (10 x 10 nodes, learning rate 0.5)
xm,ym = 100,100
som = SOM(xm, ym, iris_data.shape[1], 2)
som.plot("Alte Karte")
plt.show()
print("Berechne",(iris.data.shape[0]*xm*ym),"neue Knoten...")

# Step 2: Get Input
for x in iris_scaled:
    
    # Step 3: Find Winner
    n_b = som.find_winner(x)
    
    # Step 4: Update winner and neighborhood
    som.update_network(x, n_b)
    
    # Step 5: Adjust neighborhood size
    som.sigma /= 1.1
    
# Step 6: Plot network
som.plot("Neue Karte")

plt.show()

