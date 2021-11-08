#import libraries
import numpy as np
import datetime as dt
import heapq
import logging

logging.basicConfig(filename='matching.log', level=logging.DEBUG)

#import functions
from matching.utility import combine_dt, mode, group_by_cluster, match_score


# Basic K-Means #

# src: https://github.com/geodra/Articles/blob/master/K-Means_scratch.ipynb
# src: https://www.analyticsvidhya.com/blog/2019/08/comprehensive-guide-k-means-clustering/
# src: Professor Steven Zucker's base code kmeans.py

def kmeans(data, k, MAXITER):
    ''' kmeans() implements the k-means clustering algorithm.

    [clusters, centroids] = kmeans(data, K, MAXITER) partitions the data points
    in data into K distinct clusters. 
    This is a simple implementation of the k-means algorithm with random initialization.

    KMEANS returns an array CLUSTERS containing the cluster
    indices of each data point, as well as CENTROIDS, a vector with the final cluster centroids'.
    '''
    n = len(data)

    #choose initial centroids by picking k points at random from X
    init = [data[i] for i in np.random.randint(n, size=k)]
    
    #centroids is a k-by-p random matrix
    #its i^th row contains the coordinates of the cluster with index i
    centroids = init

    #initialize cluster assignment array
    clusters = np.zeros(n)


    for iter in range(MAXITER):
        
        #create a new clusters vector to fill in with updated assignments
        new_clusters = np.zeros(n)

        #for each data point x_i
        for i in range(n):
            
            #x_i = X[i,:]
            x_i = data[i]
            
            #find closest cluster
            closest = find_closest_cluster(x_i,centroids)

            #reassign x_i to the index of the closest centroid found
            new_clusters[i] = closest

        
        if has_converged(clusters,new_clusters):
            #exit loop
            break 
        
        #otherwise, update assignment
        clusters = new_clusters
        #and recompute centroids
        centroids = recompute_centroids(data,clusters,k)

        if iter == (MAXITER-1):
            logging.info(f'Maximum number of iterations reached!')
    
    return clusters, centroids

def find_closest_cluster(x_i,centroids):
    '''Finds the closest cluster to the centroids'''
    # Compute 'distance' from x_i to each cluster centroid and return 
    # the index of the closest one (an integer).
    return np.argmax([match_score(c,x_i) for c in centroids], axis=0)

def get_cluster_avg(cluster):
    if len(cluster) == 0:
        return None
    clstr = {'netId': None,'date': None, 'destination': None,
   'origin': None,
   'groupId': "",
   'matched': False,
   'preferred_car_type': None,
   'preferred_group_size': None,
   'requestId': None,
   'request_time': None,
   'time': None}
    
    datetimes = []
    destinations = []
    origins = []
    car_types = []
    group_sizes = []
    
    for request in cluster:
        datetimes.append(combine_dt(request['date'], request['time']))
        destinations.append(request['destination'])
        origins.append(request['origin'])
        car_types.append(request['preferred_car_type'])
        group_sizes.append(request['preferred_group_size'])
    
    #get average datetime
    avg_dt = dt.datetime(1,1,1)
    count = 0
    for datetime in datetimes:
        count +=1
        avg_dt += (datetime-avg_dt)/count
        count=1
    clstr['date'] = str(avg_dt.date())
    clstr['time'] = str(avg_dt.time())[0:5]
    
    #get mode of destinations, origins, car types
    clstr['destination'] = str(mode(destinations))
    clstr['origin'] = str(mode(origins))
    clstr['preferred_car_type'] = str(mode(car_types))
    
    #get average group size
    group_sizes = [int(x) for x in group_sizes]
    clstr['preferred_group_size'] = str(round(sum(group_sizes)/len(group_sizes)))
    return clstr

def recompute_centroids(data,clusters,k):
    '''Recomputes the centroids'''
    # Recompute centroids based on current cluster assignment.
    # Return a k-by-p array where each row is a centroid. 
    n = len(data)
    
    #group by cluster
    clstrs = group_by_cluster(data, clusters, k)
    
    centroids = [get_cluster_avg(cluster) for cluster in clstrs]
    centroids = [data[np.random.randint(n)] if centroid is None else centroid for centroid in centroids ]
    return centroids

def has_converged(old_assignment, new_assignment):
    '''Determines if the assignment has not changed since last iteration'''
    return np.array_equal(old_assignment, new_assignment)



## Dynamic K-Means ##

# src: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html#sklearn.metrics.silhouette_score
# src: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_samples.html#sklearn.metrics.silhouette_samples


def dynamic_kmeans(data, start_k, end_k, MAXITER):
    '''Does kmeans for a given number of iterations'''
    logging.info(f"K-Means Clustering")
    logging.info(f"Max iter: {MAXITER}\n")

    ## We want to find the optimal k-value algorithmically. To do so, we will run k-means using a range of k-values. For
    ## each k-value, we will calculate the average silhouette score of the resulting clusters. The first local maxima found 
    ## is used as the optimal k-value.
    
    n=len(data)
    if(n < 2): #can't make groups with less than 2 people!
        return data
    
    #initialize values
    best_score = -100
    best_k = 0
    best_clusters = []
    best_centroids = []
    
    
    logging.info(f"Finding optimal k value in range [{start_k}, {end_k})...")
    for k in range(start_k, end_k):
        logging.info(f"Trying k = {k}...")
        clusters, centroids = kmeans(data, k, MAXITER)
        avg_silh_score = get_avg_silh_score(clusters, centroids, data)
        if avg_silh_score >= best_score:
            best_score = avg_silh_score
            best_k = k
            best_clusters = clusters
            best_centroids = centroids
        else: #break at local maxima (current score is worse than previous)
            break
    logging.info(f"Optimal k: {best_k}\n")
    return best_clusters, best_centroids

def get_avg_silh_score(clusters,centroids,inputs):
    '''Used to evaluate the quality of clusters within kmeans'''
    n = len(inputs)
    coeffs = []
    #compute the mean silhouette coefficeint for each sample
    for i in range(n): #for each sample in inputs
        #find the nearest cluster the sample is NOT in
        x = [match_score(inputs[i], cen) for cen in centroids]
        next_nearest_cluster = heapq.nlargest(2, range(len(x)), key=x.__getitem__)[1]
        
        #store this sample's cluster number
        my_cluster = clusters[i]
        
        #calculate the mean intra-cluster distance (a) and the mean nearest-cluster distance (b)
        intra = []
        nearest = []
        for j in range(n):
            if clusters[j] == my_cluster: #intra-cluster
                intra.append(1-match_score(inputs[i], inputs[j]))
            if clusters[j] == next_nearest_cluster: #nearest-cluster
                nearest.append(1-match_score(inputs[i], inputs[j]))

        if len(intra) > 0:
            a = sum(intra)/len(intra)
        else:
            a = 0
        
        if len(nearest) > 0:
            b = sum(nearest)/len(nearest)
        else:
            b = 0
        
        #calculate the silhouette coefficient
        if a == 0 and b == 0:
            coeffs.append(0)
        else:
            silh_coeff = (b-a)/max(a,b)
            coeffs.append(silh_coeff)
    return sum(coeffs)/len(coeffs) #return avg of silhouette coefficients over all samples

