import pdb
import time
import numpy as np
import itertools
from scipy.sparse import csr_matrix, issparse
from scipy.spatial.distance import pdist, squareform
from scipy.sparse.csgraph import floyd_warshall, shortest_path
from sklearn.neighbors import NearestNeighbors
from sklearn.manifold import Isomap
import multiprocess as mp
import os
import pickle

def path_exists(path):
    return os.path.exists(path) or os.path.islink(path)

def makedirs(dirpath):
    if path_exists(dirpath):
        return
    os.makedirs(dirpath)

def read(fpath, verbose=True):
    if not path_exists(fpath):
        if verbose:
            print(fpath, 'does not exist.')
        return None
    with open(fpath, "rb") as f:
        data = pickle.load(f)
    if verbose:
        print('Read data from', fpath, flush=True)
    return data
    
def save(dirpath, fname, data, verbose=True):
    if not path_exists(dirpath):
        os.makedirs(dirpath)
    fpath = dirpath + '/' + fname
    with open(fpath, "wb") as f:
        pickle.dump(data, f)
    if verbose:
        print('Saved data in', fpath, flush=True)
        
        
def shortest_paths(X, n_nbrs):
    nbrs = NearestNeighbors(n_neighbors=n_nbrs).fit(X)
    knn_graph = nbrs.kneighbors_graph(mode='distance')
    dist_matrix, predecessors = shortest_path(knn_graph, return_predecessors=True, directed=False)
    return dist_matrix, predecessors

def print_log(s, log_time, local_start_time, global_start_time):
    print(s)
    if log_time:
        print('##############################')
        print('Time elapsed from last time log: %0.1f seconds' %(time.time()-local_start_time))
        print('Total time elapsed: %0.1f seconds' %(time.time()-global_start_time))
        print('##############################')
    return time.time()

class Param:
    def __init__(self,
                 algo = 'LPCA',
                 **kwargs):
        self.algo = algo
        self.T = None
        self.v = None
        self.b = None
        # Following variables are
        # initialized externally
        # i.e. by the caller
        self.zeta = None
        self.noise_seed = None
        self.noise_var = 0
        
        # For LDLE
        self.Psi_gamma = None
        self.Psi_i = None
        self.phi = None
        
        # For LPCA and its variants
        self.Psi = None
        self.mu = None
        self.X = None
        self.y = None
        
        self.add_dim = False
        
        # For ISOMAP
        self.isomap = None
        
    def eval_(self, opts):
        k = opts['view_index']
        mask = opts['data_mask']
        
        if self.algo == 'LDLE':
            temp = self.Psi_gamma[k,:][np.newaxis,:]*self.phi[np.ix_(mask,self.Psi_i[k,:])]
            n = self.phi.shape[0]
        elif self.algo == 'LPCA':
            temp = np.dot(self.X[mask,:]-self.mu[k,:][np.newaxis,:],self.Psi[k,:,:])
            n = self.X.shape[0]
        elif self.algo == 'LISOMAP':
            temp = self.isomap[k].transform(self.X[mask,:])
        
        if self.noise_var:
            np.random.seed(self.noise_seed[k])
            temp2 = np.random.normal(0, self.noise_var, (n, temp.shape[1]))
            temp = temp + temp2[mask,:]
            
        if self.add_dim:
            temp = np.concatenate([temp,np.zeros((temp.shape[0],1))], axis=1)
        
        if self.b is None:
            return temp
        else:
            temp = self.b[k]*temp
            if self.T is not None:
                temp = np.dot(temp, self.T[k,:,:])
            if self.v is not None:
                temp = temp + self.v[[k],:]
            return temp
    
    def alignment_wts(self, opts):
        beta = opts['beta']
        if beta is None:
            return None
        k = opts['view_index']
        mask = opts['data_mask']
        mu = np.mean(self.X[mask,:], axis=0)
        temp = self.X[mask,:] - mu[None,:]
        w = -np.linalg.norm(temp, 1, axis=1)/beta
        return w
        #p = np.exp(w - np.max(w))
        #p *= (temp.shape[0]/np.sum(p))
        #return p
    def repulsion_wts(self, opts):
        beta = opts['beta']
        if beta is None:
            return None
        k = opts['pt_index']
        far_off_pts = opts['repelling_pts_indices']
        if self.y is not None:
            temp = self.y[far_off_pts,:] - self.y[k,:][None,:]
            w = np.linalg.norm(temp, 2, axis=1)**2
            #temp0 = self.X[far_off_pts,:] - self.X[k,:][None,:]
            #w0 = np.linalg.norm(temp0, 2, axis=1)**2
            #p = 1.0*((w-w0)<0)
            p = 1/(w + 1e-12)
        else:
            p = np.ones(len(far_off_pts))
        return p


# includes self as the first neighbor
# data is either X or distance matrix d_e
def nearest_neighbors(data, k_nn, metric, n_jobs=-1, sort_results=True):
    n = data.shape[0]
    if k_nn > 1:
        neigh = NearestNeighbors(n_neighbors=k_nn-1, metric=metric, n_jobs=n_jobs)
        neigh.fit(data)
        neigh_dist, neigh_ind = neigh.kneighbors()
        neigh_dist = np.insert(neigh_dist, 0, np.zeros(n), axis=1)
        neigh_ind = np.insert(neigh_ind, 0, np.arange(n), axis=1)
        if sort_results:
            inds = np.argsort(neigh_dist, axis=-1)
            for i in range(neigh_ind.shape[0]):
                neigh_ind[i,:] = neigh_ind[i,inds[i,:]]
                neigh_dist[i,:] = neigh_dist[i,inds[i,:]]
    else:
        neigh_dist = np.zeros((n,1))
        neigh_ind = np.arange(n).reshape((n,1)).astype('int')
    return neigh_dist, neigh_ind
            
def sparse_matrix(neigh_ind, neigh_dist):
    if neigh_ind.dtype == 'object':
        row_inds = []
        col_inds = []
        data = []
        for k in range(neigh_ind.shape[0]):
            row_inds.append(np.repeat(k, neigh_ind[k].shape[0]).tolist())
            col_inds.append(neigh_ind[k].tolist())
            data.append(neigh_dist[k].tolist())
        row_inds = list(itertools.chain.from_iterable(row_inds))
        col_inds = list(itertools.chain.from_iterable(col_inds))
        data = list(itertools.chain.from_iterable(data))
    else:
        row_inds = np.repeat(np.arange(neigh_dist.shape[0]), neigh_dist.shape[1])
        col_inds = neigh_ind.flatten()
        data = neigh_dist.flatten()
    return csr_matrix((data, (row_inds, col_inds)))

def to_dense(x):
    if issparse(x):
        return x.toarray()
    else:
        return x
    
def compute_zeta(d_e_mask0, Psi_k_mask):
    d_e_mask = to_dense(d_e_mask0)
    if d_e_mask.shape[0]==1:
        return 1
    d_e_mask_ = squareform(d_e_mask)
    mask = d_e_mask_!=0
    d_e_mask_ = d_e_mask_[mask]
    disc_lip_const = pdist(Psi_k_mask)[mask]/d_e_mask_
    return np.max(disc_lip_const)/(np.min(disc_lip_const) + 1e-12)


def custom_procrustes(X, Y, reflection='best'):
    n,m = X.shape
    ny,my = Y.shape

    muX = X.mean(0)
    muY = Y.mean(0)

    X0 = X - muX
    Y0 = Y - muY

    ssX = (X0**2.).sum()
    ssY = (Y0**2.).sum()

    # centred Frobenius norm
    normX = np.sqrt(ssX)
    normY = np.sqrt(ssY)

    # scale to equal (unit) norm
    X0 /= normX
    Y0 /= normY

    if my < m:
        Y0 = np.concatenate((Y0, np.zeros(n, m-my)),0)

    # optimum rotation matrix of Y
    A = np.dot(X0.T, Y0)
    U,s,Vt = np.linalg.svd(A,full_matrices=False)
    V = Vt.T
    T = np.dot(V, U.T)

    if reflection != 'best':

        # does the current solution use a reflection?
        have_reflection = np.linalg.det(T) < 0

        # if that's not what was specified, force another reflection
        if reflection != have_reflection:
            V[:,-1] *= -1
            s[-1] *= -1
            T = np.dot(V, U.T)

    # transformation matrix
    if my < m:
        T = T[:my,:]
    c = muX - np.dot(muY, T)
   
    return T, c

# Solves for T, v s.t. T, v = argmin_{R,w)||AR + w - B||_F^2
# Here A and B have same shape n x d, T is d x d and v is 1 x d
def procrustes(A, B):
    T, c = custom_procrustes(B,A)
    return T, c

def ixmax(x, k=0, idx=None):
    col = x[idx, k] if idx is not None else x[:, k]
    z = np.where(col == col.max())[0]
    return z if idx is None else idx[z]

def lexargmax(x):
    idx = None
    for k in range(x.shape[1]):
        idx = ixmax(x, k, idx)
        if len(idx) < 2:
            break
    return idx[0]

def compute_distortion_at(y_d_e, s_d_e):
    scale_factors = (y_d_e+1e-12)/(s_d_e+1e-12)
    mask = np.ones(scale_factors.shape, dtype=bool)
    np.fill_diagonal(mask, 0)
    max_distortion = np.max(scale_factors[mask])/np.min(scale_factors[mask])
    print('Max distortion is:', max_distortion, flush=True)
    n = y_d_e.shape[0]
    distortion_at = np.zeros(n)
    mask = np.ones(n, dtype=bool)
    for i in range(n):
        mask[i] = 0
        distortion_at[i] = np.max(scale_factors[i,mask])/np.min(scale_factors[i,mask])
        mask[i] = 1
    return distortion_at, max_distortion

def compute_prctile_distortion_at(y_d_e, s_d_e, prctile=50):
    scale_factors = (y_d_e+1e-12)/(s_d_e+1e-12)
    np.fill_diagonal(scale_factors,1)
    max_distortion = np.percentile(scale_factors, prctile)/np.percentile(scale_factors, 100-prctile)
    print('Max distortion is:', max_distortion, flush=True)
    n = y_d_e.shape[0]
    distortion_at = np.zeros(n)
    for i in range(n):
        distortion_at[i] = np.percentile(scale_factors[i,:], prctile)/np.percentile(scale_factors[i,:], 100-prctile)
    return distortion_at, max_distortion

def get_global_distortion_info(ldle=None, ys=None, names=None, include_ldle=True, s_d_e=None):
    assert ((ldle is not None) or (include_ldle is False)), 'error: ldle is None and include_ldle is True.'
    if s_d_e is None:
        print('Using Floyd Warshall on the data', flush=True)
        s_d_e = scipy.sparse.csgraph.floyd_warshall(ldle.d_e, directed=False)
    df_dict = {}
    max_dict = {}
    if include_ldle:
        print('Computing pairwise Euclidean distances in the LDLE embedding', flush=True)
        y_ldle_d_e = ldle.GlobalViews.compute_pwise_dist_in_embedding(s_d_e, ldle.GlobalViews.y_final,
                                                                    ldle.IntermedViews.Utilde,
                                                                    ldle.IntermedViews.C, ldle.global_opts,
                                                                    ldle.GlobalViews.n_Utilde_Utilde)
        df_dict['LDLE'] = compute_distortion_at(y_ldle_d_e, s_d_e)

    for i in range(len(ys)):
        print('Computing pairwise Euclidean distances in the', names[i], 'embedding.', flush=True)
        y_d_e = squareform(pdist(ys[i]))
        df_dict[names[i]], max_dict[names[i]] = compute_distortion_at(y_d_e, s_d_e)
    return df_dict, max_dict, s_d_e

def get_weak_global_distortion_info(ldle=None, ys=None, names=None, include_ldle=True,
                                    s_d_e=None, pred=None, verbose=True, n_proc=16):
    assert ((ldle is not None) or (include_ldle is False)), 'error: ldle is None and include_ldle is True.'
    if s_d_e is None:
        print('Using Floyd Warshall on the data', flush=True)
        s_d_e, pred = scipy.sparse.csgraph.floyd_warshall(ldle.d_e, directed=False, return_predecessors=True)
    df_dict = {}
    max_dist = {}
    if include_ldle:
        print('Computing pairwise Euclidean distances in the LDLE embedding', flush=True)
        y_ldle_d_e = ldle.GlobalViews.compute_pwise_dist_in_embedding(s_d_e, ldle.IntermedViews.Utilde,
                                                                    ldle.IntermedViews.C, ldle.global_opts,
                                                                    ldle.GlobalViews.n_Utilde_Utilde,
                                                                    y = ldle.GlobalViews.y_final)
        df_dict['LDLE'] = compute_distortion_at(y_ldle_d_e, s_d_e)

    for s in range(len(ys)):
        print('Computing pairwise Euclidean distances in the', names[s], 'embedding.', flush=True)
        y_d_e = squareform(pdist(ys[s]))
        n = ys[s].shape[0]
        y_d_e2 = np.zeros((n,n))
        
        def target_proc(start_ind, end_ind, q_, y_d_e, s_d_e, pred):
            def get_path_length(i, j):
                path_length = 0
                k = j
                while pred[i, k] != -9999:
                    path_length += y_d_e[k, pred[i, k]]
                    k = pred[i, k]
                return path_length
            
            y_d_e2_ = np.zeros((end_ind-start_ind+1, n))
            for i in range(start_ind, end_ind):
                for j in range(i+1,n):
                    y_d_e2_[i-start_ind,j] = get_path_length(i,j)
                    
            q_.put((start_ind, end_ind, y_d_e2_))
                   
        q_ = mp.Queue()
        chunk_sz = int((n*(n-1))/(2*n_proc))
        proc = []
        start_ind = 0
        end_ind = 1
        for p_num in range(n_proc):
            if p_num == n_proc-1:
                end_ind = n
            else:
                while (n-1)*(end_ind-start_ind) - (end_ind*(end_ind-1))/2 + (start_ind*(start_ind-1))/2 < chunk_sz:
                    end_ind += 1
                    
            proc.append(mp.Process(target=target_proc,
                                   args=(start_ind, end_ind, q_,y_d_e, s_d_e, pred),
                                   daemon=True))
            proc[-1].start()
            start_ind = end_ind
        
        print('All processes started', flush=True)
        for p_num in range(n_proc):
            start_ind, end_ind, y_d_e2_ = q_.get()
            for i in range(start_ind, end_ind):
                y_d_e2[i,i+1:] = y_d_e2_[i-start_ind,i+1:]
                y_d_e2[i+1:,i] = y_d_e2[i,i+1:]

        q_.close()
        for p_num in range(n_proc):
            proc[p_num].join()
            
#         def get_path_length(i, j):
#             path_length = 0
#             k = j
#             while pred[i, k] != -9999:
#                 path_length += y_d_e[k, pred[i, k]]
#                 k = pred[i, k]
#             return path_length
        
#         print_freq = n//10
#         for i in range(n):
#             if verbose and np.mod(i, print_freq) == 0:
#                  print('Processed', i, 'points.', flush=True)
#             for j in range(i+1,n):
#                 y_d_e2[i,j] = get_path_length(i, j)
#                 y_d_e2[j,i] = y_d_e2[i,j]
        
        df_dict[names[s]], max_dist[names[s]] = compute_distortion_at(y_d_e2, s_d_e)
        print('done', flush=True)
    return df_dict, max_dist, s_d_e

# def get_path_lengths_in_embedding_space(s_d_e, pred, y_d_e, verbose=True):
#     def get_path_length(i, j):
#         path_length = 0
#         k = j
#         while pred[i, k] != -9999:
#             path_length += y_d_e[k, pred[i, k]]
#             k = pred[i, k]
#         return path_length
        
#     n = y_d_e.shape[0]
#     y_d_e2 = np.zeros((n,n))
#     print_freq = n//10
#     for i in range(n):
#         if verbose and np.mod(i, print_freq) == 0:
#             print('Processed', i, 'points.', flush=True)
#         # TODO: make this faster
#         for j in range(i+1,n):
#             y_d_e2[i,j] = get_path_length(i, j)
#             y_d_e2[j,i] = y_d_e2[i,j]
#     return y_d_e2

def get_path_lengths_in_embedding_space(s_d_e, pred, y_d_e, n_proc=8, verbose=True):
    n = pred.shape[0]
    inds = np.arange(n)
    y_d_e2 = np.zeros((n,n))
    
    def target_proc(pairs_to_proc, start_ind, end_ind, q_, y_d_e, s_d_e, pred):
        def get_path_length(i, j):
            path_length = 0
            k = j
            while pred[i, k] != -9999:
                path_length += y_d_e[k, pred[i, k]]
                k = pred[i, k]
            return path_length

        my_data = np.zeros(end_ind-start_ind)
        for ind in range(start_ind, end_ind):
            i,j = pairs_to_proc[ind]
            my_data[ind-start_ind] = get_path_length(i,j)

        q_.put((start_ind, end_ind, my_data))

    pairs_to_proc = list(itertools.combinations(np.arange(n), 2))
    q_ = mp.Queue()
    chunk_sz = len(pairs_to_proc)//n_proc
    proc = []
    start_ind = 0
    end_ind = 1
    for p_num in range(n_proc):
        if p_num == n_proc-1:
            end_ind = len(pairs_to_proc)
        else:
            end_ind = (p_num+1)*chunk_sz

        proc.append(mp.Process(target=target_proc,
                               args=(pairs_to_proc, start_ind, end_ind, q_, y_d_e, s_d_e, pred),
                               daemon=True))
        proc[-1].start()
        start_ind = end_ind

    print('All processes started', flush=True)
    for p_num in range(n_proc):
        start_ind, end_ind, y_d_e2_ = q_.get()
        for ind in range(start_ind, end_ind):
            i,j = pairs_to_proc[ind]
            y_d_e2[i,j] = y_d_e2_[ind-start_ind]
            y_d_e2[j,i] = y_d_e2[i,j]

    q_.close()
    for p_num in range(n_proc):
        proc[p_num].join()
    
    return y_d_e2