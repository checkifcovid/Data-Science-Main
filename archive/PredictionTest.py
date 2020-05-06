# This file visualizes the centroids of a given dataset based on the lat and long coordinates.
import os
import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import geodesic
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


# Load the data
# Unsure where this data is coming from...
file_path = pathlib.Path('archive/data/out.csv')

# assert os.path.isfile(file_path)
data = pd.read_csv(file_path, sep=',') # not useful name

# Only using location?
data = data[["latitude","longitude"]]

def clean_dataset(df):
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    return df[indices_to_keep].astype(np.float64)


# Not sure what this is doing without any `=`
# clean_dataset(data)


Kmean = KMeans(n_clusters=3)
Kmean.fit(data)

centroids = Kmean.cluster_centers_
print(centroids)


plt.scatter(data['latitude'], data['longitude'], c= Kmean.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.show()


distortions = []
for i in range(1, 30):
    km = KMeans(
        n_clusters=i, init='random',
        n_init=10, max_iter=300,
        tol=1e-04, random_state=0
    )
    km.fit(data)
    distortions.append(km.inertia_)

# Visualize results
plt.plot(range(1, 30), distortions, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Distortion')
plt.yscale('log')
plt.show()


pd.Series(distortions).diff()[5:].idxmax()


pd.Series(distortions).diff().abs().plot()
plt.yscale('log')


Kmean = KMeans(n_clusters=26)
Kmean.fit(data)
centroids = Kmean.cluster_centers_
print(centroids)
plt.scatter(data['latitude'], data['longitude'], c= Kmean.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.show()


def findDistance(coords_1,coords_2):
    return geopy.distance.geodesic(coords_1, coords_2).km

df_new = data.copy(deep=True)
for i,x in enumerate(centroids):
    col_name = f'cluster_distance_{i}'
    df_new[col_name] = df_new[['latitude','longitude']].apply(lambda arr: findDistance(arr, x),axis=1)
df_new
findDistance(centroids[0],centroids[1])
