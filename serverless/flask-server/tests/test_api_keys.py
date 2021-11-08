import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_keys import get_api_key, is_key_valid, is_key_valid_match_algo, valid_keys, get_algo_key

def test_get_api_key():
    # try 100 runs
    for i in range(100):
        key = get_api_key()
        assert key in valid_keys

def test_is_key_valid():
    # try 100 runs
    for i in range(100):
        key = get_api_key()
        assert is_key_valid(key)

def test_is_key_valid_match_algo():    
    # try 100 runs
    for i in range(100):
        key = get_algo_key()
        assert is_key_valid_match_algo(key)

