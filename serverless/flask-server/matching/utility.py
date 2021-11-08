#import libraries
import datetime as dt
from collections import defaultdict


## Grouping and sorting ##
def group_by_cluster(data, clusters, no_clusters):
    ''' returns a nested list of data, sorted by cluster '''
    ret = [[] for i in range(no_clusters)]
    for i in range(len(clusters)):
        index = int(clusters[i])
        d = data[i]
        ret[index].append(d)
    return ret

def sort_by_group(requests):
    ''' given a list of requests, returns a list of lists, where the sublists contain netids of each group '''
    groups =  defaultdict(list)
    
    for req in requests:
        if req['matched']:
            groups[req['groupId']].append(req)
    
    return list(groups.values())

def sort_by_clusters(inputs, clusters, l_centroids, yes):
    if yes:
        cluster_arr = group_by_cluster(inputs, clusters, l_centroids) #organize data into clusters given by k-means
        sorted_clusters = [sorted(cluster, key = lambda i: i['request_time']) for cluster in cluster_arr]
    else:
        sorted_clusters = sorted(inputs, key=lambda i: i['request_time'])

    return sorted_clusters


## Evaluation ##
def match_score(req1, req2):
    '''Utility tool to evaluate the feasibility of two requests given our evaluation heuristics'''
    # Datetime
    d1 = combine_dt(req1['date'], req1['time'])
    d2 = combine_dt(req2['date'], req2['time'])

    d_hours = abs(d1-d2).total_seconds() / 3600.0
    if d_hours > 168:
        dt_score = 0
    else:
        dt_score = 0.000031001984127*(d_hours ** 2) - 0.0111607142857*d_hours + 1


    # Groupsize
    g = abs(int(req1['preferred_group_size']) - int(req2['preferred_group_size']))
    group_sz_score = ((-1 / 3) * g) + 1


    # Car size
    if req1['preferred_car_type'] == req2['preferred_car_type']:
        car_sz_score = 1
    else:
        car_sz_score = 0

    # Origin
    if req1['origin'] == req2['origin']:
        origin_score = 1
    else:
        origin_score = 0

    # Destination
    kg = ['Airport-JFK', 'Airport-LGA']
    if req1['destination'] == req2['destination']:
        dest_score = 1
    elif (req1['destination'] in kg) and (req2['destination']in kg):
        dest_score = 0.9
    elif (req1['destination'] in kg and req2['destination'] == 'Airport-EWR') or (req2['destination']in kg and req1['destination'] == 'Airport-EWR'):
        dest_score = 0.6
    elif (req1['destination'] in kg and req2['destination'] == 'Airport-BDL') or (req2['destination']in kg and req1['destination'] == 'Airport-BDL'):
        dest_score = 0.2
    else:
        dest_score = 0

    return 0.5*dt_score + 0.05*group_sz_score + 0.05*car_sz_score + 0.20*origin_score + 0.20*dest_score

def group_score(cluster):
    '''For each group made, finds average value of the feasiblity of the matched group using each member as the head'''
    if len(cluster) <  2:
        return 0
    # Calculate match_score for each member as head
    dat = {}
    for req in cluster:
        count = 0
        for r in cluster:
            if r != req:
                v = match_score(req, r)
                count += v
        # Last element has the preferred group size
        dat[req['netId']] = count/(len(cluster)-1)

    avg = 0
    cnt = 0
    for item in dat.values():
        avg += item
        cnt += 1

    return avg/cnt


## Analytics, Summary, and Visualization Output ##
def get_stats(requests):
    '''Returns a dictionary of relevant stats'''
    groups = sort_by_group(requests)
    no_matched = 0
    avg_g_score = 0
    
    for group in groups:
        no_matched += len(group)
        avg_g_score += group_score(group)

    no_groups = len(groups)
    if no_groups > 0:
        return {'No. matched': no_matched, 'No. groups': no_groups, 'Avg. group score':str(round(100*avg_g_score/no_groups,2))+'%', 'Avg. group size': no_matched/no_groups, 'Match rate': (no_matched/len(requests))*100}
    else:
        return {'No. matched': no_matched, 'No. groups': no_groups, 'Avg. group score':'0%', 'Avg. group size': 0, 'Match rate': 0}

def print_stats(stats):
    '''Prints relevant stats'''
    for item in stats:
        print(f"\n{item}: {stats[item]}",end='')
    print("%")

def print_groups(requests):
    '''Prints groups formed from our matching'''
    groups = sort_by_group(requests)

    for i in groups:
        print(f"Group ID: {i[0]['groupId']}")
        print(f"Group score: {round(group_score(i)*100,2)}%")
        for request in i:
            print(f"net ID: {request['netId']}, date/time: {request['date']} {request['time']}, origin: {request['origin']}, destination: {request['destination']}, pref. group size: {request['preferred_group_size']}, pref. car type: {request['preferred_car_type']}")
        print("\n")

def print_results(results):
    print("Summary:")
    print("--------------------------------", end='')
    stats = get_stats(results)
    print_stats(stats)

    print("\nGroups")
    print("--------------------------------")
    print_groups(results)
    
    print("--------------------------------")


## Misc utility ##
def combine_dt(date_str, time_str):
    '''Utility tool to create datetime object from separate date and time'''
    date = dt.datetime.strptime(date_str, '%Y-%m-%d').date()
    time = dt.datetime.strptime(time_str, '%H:%M').time()
    datetime = dt.datetime.combine(date, time)
    return datetime

def mode(lst):
    '''Returns modal score from a list'''
    return max(set(lst), key = lst.count)