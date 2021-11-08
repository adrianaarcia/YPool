#import libraries
import datetime as dt
import logging

logging.basicConfig(filename='matching.log', level=logging.DEBUG)

#import functions
from matching.kmeans import dynamic_kmeans
from matching.greedy import dynamic_greedy_matching
from matching.utility import sort_by_clusters


def find_matches(data):
    '''Takes in requests and finds matches for them if they exist returns a list of dict of the requests'''
    start = dt.datetime.now()
    
    matched = [dat for dat in data if dat['matched']]
    inputs = [dat for dat in data if not dat['matched']]
    n = len(inputs)


    ## Step 1: Run K-Means Clustering Algorithm ##

    #determine the appropriate range of k-values to test, based on the assumption that samples will be evenly distributed amongst clusters
    max_cluster_sz = 50 #maximum desireable size of a cluster
    min_cluster_sz = 10 #minimum desirable size of a cluster
    start_k = max(2, int(n/max_cluster_sz))
    end_k = max(3, int(n/min_cluster_sz))

    #maximum number of iterations for each run of k-means
    max_iter = 300
    
    
    #get result of k-means with optimal k-value
    if n > 500:
        start_k = min(int(n/70), 21)
        end_k = start_k+4
        clusters, centroids = dynamic_kmeans(inputs, start_k, end_k, 20)
        cluster_array = sort_by_clusters(inputs, clusters, len(centroids), True) #organize data into clusters given by k-means


    elif n > 40:
        clusters, centroids = dynamic_kmeans(inputs, start_k, end_k, max_iter)
        cluster_array = sort_by_clusters(inputs, clusters, len(centroids), True) #organize data into clusters given by k-means

    else:
        sorted_clusters = sort_by_clusters(inputs, None, None, False)
        cluster_array = [sorted_clusters]
        
    ## Step 2: Use greedy algorithm to finalize matches, balancing match rate and quality of matches ##
        
    results = dynamic_greedy_matching(cluster_array)
    
    
    #timing
    end = dt.datetime.now()
    logging.info(f"Elapsed time:{end-start}\n")
    
    results.extend(matched)
    return results





