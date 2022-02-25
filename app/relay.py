import time
import requests
from web3 import Web3
from web3.middleware import geth_poa_middleware
from config import *

w3 = Web3(Web3.WebsocketProvider(RPC_URL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def transact(f):
    nonce = w3.eth.getTransactionCount(RELAYER_ADDRESS, 'pending')
    tx = f.buildTransaction({
        'chainId': CHAINID,
        # 'gas': GAS,
        # 'gasPrice': GAS_PRICE,
        'nonce': nonce,
    })
    signed_txn = w3.eth.account.sign_transaction(tx, private_key=RELAYER_PRIVATE)
    w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    receipt = w3.eth.waitForTransactionReceipt(signed_txn['hash'])
    assert receipt['status'], '{} failed'.format(tx)

def mint(addr, uuid, logger):
    logger.info('minting {}'.format(uuid))

    addr = Web3.toChecksumAddress(addr)

    # Query user's nft balance.
    balance = contract.functions.balanceOf(addr).call()

    # balance = 0 # DEBUG

    # Check to see if the user is already verified.
    if balance > 0:
        logger.info('{} has minted'.format(addr))
        return

    logger.info('{} has NOT minted'.format(addr))

    # Get the contract data that will be used as
    # input for the verification transaction.
    data = requests.get(VERIFICATIONS_URL + '/' + CONTEXT + '/' + uuid + '?signed=eth&timestamp=seconds').json()
    # logger.info('Query verification signing data')
    # logger.info(data)

    data = data['data']

    # Convert all contextIds to byte32
    data['contextIds'] = list(map(Web3.utils.asciiToHex, data['contextIds']))

    # Run the verification transaction.
    logger.info('minting {}'.format(uuid))
    transact(contract.functions.mint(
        data['contextIds'],
        data['timestamp'],
        data['sig']['v'],
        '0x' + data['sig']['r'],
        '0x' + data['sig']['s']
    ))

    logger.info('{} minted'.format(uuid))

def bind(addr, uuidHash, nonce, signature, logger):
    logger.info('binding {}'.format(addr))
    logger.info('binding {}'.format(uuidHash))
    logger.info('binding {}'.format(nonce))
    logger.info('binding {}'.format(signature))

    addr = Web3.toChecksumAddress(addr)

    # Query user's nft balance.
    balance = contract.functions.balanceOf(addr).call()

    # balance = 0 # DEBUG

    # Check to see if the user is already verified.
    if balance > 0:
        logger.info('{} has minted'.format(addr))
        return

    # Run the sponsorship transaction.
    logger.info('binding {}'.format(addr))
    transact(contract.functions.bind(addr, uuidHash, nonce, signature))

    logger.info('{} bound'.format(addr))

def check_brightid_link(contextId, logger):
    logger.info('checking brightid link {}'.format(contextId))

    # waiting for link
    for i in range(LINK_CHECK_NUM):
        # Query BrightID verification data
        data = requests.get(VERIFICATIONS_URL + '/' + CONTEXT + '/' + contextId).json()
        # logger.info('Query verification data')
        # logger.info(data)

        # Check to see if the user has a linked BrightID
        if 'errorNum' not in data or data['errorNum'] != NOT_FOUND:
            logger.info('{} is linked'.format(contextId))

            # Verify the contextId is the one currently linked to the BrightID account
            contextIds = data.get('data', {}).get('contextIds', [])
            if contextIds and contextIds[0].lower() != contextId.lower():
                logger.info('uuid is not current BrightID link')
                logger.info(contextIds)
                logger.info(contextId)
                raise Exception('This uuid is not the most recent one you\'ve linked to BrightID. Please relink {} via BrightID!'.format(contextIds[0]))

            return

        logger.info('{} is NOT linked'.format(contextId))
        time.sleep(LINK_CHECK_PERIOD)
    else:
        logger.info('{} monitoring expired'.format(contextId))
        raise Exception('Could not determine that uuid is linked to BrightID')

def check_valid_sponsor(contextId, logger):
    # Query BrightID verification data
    # This can be used to check for a valid sponsorship and
    # will be used to complete the verification in the next step.
    data = requests.get(VERIFICATIONS_URL + '/' + CONTEXT + '/' + contextId).json()
    # logger.info('Query verification data')
    # logger.info(data)

    # return if user does not have BrightID verification
    # or there are other errors
    if 'errorMessage' in data:
        logger.info(data['errorMessage'])
        raise Exception(data['errorMessage'])

def processBind(addr, uuidHash, nonce, signature, logger):
    logger.info('processing bind {}'.format(addr))

    # bind
    bind(addr, uuidHash, nonce, signature, logger)

def processMint(addr, uuid, logger):
    logger.info('processing mint {}'.format(uuid))

    # Make sure the address is a current BrightID link
    check_brightid_link(uuid, logger)

    # mint nft
    mint(addr, uuid, logger)
