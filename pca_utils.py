#from sklearn.decomposition import PCA
#def fit_pca(X):

 #   pca = PCA(
  #      n_components=2
   # )
    #return pca.fit_transform(X)
    
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def plot_pca(X, labels):

    pca = PCA(
        n_components=2
    )

    X_pca = pca.fit_transform(X)

    plt.figure(
        figsize=(8,6)
    )

    for label in set(labels):

        idx = labels == label

        plt.scatter(

            X_pca[idx,0],

            X_pca[idx,1],

            label=label

        )

    plt.legend()

    plt.title(
        "PCA Mineral Space"
    )

    plt.show()