import json
import requests
import inspect
from time import sleep
from .__config__ import *


def get_address_info(addr: [str, list]) -> list:
    """
    https://api.koios.rest/#post-/address_info
    Get address info - balance, associated stake address (if any) and UTxO set for given addresses
    :param addr: Payment address(es) as string (for one address) or list (for multiple addresses)
    :returns: The list of address information maps
    """
    url = API_BASE_URL + '/address_info'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    addresses = {}
    if isinstance(addr, list):
        addresses['_addresses'] = addr
    else:
        addresses['_addresses'] = [addr]
    while True:
        try:
            response = requests.post(url, headers=headers, data=json.dumps(addresses))
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


def get_address_txs(addr: [str, list], block_height: int = 0) -> list:
    """
    https://api.koios.rest/#post-/address_txs
    Get the transaction hash list of input address array, optionally filtering after specified block height (inclusive)
    :param addr: Payment address(es) as string (for one address) or list (for multiple addresses)
    :param block_height: Return only the transactions after this block height. Optional.
    :returns: The list of transactions maps
    """
    url = API_BASE_URL + '/address_txs'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    parameters = {}
    addresses = {}
    if isinstance(addr, list):
        addresses['_addresses'] = addr
    else:
        addresses['_addresses'] = [addr]
    if block_height > 0:
        addresses['_after_block_height'] = block_height
    txs = []
    offset = 0
    while True:
        if offset > 0:
            parameters['offset'] = offset
        while True:
            try:
                response = requests.post(url, headers=headers, params=parameters, data=json.dumps(addresses))
                if response.status_code == 200:
                    resp = json.loads(response.text)
                    break
                else:
                    print(f"status code: {response.status_code}, retrying...")
            except Exception as e:
                print(f"Exception in {inspect.getframeinfo(inspect.currentframe()).function}: {e}")
                sleep(SLEEP_TIME)
                print(f"offset: {offset}, retrying...")
        txs += resp
        if len(resp) < API_RESP_COUNT:
            break
        else:
            offset += len(resp)
    return txs


def get_credential_utxos(cred: [str, list]) -> list:
    """
    https://api.koios.rest/#post-/credential_utxos
    Get a list of UTxO against input payment credential array including their balances
    :param cred: Payment credential in hex format as string (for one credential) or list (for multiple credentials)
    :returns: The list of input payment credentials maps
    """
    url = API_BASE_URL + '/credential_utxos'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    credentials = {}
    if isinstance(cred, list):
        credentials['_payment_credentials'] = cred
    else:
        credentials['_payment_credentials'] = [cred]
    while True:
        try:
            response = requests.post(url, headers=headers, data=json.dumps(credentials))
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


def get_address_assets(addr: [str, list]) -> list:
    """
    https://api.koios.rest/#post-/address_assets
    Get the list of all the assets (policy, name and quantity) for given addresses
    :param addr: Payment address(es) as string (for one address) or list (for multiple addresses)
    :returns: The list of assets maps by address
    """
    url = API_BASE_URL + '/address_assets'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    parameters = {}
    addresses = {}
    if isinstance(addr, list):
        addresses['_addresses'] = addr
    else:
        addresses['_addresses'] = [addr]
    assets = []
    offset = 0
    while True:
        if offset > 0:
            parameters['offset'] = offset
        while True:
            try:
                response = requests.post(url, headers=headers, params=parameters, data=json.dumps(addresses))
                if response.status_code == 200:
                    resp = json.loads(response.text)
                    break
                else:
                    print(f"status code: {response.status_code}, retrying...")
            except Exception as e:
                print(f"Exception in {inspect.getframeinfo(inspect.currentframe()).function}: {e}")
                sleep(SLEEP_TIME)
                print(f"offset: {offset}, retrying...")
        assets += resp
        if len(resp) < API_RESP_COUNT:
            break
        else:
            offset += len(resp)
    return assets


def get_credential_txs(cred: [str, list], after_block: int = 0) -> list:
    """
    https://api.koios.rest/#post-/credential_txs
    Get the transaction hash list of input payment credential array,
    optionally filtering after specified block height (inclusive)
    :param cred: Credential(s) as string (for one credential) or list (for multiple credentials)
    :param after_block: Only fetch information after specific block height
    :returns: The list of address information maps
    """
    url = API_BASE_URL + '/credential_txs'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    parameters = {}
    if isinstance(cred, list):
        parameters['_payment_credentials'] = cred
    else:
        parameters['_payment_credentials'] = [cred]
    if after_block:
        parameters['_after_block_height'] = after_block
    while True:
        try:
            response = requests.post(url, headers=headers, data=json.dumps(parameters))
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
