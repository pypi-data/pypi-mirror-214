import json
import requests
import inspect
from time import sleep
from .__config__ import *


def get_blocks(limit: int = 0) -> list:
    """
    https://api.koios.rest/#get-/blocks
    Get summarised details about all blocks (paginated - latest first)
    :param limit: the limit of the returned blocks number
    :returns: The list of block maps (the newest first)
    """
    url = API_BASE_URL + '/blocks'
    parameters = {}
    blocks = []
    offset = 0
    while True:
        if offset > 0:
            parameters['offset'] = offset
        if isinstance(limit, int) and limit > 0:
            parameters['limit'] = limit
        while True:
            try:
                response = requests.get(url, params=parameters)
                if response.status_code == 200:
                    resp = json.loads(response.text)
                    break
                else:
                    print(f"status code: {response.status_code}, retrying...")
            except Exception as e:
                print(f"Exception in {inspect.getframeinfo(inspect.currentframe()).function}: {e}")
                sleep(SLEEP_TIME)
                print(f"offset: {offset}, retrying...")
        blocks += resp
        if len(resp) < API_RESP_COUNT:
            break
        else:
            offset += len(resp)
        if isinstance(limit, int) and len(blocks) > limit:
            break
    if isinstance(limit, int) and limit > 0:
        return blocks[0:limit]
    else:
        return blocks


def get_block_info(block: [str, list]) -> list:
    """
    https://api.koios.rest/#post-/block_info
    Get detailed information about a specific block
    :param block: Block hash as string (for one block) or list of block hashes (for multiple blocks)
    :returns: The list of block maps
    """
    url = API_BASE_URL + '/block_info'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    block_hashes = {}
    if isinstance(block, list):
        block_hashes['_block_hashes'] = block
    else:
        block_hashes['_block_hashes'] = [block]
    while True:
        try:
            response = requests.post(url, headers=headers, data=json.dumps(block_hashes))
            if response.status_code == 200:
                resp = json.loads(response.text)
                break
            else:
                print(f"status code: {response.status_code}, retrying...")
        except Exception as e:
            print(f"Exception in {inspect.getframeinfo(inspect.currentframe()).function}: {e}")
            sleep(SLEEP_TIME)
            print('retrying...')
    return resp


def get_block_txs(block: [str, list]) -> list:
    """
    https://api.koios.rest/#post-/block_txs
    Get a list of all transactions included in provided blocks
    :param block: Block hash as string (for one block) or list of block hashes (for multiple blocks)
    :returns: The list of transaction maps by block
    """
    url = API_BASE_URL + '/block_txs'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    block_hashes = {}
    if isinstance(block, list):
        block_hashes['_block_hashes'] = block
    else:
        block_hashes['_block_hashes'] = [block]
    while True:
        try:
            response = requests.post(url, headers=headers, data=json.dumps(block_hashes))
            if response.status_code == 200:
                resp = json.loads(response.text)
                break
            else:
                print(f"status code: {response.status_code}, retrying...")
        except Exception as e:
            print(f"Exception in {inspect.getframeinfo(inspect.currentframe()).function}: {e}")
            sleep(SLEEP_TIME)
            print('retrying...')
    return resp
