
import random
import uuid



def random_matching(data):
    inp = data.copy()

    grp = str(uuid.uuid4())

    for entry in inp:
        entry['matched'] = True
        entry['groupId'] = grp

    return inp

# def random_matching(data):
#     inp = data.copy()
#     out = []
#     group_num = 1
#     while len(inp) != 0:
#         count = len(inp)
#         group_sz = random.randint(2,5)
#         print(f"GroupSize = {group_sz}")
#         if count < group_sz: #and remaining entries to output, unchanged and stop
#             print(f"Entries left: {len(inp)}")
#             out.extend(inp)
#             inp = []
#         else: #choose a random group of size group_sz
#             group_id = group_num
#             group_num+=1
#             for i in range(group_sz): #for each spot in the group
#                 index = random.randint(0, len(inp)-1)#select a random member of inp
    
#                 #add to group
#                 inp[index]['matched'] = True
#                 inp[index]['groupId'] = group_id
                
#                 out.append(inp[index]) #add to output
#                 inp.pop(index) #remove from inp
            
#     return out

# Call random_matching
#output = random_matching(dat)



# print("-----------------------------------------")
# print("Unmatched requests")
# for item in output:
#     if not item['matched']:
#         print(item)
# print("-----------------------------------------")
# print("\n\n-----------------------------------------")
# print("Matched requests")
# for item in output:
#     if item['matched']:
#         print(item)
# print("-----------------------------------------")





