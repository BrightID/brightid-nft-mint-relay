import time
import requests
from web3 import Web3
from web3.middleware import geth_poa_middleware
from config import *
from fetch_events import *

w3 = Web3(Web3.WebsocketProvider(RPC_URL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def transact(f):
    nonce = w3.eth.getTransactionCount(RELAYER_ADDRESS, 'pending')
    tx = f.buildTransaction({
        'chainId': CHAINID,
        # 'gas': int(GAS),
        # 'gasPrice': int(GAS_PRICE),
        'nonce': nonce,
    })
    signed_txn = w3.eth.account.sign_transaction(tx, private_key=RELAYER_PRIVATE)
    w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    receipt = w3.eth.waitForTransactionReceipt(signed_txn['hash'])
    assert receipt['status'], '{} failed'.format(tx)

def toBase32(inputStr):
    return '0x' + inputStr.encode('utf-8').hex()

def checkBrightIDLink(contextId, logger):
    logger.info('checking BrightID link {}'.format(contextId))

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
        raise Exception('Could not determine that uuid is linked to BrightID.')

def checkBrightIDSponsorship(contextId, logger):
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

def checkBindAllowed(addr, logger):
    logger.info('check bind limit for {}'.format(addr))

    # Format address to checksum format
    addr = Web3.toChecksumAddress(addr)

    # only allow a bind every n minutes per address
    rateLimitLengthSeconds = 60 * int(BIND_RATE_LIMIT_DURATION_MINUTES)

    # each block takes ~5 seconds
    blockLengthSeconds = 5

    # Number of blocks during the rate limit time
    blocksToCheck = rateLimitLengthSeconds / blockLengthSeconds

    # Current block
    currentBlock = w3.eth.blockNumber

    # First block to check
    fromBlock = currentBlock - blocksToCheck

    # fromBlock = 0 # DEBUG - Check all blocks
    # fromBlock = currentBlock # DEBUG - Check no blocks

    # All AddressBound events since the start of the rate limit period
    events = list(fetch_events(contract.events.AddressBound, from_block=fromBlock))

    # If any of the events are for this address throw an error
    for event in events:
        if (event.args.addr.lower() == addr.lower()):
            logger.info('{} has reach bind limit'.format(addr))
            raise Exception('This address has reached the bind rate limit.'.format(addr))

def checkMintAllowed(addr, logger):
    # Format address to checksum format
    addr = Web3.toChecksumAddress(addr)

    # Query user's nft balance.
    balance = contract.functions.balanceOf(addr).call()

    # balance = 0 # DEBUG

    # Check to see if the user is already verified.
    if balance > 0:
        logger.info('{} has minted'.format(addr))
        raise Exception('This address has already minted.'.format(addr))

def bind(addr, uuidHash, nonce, signature, logger):
    logger.info('binding {}'.format(addr))
    logger.info('binding {}'.format(uuidHash))
    logger.info('binding {}'.format(nonce))
    logger.info('binding {}'.format(signature))

    # Check if calling bind via the relay is allowed.
    checkMintAllowed(addr, logger)
    checkBindAllowed(addr, logger)

    # Format address to checksum format
    addr = Web3.toChecksumAddress(addr)

    # Convert nonce to int
    nonce = int(nonce)

    # Run the sponsorship transaction.
    logger.info('binding {}'.format(addr))
    transact(contract.functions.bind(addr, uuidHash, nonce, signature))

    logger.info('{} bound'.format(addr))

def mint(addr, uuid, logger):
    logger.info('minting {}'.format(addr))
    logger.info('minting {}'.format(uuid))

    # Check if calling bind via the relay is allowed.
    checkMintAllowed(addr, logger)

    # Format address to checksum format
    addr = Web3.toChecksumAddress(addr)

    # Get the contract data that will be used as
    # input for the verification transaction.
    data = requests.get(VERIFICATIONS_URL + '/' + CONTEXT + '/' + uuid + '?signed=eth&timestamp=seconds').json()
    logger.info('Query verification signing data')
    logger.info(data)

    data = data['data']

    # Convert all contextIds to byte32
    # logger.info(data['contextIds'])
    data['contextIds'] = list(map(toBase32, data['contextIds']))
    logger.info(data['contextIds'])

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

def processBind(addr, uuidHash, nonce, signature, logger):
    logger.info('processing bind {}'.format(addr))

    # bind
    bind(addr, uuidHash, nonce, signature, logger)

def processMint(addr, uuid, logger):
    logger.info('processing mint {}'.format(uuid))

    # Make sure the address is a current BrightID link
    checkBrightIDLink(uuid, logger)

    # mint nft
    mint(addr, uuid, logger)
