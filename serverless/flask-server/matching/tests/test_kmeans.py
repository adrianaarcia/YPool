import random
import datetime as dt
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kmeans import kmeans, find_closest_cluster, get_cluster_avg, recompute_centroids, has_converged, dynamic_kmeans, get_avg_silh_score
from sample_inputs import gen_sample_input, gen_request, gen_random_datetime
from test_sample_inputs import req_format, locs

## FIXTURES ##

## Randomly generated sample datasets of size n.

## Datasets are defined by two factors: size and sparsity.
##
## Size
## ---------------------------
## small -- 2 < n < 40
## med -- 40 < n < 200
## large -- 200 < n < 2000
##
## Sparsity
## ---------------------------
## semester -- departure times of requests are within 16 weeks of each other
semester = dt.timedelta(weeks=16)
## month -- departure times of requests are within a month of each other
month = dt.timedelta(weeks=4)
## fort -- departure times of requests are within two weeks of each other
fort = dt.timedelta(weeks=2)
## week -- departure times of requests are within a week of each other
week = dt.timedelta(weeks=1)

s = dt.date(2021, 1, 1)
e = dt.date(2021, 12, 31)

@pytest.fixture
def semester_small():
    return gen_sample_input(random.randint(2, 40), s, e, semester,matched=0)

@pytest.fixture
def semester_med():
    return gen_sample_input(random.randint(41, 200), s, e, semester,matched=0)

@pytest.fixture
def semester_large():
    return gen_sample_input(random.randint(200, 2000), s, e, semester, matched=0)
    

@pytest.fixture
def month_small():
    return gen_sample_input(random.randint(2, 40), s, e, month, matched=0)

@pytest.fixture
def month_med():
    return gen_sample_input(random.randint(41, 200), s, e, month, matched=0)

@pytest.fixture
def month_large():
    return gen_sample_input(random.randint(201, 2000), s, e, month, matched=0)


@pytest.fixture
def fort_small():
    return gen_sample_input(random.randint(2, 40), s, e, fort, matched=0)

@pytest.fixture
def fort_med():
    return gen_sample_input(random.randint(41, 200), s, e, fort, matched=0)

@pytest.fixture
def fort_large():
    return gen_sample_input(random.randint(201, 2000), s, e, fort, matched=0)


@pytest.fixture
def week_small():
    return gen_sample_input(random.randint(2, 40), s, e, week, matched=0)

@pytest.fixture
def week_med():
    return gen_sample_input(random.randint(41, 200), s, e, week, matched=0)

@pytest.fixture
def week_large():
    return gen_sample_input(random.randint(201, 2000), s, e, week, matched=0)

@pytest.fixture
def samples(semester_small, semester_med, semester_large, month_small, month_med, month_large, fort_small, fort_med, fort_large, week_small, week_med, week_large):
    return [semester_small, semester_med, semester_large, month_small, month_med, month_large, fort_small, fort_med, fort_large, week_small, week_med, week_large]



## Basic K-Means ##
#@pytest.mark.skip
def test_kmeans(samples):
    for sample in samples:
        for k in [2,3,4]:
            clusters, centroids = kmeans(sample, k, 100)
            assert len(clusters) == len(sample)
            assert len(centroids) == k
            assert all(x in range(k) for x in clusters)

@pytest.fixture
def centroids():
    k = 3
    cent = gen_sample_input(k, s, e, fort)
    return cent

@pytest.fixture
def requests():
    d1 = gen_random_datetime()
    d2 = gen_random_datetime()
    d3 = gen_random_datetime()
    d4 = gen_random_datetime()

    r1 = gen_request(0, min(d1, d2), max(d1,d2))
    r2 = gen_request(1, min(d3, d4), max(d3, d4))

    return [r1, r2]

def test_find_closest_cluster(centroids, requests):
    r1 = requests[0]
    r2 = requests[1]

    k = len(centroids)

    c1 = find_closest_cluster(r1, centroids) 
    c2 =  find_closest_cluster(r2, centroids)

    assert all(x in range(k) for x in [c1,c2])

def check_format(req, req_format):  
    #check type
    assert type(req) is dict

    #check keys
    assert req.keys() == req_format.keys()
    
    #check entries
    assert dt.datetime.strptime(req['date'], '%Y-%m-%d') #date
    assert dt.datetime.strptime(req['time'], '%H:%M') #time
    assert req['origin'] in locs and req['destination'] in locs #origin and destination
    assert req['groupId'] == '' and not req['matched'] #default values
    assert req['preferred_car_type'] in ['Regular', 'XL'] #car type
    assert req['preferred_group_size'] in ['2','3','4','5'] #group size


def test_get_cluster_avg(centroids, req_format):
    req = get_cluster_avg(centroids)
    check_format(req, req_format)
    
def test_recompute_centroids(samples, req_format):
    for sample in samples:
        n = len(sample)
        k = 3
        res = recompute_centroids(sample, [random.randrange(k) for _ in range(n)], k)

        assert len(res) == k
        for req in res:
            check_format(req, req_format)

def test_has_converged():
    k = 3
    l = 20
    clusters1 = [random.randrange(k) for _ in range(l)] 
    clusters2 = [random.randrange(k) for _ in range(l)]

    assert has_converged(clusters1, clusters1)
    assert not has_converged(clusters1, clusters2)



## Dynamic K-Means ##

@pytest.fixture
def clustered_samples(samples):
    max_iter = 50
    results = []
    for sample in samples:
        n = len(sample)
        k = max(3, int(n/10))
        clusters, centroids = kmeans(sample, k, max_iter)

        results.append([clusters, centroids, sample])
    
    return results
    
@pytest.mark.skip
def test_get_avg_silh_score(clustered_samples):
    clusters, centroids, sample = clustered_samples[random.choice([0,3,6,9])]
    score = get_avg_silh_score(clusters, centroids, sample)
    
    assert isinstance(score, float) 

#@pytest.mark.skip
def test_dynamic_kmeans(samples):
    start_k = 2
    stop_k = 20
    max_iter = 50

    sample = samples[random.choice([0,3,6,9])]
    
    clusters, centroids = dynamic_kmeans(sample, start_k, stop_k, max_iter)
    k = len(centroids)
    assert len(clusters) == len(sample)
    assert start_k <= k and k <= stop_k
