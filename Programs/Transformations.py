import numpy as np
from pycpd import *
from sklearn.neighbors import NearestNeighbors

def ICP_Registration(CT_fiducials, US_fiducials, CT_Target, US_Target):
    US_Target_Modified = []

    # Turn fiducial arrays into NP arrays
    US_fiducials = np.array(US_fiducials)
    CT_fiducials = np.array(CT_fiducials)
    
    T, distances, iterations = icp(US_fiducials , CT_fiducials)
    num_rows, num_cols = US_fiducials.shape

    # Make US_fiducials_modified a homogeneous representation of CT_fiducials
    US_fiducials_modified = np.ones((num_rows, 4))
    US_fiducials_modified[:,0:3] = US_fiducials

    # Transform US_fiducials_modified
    US_fiducials_modified = np.dot(T, US_fiducials_modified.T).T
    US_fiducials_modified = US_fiducials_modified.tolist()

    # Make US_Target_modified a homogeneous representation of CT_Target
    US_Target_Modified.append(US_Target[0])
    US_Target_Modified.append(US_Target[1])
    US_Target_Modified.append(US_Target[2])
    US_Target_Modified.append(1)

    # Transform Target
    US_Target_Modified = np.dot(T,US_Target_Modified)
    US_Target_Modified = US_Target_Modified.tolist()
    US_Target_Modified.pop()
    
    # remove 1's from US_fiducials_modified
    for x in range(len(US_fiducials_modified)):
        US_fiducials_modified[x].pop()

    # (target fiducial set - CT_fiducials, modified fiducial set - US_fiducials_modified, Original target - CT_Target, Modified Target - US_Target)
    ICP_data = [CT_fiducials, US_fiducials_modified, CT_Target, US_Target_Modified]
    return ICP_data

def CPD_Registration(CT_fiducials, US_fiducials, CT_Target, US_Target):
    
    # Append source target to point cloud
    US_fiducials.append(US_Target)

    # convert to arrays a perform registration using CPD library
    Y = np.array(CT_fiducials)
    X = np.array(US_fiducials)
    reg = DeformableRegistration(**{'X': X, 'Y': Y})
    TY, _ = reg.register()
    TY_List = TY.tolist()
    US_Target_Modified = TY_List[-1]
    del TY_List[-1]
    US_fiducials_modified = TY_List
    CT_fiducials.pop()

    # (target fiducial set - CT_fiducials, modified fiducial set - US_fiducials_modified, Original target - CT_Target, Modified Target - US_Target)
    CPD_data = [CT_fiducials, US_fiducials_modified, CT_Target, US_Target_Modified]
    return CPD_data

def best_fit_transform(A, B):
    '''
    Calculates the least-squares best-fit transform that maps corresponding points A to B in m spatial dimensions
    Input:
    A: Nxm numpy array of corresponding points
    B: Nxm numpy array of corresponding points
    Returns:
    T: (m+1)x(m+1) homogeneous transformation matrix that maps A on to B
    R: mxm rotation matrix
    t: mx1 translation vector
    '''

    assert A.shape == B.shape

    # get number of dimensions
    m = A.shape[1]

    # translate points to their centroids
    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)
    AA = A - centroid_A
    BB = B - centroid_B

    # rotation matrix
    H = np.dot(AA.T, BB)
    U, S, Vt = np.linalg.svd(H)
    R = np.dot(Vt.T, U.T)

    # special reflection case
    if np.linalg.det(R) < 0:
        Vt[m-1,:] *= -1
        R = np.dot(Vt.T, U.T)

    # translation
    t = centroid_B.T - np.dot(R,centroid_A.T)

    # homogeneous transformation
    T = np.identity(m+1)
    T[:m, :m] = R
    T[:m, m] = t

    return T, R, t

def nearest_neighbor(src, dst):
    '''
    Find the nearest (Euclidean) neighbor in dst for each point in src
    Input:
        src: Nxm array of points
        dst: Nxm array of points
    Output:
        distances: Euclidean distances of the nearest neighbor
        indices: dst indices of the nearest neighbor
    '''

    assert src.shape == dst.shape

    neigh = NearestNeighbors(n_neighbors=1)
    neigh.fit(dst)
    distances, indices = neigh.kneighbors(src, return_distance=True)
    return distances.ravel(), indices.ravel()

def icp(A, B, init_pose=None, max_iterations=20, tolerance=0.001):
    '''
    The Iterative Closest Point method: finds best-fit transform that maps points A on to points B
    Input:
        A: Nxm numpy array of source mD points
        B: Nxm numpy array of destination mD point
        init_pose: (m+1)x(m+1) homogeneous transformation
        max_iterations: exit algorithm after max_iterations
        tolerance: convergence criteria
    Output:
        T: final homogeneous transformation that maps A on to B
        distances: Euclidean distances (errors) of the nearest neighbor
        i: number of iterations to converge
    '''

    assert A.shape == B.shape

    # get number of dimensions
    m = A.shape[1]

    # make points homogeneous, copy them to maintain the originals
    src = np.ones((m+1,A.shape[0]))
    dst = np.ones((m+1,B.shape[0]))
    src[:m,:] = np.copy(A.T)
    dst[:m,:] = np.copy(B.T)

    # apply the initial pose estimation
    if init_pose is not None:
        src = np.dot(init_pose, src)

    prev_error = 0

    for i in range(max_iterations):
        # find the nearest neighbors between the current source and destination points
        distances, indices = nearest_neighbor(src[:m,:].T, dst[:m,:].T)

        # compute the transformation between the current source and nearest destination points
        T,_,_ = best_fit_transform(src[:m,:].T, dst[:m,indices].T)

        # update the current source
        src = np.dot(T, src)

        # check error
        mean_error = np.mean(distances)
        if np.abs(prev_error - mean_error) < tolerance:
            break
        prev_error = mean_error

    # calculate final transformation
    T,_,_ = best_fit_transform(A, src[:m,:].T)

    return T, distances, i
