import copy
import uuid
import logging
logging.basicConfig(filename='matching.log', level=logging.DEBUG)

from matching.utility import match_score, get_stats


def dynamic_greedy_matching(cluster_array):
    '''Returns list of all requests, some of which may have been matched according to our heuristics'''
    logging.info(f"Greedy Matching\n")
    ## Run the greedy algorithm on the clustered data, decreasing the baseline threshold for match quality
    ## if the match rate is too low.

    #define bounds for results
    threshold = 0.935 #threshold value for similarity used in greedy, start at 0.935
    thresh_limit = 0.9 #threshold lower limit
    match_rate_target = 15 #our target it at least 15% of requests matched
    step = 0.005
    logging.info(f"\nThreshold upper bound: {threshold}\nThreshold lower bound: {thresh_limit}\nStep: {step}\nTarget match rate: {match_rate_target}%\n")

    while threshold >= thresh_limit:
        matches = []
        for cluster in cluster_array:
            clstr = greedy_matching(cluster, threshold)
            matches.extend(clstr)

        info = get_stats(matches) #fetch analytics for this solution
        match_rate = info['Match rate']

        logging.info(f"Threshold: {threshold}, Match rate: {match_rate}")
        if float(match_rate) >= match_rate_target:
            break
        threshold -= step

    return sorted(matches, key = lambda i: i['request_time']) #sort by request time

   
def greedy_matching(cluster, threshold):
    '''For a given cluster and threshold value continuously fetches the next best grouping and matches them'''
    c = copy.deepcopy(cluster)
    out = []
    end = 1
    while end > threshold:
        # Get best available group
        end, lst = greedy_util(c)
        if(end > threshold):
            # If group score is higher than our threshold, match the members of the group
            group_id = str(uuid.uuid4())

            # Delete members that have been matched so we don't consider them again
            rm = []

            for i in range(len(c)):
                if c[i]['requestId'] in lst:
                    c[i]['groupId'] = group_id
                    c[i]['matched'] = True
                    out.append(c[i])
                    # Mark for deletion
                    rm.append(c[i])

            # Remove from c
            for i in range(len(rm)):
                c.remove(rm[i])

    # Add members that were not matched and return the entire list of requests
    out.extend(c)
    return out          


def greedy_util(cluster):
    '''Function that returns the highest scored possible group within the cluster in question'''
    # If only 1 person, return 0; can't match with anyone
    if len(cluster) <  2:
        return 0, []

    # Create list of best possible match for each request and place the list in dat
    dat = {}
    for req in cluster:
        num = int(req['preferred_group_size'])
        lst = [["requestId", -1] for i in range(num)]
        for r in cluster:
            if r != req:
                v = match_score(req, r)
                pos = -1
                for i in range(num):
                    if v > lst[i][1]:
                        pos = i
                        break

                #pos is the index you break at use this to splice the list
                if pos > -1:
                    lst.insert(pos, [r['requestId'], v])
                    lst.pop()

        # Last element has the preferred group size
        dat[req['requestId']] = [lst, req['preferred_group_size']]

    # From proposed matches in dat find group with highest score.
    dat2 = {}

    for pair in dat.items():
        ls = pair[1][0]
        val = 0
        # If a member of the list couldn't be paired, continue (disregard the last item)
        for i in range(len(ls)-1):
            if ls[i][1] == -1:
                continue
            else:
                val += ls[i][1]
        # Divide the value obtained by the original preferred group size - 1. This will punish groupings that weren't able to find the right no of members
        dat2[pair[0]] = val/(int(pair[1][-1]) - 1)

    # Find max value in dat2
    all_values = dat2.values()
    max_value = max(all_values)

    max_key = max(dat2, key=dat2.get)
    t_lst = dat[max_key]
    # Remove the preferred value
    t_lst.pop()
    flat_list = [item for sublist in t_lst for item in sublist]

    # Retrieve a flattened list of netid's reprenting members our head can be matched with
    ret_lst = [flat_list[i][0] for i in range(len(flat_list))]
    # Remove last person
    ret_lst.pop()
    # Append the max key
    ret_lst.append(max_key)

    if 'requestId' in ret_lst:
        return 0, []

    return max_value, ret_lst
