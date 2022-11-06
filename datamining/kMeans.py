import numpy as np
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import ipywidgets as widgets
figure_format
#%config InlineBackend.figure_format = 'svg' # matplotlib magic
np.random.seed(1337) # seeds help with reproducible results

iris = load_iris()
#print(iris.keys()) => ['data', 'target', 'frame', 'target_names', 'DESCR', 'feature_names', 'filename']
data = PCA(n_components=2).fit_transform(iris.data)
#print(iris["data"].shape) => (150, 4)
#print(data.shape) => (150, 2)

k = np.unique(iris.target).shape[0]
#print(k) #=> 3

def init():
    cluster = []
    for i in np.random.choice(data.shape[0],k,replace=False):
        cluster += [data[i]]
    return np.array(cluster)

cluster = init()
#print(cluster) #=> [[ 1.33202444  0.24444088]
                #    [-2.77010243  0.26352753]
                #    [ 1.25850816 -0.17970479]]

def distances(data, centroids):
    dists = np.zeros((data.shape[0],k)) #erzeuge Zielmatrix
    for d,c in np.ndindex(dists.shape): #Gucke auf jedes Data+Cluster-Paar
        dists[d,c] = np.linalg.norm(data[d]-centroids[c])
    return dists
#testdata = np.array([[0,0]]) #bel. viele Punkte
#testcluster = np.array([[1,1],[1,0],[0,1]]) #drei Elemente wegen k=3
#distances(testdata,testcluster) #=> array([[1.41421356, 1.        , 1.        ]])

def compute_assignments(data, centroids):
    dataDists = distances(data, centroids) #Hole Distanzen von jedem Punkt zu jedem Zentrum
    #print(dataDists[:10])
    res = np.array([np.argmin(data) for data in dataDists]) #Setze Zentroiden ein
    return res
#testdata = np.array([[0,0],[0,.5],[0,.51],[0,1],[100,100],[550,550],[600,600]]) #bel. viele Punkte
#testcluster = np.array([[0,0],[0,1],[999,999]]) #drei Elemente wegen k=3
#print(compute_assignments(testdata, testcluster)) #=>array([0, 0, 1, 1, 1, 2, 2])
#testcluster = np.array([[-10,.10],[0,1],[999,999]]) #drei Elemente wegen k=3
#print(compute_assignments(testdata, testcluster)) #=>array([1, 1, 1, 1, 1, 2, 2])

def compute_new_centres(data, assignments, centroids):
    cluster = np.zeros_like(centroids,dtype=float)
    for i in range(k): #Für jeden Cluster
        n = np.sum(np.where(assignments == i,1,0)) #Zähle wie oft er zugewiesen wurde
        summ = np.zeros(data[0].shape) #Erzeuge Summenvariablem, in Form eines Datenpunktes
        for j in range(len(data)): #Probiere alle Datenpunkte und ihre Zuweisungen durch
            if assignments[j] == i: summ += data[j] #Falls Zuweisung akt. Cluster entspricht, addiere Punkt
        cluster[i] = summ/n #Setze neuen Mittelpunkt auf neues Massezentrum
        #print("Cluster:",i,"Anzahl:",n,"Summe der Daten:",summ,"Neuer Mittelpunkt:",summ/n)
    return cluster
#testdata = np.array([[0,0],[0,.5],[0,.51],[0,1],[100,100],[550,550],[600,600]])
#testcluster = np.array([[0,0],[0,1],[999,999]])
#testassignments = np.array([0, 0, 1, 1, 1, 2, 2])
#compute_new_centres(testdata, testassignments, testcluster)

def radius(data, centroids, centroid, assignments): #Berechne Radius eines Clusters
    n = np.sum(np.where(centroid == assignments,1,0)) #Zähle wie oft er zugewiesen wurde
    if n == 0: return 9e99 #Verhindere DivByZero
    poweredDiffs = []
    for j in range(data.shape[0]): #Für jeden Datenpunkt
        if assignments[j]==centroid: #Falls Punkt zum Cluster gehört
            poweredDiffs += [np.power(np.linalg.norm(data[j]-centroids[centroid]),2.)]
    return np.sqrt(np.sum(poweredDiffs)/n)
#testdata = np.array([[0,1],[1,1],[2,1]])
#testcluster = np.array([[1,1],[1,1],[1,1]]) #Müssen 3 sein wegen k=3
#testindex = 0
#testassignments = np.array([0,0,0])
#radius(testdata, testcluster, testindex, testassignments) #=> 0.816496580927726

def db_index(data, centroids, assignments):               
    R = []
    for i in range(k): #Für jeden Cluster
        R += [radius(data,centroids,i,assignments)] #Berechne Radius des Clusters
               
    dists = np.zeros((k,k)) #Erzeuge Distanzen-Array
    for i in range(k): #Für jedes Cluster-Paar (ja auch redundant und reflexiv!)
        for j in range(k):
            dists[i,j] = np.linalg.norm(centroids[i]-centroids[j]) #Berechne Distanz
               
    D = np.zeros((k,k)) #Erzeuge badnessOfSep-Array
    for i in range(k): #Für jedes Cluster-Paar
        for j in range(k):
            D[i,j] = (R[i]+R[j])/(dists[i,j]+1e-10) #Berechne BadnessOfSeparation
           
    worst = []
    for i in range(k): #Für jeden Cluster, füge relevanten "least separated" hinzu
        worst += [D[i,np.argmax(D[i,:])]]
            
    dbIndex = np.sum(worst)/k
    return dbIndex
#db_index(testdata, testcluster, testassignments) #=> 1.4999999999999999e+110

iterations = 20
cluster = init() #Neue Cluster erzeugen

#Logs passender Länge und Format erstellen
aLog = np.zeros((iterations,data.shape[0]))
cLog = np.zeros((iterations,cluster.shape[0],cluster.shape[1]))
dbLog = np.zeros((iterations))

for i in range(iterations):
    assignments = compute_assignments(data, cluster)
    aLog[i] = assignments
    cluster = compute_new_centres(data, assignments, cluster)
    cLog[i] = cluster
    dbLog[i] = db_index(data, cluster, assignments)

#%matplotlib inline
plt.plot(dbLog)
plt.title("Davis-Bouldin Index")
plt.xlabel("Iterationen")
plt.ylabel("Index")
plt.show()

#%matplotlib widget
_, ax = plt.subplots()
    
def plot_clusters(iteration):
    iter_assignments = aLog[iteration]# get current cluster assignments
    iter_centres = cLog[iteration]# get current cluster centres
    ax.clear()
    ax.set_xlabel('Projected x-Value')
    ax.set_ylabel('Projected y-Value')
    ax.set_title('Clusterverteilungen')
    
    for i in range(k): # Plot each cluster
        points = data[iter_assignments == i, :] # get data points belonging to cluster i
        ax.scatter(points[:, 0], points[:, 1], color="C{}".format(i), s=20)
        ax.scatter(iter_centres[i, 0], iter_centres[i, 1], color="C{}".format(i), 
                   marker='s', s=50, edgecolor="black", linewidth=2)

iteraction_slider = widgets.IntSlider(min=0, max=iterations-1, description='Iteration:')
widgets.interact(plot_clusters, iteration=iteraction_slider);
print("ACHTUNG: Durch die folgenden Plots wird dieser deaktiviert, sonst diesen manuell neuladen!")
plt.show()

#%matplotlib inline
_, ax2 = plt.subplots(1,2)
iter_assignments2 = aLog[19]
iter_centres2 = cLog[19]
labels = iris.target
ax2[0].clear()
ax2[0].set_xlabel('Projected x-Value')
ax2[0].set_ylabel('Projected y-Value')
ax2[0].set_title('Clusterverteilungen')
for i in range(k): # Plot each cluster
    points = data[iter_assignments2 == i, :] # get data points belonging to cluster i
    ax2[0].scatter(points[:, 0], points[:, 1], color="C{}".format(i), s=20)
    ax2[0].scatter(iter_centres2[i, 0], iter_centres2[i, 1], color="C{}".format(i), 
                  marker='s', s=50, edgecolor="black", linewidth=2)

ax2[1].clear()
ax2[1].set_xlabel('Projected x-Value')
ax2[1].set_title('Reale Verteilung')
for i in np.unique(labels): # Plot each Labeled-Group
    points = data[labels == i, :] # get data points belonging to cluster i
    ax2[1].scatter(points[:, 0], points[:, 1], color="C{}".format(i), s=20)

plt.show()


from sklearn.datasets import load_digits
from sklearn.cluster import KMeans

digits = load_digits()
#print(digits.keys()) #=> ['data', 'target', 'frame', 'feature_names', 'target_names', 'images', 'DESCR']
#print(digits["data"].shape) #=> (1797, 64)
data2 = PCA(n_components=2).fit_transform(digits.data)
#print(data.shape) #=> (1797, 2)
#plt.scatter(data[:,0],data[:,1])
#plt.show()
k2 = np.unique(digits.target).shape[0]
#print(k2) #=> 10

kmeans = KMeans(n_clusters=k2).fit(data2)
centres = kmeans.cluster_centers_
assignments = kmeans.labels_

#%matplotlib inline
_, ax3 = plt.subplots(1,2)
ax3[0].set_xlabel('Projected x-Value')
ax3[0].set_ylabel('Projected y-Value')
ax3[0].set_title('Clusterverteilungen')
for i in range(k2): # Plot each cluster
    points = data2[assignments == i, :] # get data points belonging to cluster i
    ax3[0].scatter(points[:, 0], points[:, 1], color="C{}".format(i), s=10)
    ax3[0].scatter(centres[i, 0], centres[i, 1], color="C{}".format(i), 
               marker='s', s=50, edgecolor="black", linewidth=2)
    
ax3[1].set_xlabel('Projected x-Value')
ax3[1].set_ylabel('Projected y-Value')
ax3[1].set_title('Reale Verteilung')
target = digits.target
for i in np.unique(target): # Plot each target-group
    points = data2[target == i, :] # get data points belonging to cluster i
    ax3[1].scatter(points[:, 0], points[:, 1], color="C{}".format(i), s=10)

plt.show()
