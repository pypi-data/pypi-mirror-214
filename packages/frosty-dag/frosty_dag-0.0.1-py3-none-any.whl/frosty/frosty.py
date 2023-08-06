import numpy as np
import scipy
from inverse_covariance import QuicGraphicalLasso
import sksparse
import robsel

def amd(A):
    '''
    Parameters
    ----------
    A : ndarray
        Symmetric positive definite matrix
    
    Returns
    -------
    L : ndarray
        Sparse Cholesky factor
    perm : ndarray of shape (n_features,)
        Topological ordering
    '''
    p = len(A)
    csc = scipy.sparse.csc_matrix(A)
    factor = sksparse.cholmod.cholesky(csc, ordering_method='amd')
    L = factor.L().toarray()
    perm = np.argsort(factor.P())
    
    return L, perm

def frosty(X, alpha=0.99, b=200, diag=True):
    '''
    FROSTY algorithm for Bayesian network estimation
    
    Parameters
    ----------
    X : ndarray of shape (n_samples, n_features)
        Data matrix
    alpha : float, default=0.99
        (1-alpha) confidence level for robust selection
    b : int, default=200
        Number of bootstrap samples for robust selection
    diag : bool, default=True
        Whether or not to include diagonal when compute RWP function
    
    Returns
    -------
    B : ndarray of shape (n_features, n_features)
        Estimated Bayesian network
    perm : ndarray of shape (n_features,)
        Topological ordering
    '''
    n, p = X.shape
    
    # RobSel
    lam = robsel.RobustSelection(X, alpha, b, diag)
    
    # graphical lasso
    quic = QuicGraphicalLasso(lam=lam).fit(X)
    Theta = quic.precision_
    
    L, perm = amd(Theta)
    L_orig = L[:,perm][perm]
    B = (np.diag(np.diag(L_orig)) - L_orig) @ np.diag(1 / np.diag(L_orig))
    
    return B, perm