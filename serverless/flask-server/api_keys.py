import random
import uuid

valid_keys = [
    "a333b39d-6ff7-4e54-9488-b8ec66d7a39d",
    "4d982688-df96-43a5-ba14-bbaafcdee7ff",
    "11ab11ee-0fc5-40e7-ae25-f3167a0c6e90",
    "7c55253f-d199-4eb4-88f2-8df0e3b30fab",
    "7c531163-4688-4c12-b166-48e935d34cf9",
    "d73916de-588c-4966-8dbd-9ae1ed668ee8",
    "d5a62e4d-2c45-49c9-9f96-fbff3d3aa8d0",
    "fa5ea148-3b3a-4bd8-bd2c-10d54df3e7fd",
    "fceabefb-a118-4087-aea5-3d6048ab9e04",
    "100fe632-8e36-47da-a3a3-143b086ce1e4",
    "f320ef63-c568-41d2-83dc-452cc9d6c526",
    "241876f9-f65c-4a43-9838-e2cde6bfe884",
    "849492b7-8cec-44e9-a737-0699e0f19deb",
    "24d7fb5a-a87c-4ddc-a8ef-de3dae77d8d8",
    "54934943-bf17-4beb-a767-478973272d89",
    "8d3f8557-95f3-4e7d-a975-d60c42a0a232",
    "d3de02ea-61b2-48bb-8a82-d413faa00d59",
    "ef684cf8-84a2-4b63-bf18-fdd9b89b420f",
    "d8064925-17c8-4cc9-8445-d2f2c333f048",
    "002fcbf3-6cae-49a9-bf66-50c148d5df3e",
]

algo_keys = [
    '8d6dadde-3d6f-450d-bb5d-df8fa6005982',
    '61fb0b33-bfbd-4761-9129-c8782c2aa375',
    'a26c10e4-e83a-49af-a5f1-feb071d07d0c',
    '2895d831-77f0-4bc0-9eda-0b7c507cf86a',
    'bbafd0bb-a4dc-4114-9568-5affb58d2b2a']


# # code to generate new api keys
# keys = []
# for i in range(5):
#     keys.append(str(uuid.uuid4()))
# print(keys)


def get_api_key():
    return random.choice(valid_keys)

def get_algo_key():
    return random.choice(algo_keys)

def is_key_valid(key):
    return key in valid_keys

# algo_keys are different set of keys to invoke matching algorithm 
def is_key_valid_match_algo(key):
    return key in algo_keys
