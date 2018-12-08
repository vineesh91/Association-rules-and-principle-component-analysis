import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


def covariance_mat(X):

    mean_vec = X.mean()
    norm_data = X - mean_vec
    covar_mat = (norm_data.T.dot(norm_data))/(norm_data.shape[0] - 1)
    return covar_mat, norm_data


def eigen_value_method1(X):

    eign_val, eign_vec = np.linalg.eig(X)
    return eign_val, eign_vec


def svd_method2(X):

    eign_vec, eign_val, _ = np.linalg.svd(X.T, full_matrices=True)
    return eign_val, eign_vec


def tsne_method3(file_name):
    features_embedded = TSNE(n_components=2).fit_transform(features)
    scatter_plot_fn(features_embedded, file_name)


def eigen_svd_main(cov_mat,norm_data,choose_method, file_name, features):
    if choose_method == 1:
        eign_val, eign_vec = eigen_value_method1(cov_mat)
    else:
        eign_val, eign_vec = svd_method2(norm_data)
        #eign_val, eign_vec = svd_method2(features)

    #Making list of eigen value and corresponding eigen vector
    eign_list = [[eign_val[i],eign_vec[:,i]] for i in range(0,len(eign_val))]

    #Sorting the list so that we can get the highest eigen values which has the maximum variance in the data
    eign_list.sort(key=lambda x: x[0], reverse=True)

    #Reducing to 2 dimensions
    red_dim = 2

    #Filtering only the required eigen values and vectors
    eign_list = eign_list[0:red_dim]

    #saving the first eigen vector to an array
    new_dim = np.asarray(eign_list[0][1].reshape(prev_dim,1))

    #getting the rest of the eigen vectors and stacking them together
    for i in range(1, red_dim):
        new_dim = np.hstack((new_dim, eign_list[i][1].reshape(prev_dim,1)))


    #now the initial standardized matrix is multipllied with the new_dim matrix too get the new dimensional matrix Y
    y = norm_data.dot(new_dim)
    #y = features.dot(new_dim)
    scatter_plot_fn(y, file_name)



def scatter_plot_fn(input, file_name):
    #converting input into a dataframe and concatentaing the disease_class values(as column) to do scatter plot
    df = pd.DataFrame(input)
    df = pd.concat([df, disease_class], axis=1)

    #grouping by the disease name for the ease of plotting
    groups = df.groupby(df.iloc[:,-1])

    fig, ax = plt.subplots()
    for diseas_name, group in groups:
        ax.plot(group[0], group[1], marker='o', linestyle='', ms=12, label=diseas_name)
    ax.legend()
    plt.title(file_name + ' scatter plot')
    plt.show()


file_name = "pca_a.txt"
features = pd.read_csv(file_name, sep="\t", header=None)

disease_class = features.iloc[:,-1]
features = features.iloc[:,:-1]
samples, prev_dim = features.shape

#choose_method = 1 means eigen value method, =2 means svd method, = 3 means t-sne method
choose_method = 1

if choose_method == 1 or choose_method == 2:
    cov_mat, norm_data = covariance_mat(features)
    eigen_svd_main(cov_mat, norm_data, choose_method, file_name, features)
else:
    tsne_method3(file_name)

