import os

CONTRACT_ABI = '[{"type":"constructor","stateMutability":"nonpayable","inputs":[{"type":"address","name":"verifier","internalType":"address"},{"type":"bytes32","name":"context","internalType":"bytes32"},{"type":"string","name":"name_","internalType":"string"},{"type":"string","name":"symbol_","internalType":"string"}]},{"type":"event","name":"AddressBound","inputs":[{"type":"address","name":"addr","internalType":"address","indexed":true}],"anonymous":false},{"type":"event","name":"ContextSet","inputs":[{"type":"bytes32","name":"context","internalType":"bytes32","indexed":false}],"anonymous":false},{"type":"event","name":"OwnershipTransferred","inputs":[{"type":"address","name":"previousOwner","internalType":"address","indexed":true},{"type":"address","name":"newOwner","internalType":"address","indexed":true}],"anonymous":false},{"type":"event","name":"Transfer","inputs":[{"type":"address","name":"from","internalType":"address","indexed":true},{"type":"address","name":"to","internalType":"address","indexed":true},{"type":"uint256","name":"tokenId","internalType":"uint256","indexed":true}],"anonymous":false},{"type":"event","name":"VerifierSet","inputs":[{"type":"address","name":"verifier","internalType":"address","indexed":false}],"anonymous":false},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"owner","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"bind","inputs":[{"type":"address","name":"owner","internalType":"address"},{"type":"bytes32","name":"uuidHash","internalType":"bytes32"},{"type":"uint256","name":"nonce","internalType":"uint256"},{"type":"bytes","name":"signature","internalType":"bytes"}]},{"type":"function","stateMutability":"pure","outputs":[{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"getUUIDHash","inputs":[{"type":"address","name":"owner","internalType":"address"},{"type":"bytes32","name":"uuidHash","internalType":"bytes32"},{"type":"uint256","name":"nonce","internalType":"uint256"}]},{"type":"function","stateMutability":"pure","outputs":[{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"hashUUID","inputs":[{"type":"bytes32","name":"uuid","internalType":"bytes32"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"mint","inputs":[{"type":"bytes32[]","name":"contextIds","internalType":"bytes32[]"},{"type":"uint256","name":"timestamp","internalType":"uint256"},{"type":"uint8","name":"v","internalType":"uint8"},{"type":"bytes32","name":"r","internalType":"bytes32"},{"type":"bytes32","name":"s","internalType":"bytes32"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"name","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"owner","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"ownerOf","inputs":[{"type":"uint256","name":"tokenId","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"renounceOwnership","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"rescue","inputs":[{"type":"bytes32[]","name":"contextIds","internalType":"bytes32[]"},{"type":"uint256","name":"timestamp","internalType":"uint256"},{"type":"uint256","name":"tokenId","internalType":"uint256"},{"type":"uint8","name":"v","internalType":"uint8"},{"type":"bytes32","name":"r","internalType":"bytes32"},{"type":"bytes32","name":"s","internalType":"bytes32"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"rescue","inputs":[{"type":"bytes32[]","name":"contextIds","internalType":"bytes32[]"},{"type":"uint256","name":"timestamp","internalType":"uint256"},{"type":"uint256","name":"tokenId","internalType":"uint256"},{"type":"uint8","name":"v","internalType":"uint8"},{"type":"bytes32","name":"r","internalType":"bytes32"},{"type":"bytes32","name":"s","internalType":"bytes32"},{"type":"bytes","name":"data","internalType":"bytes"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setContext","inputs":[{"type":"bytes32","name":"context","internalType":"bytes32"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setVerifier","inputs":[{"type":"address","name":"verifier","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"supportsInterface","inputs":[{"type":"bytes4","name":"interfaceId","internalType":"bytes4"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"symbol","inputs":[]},{"type":"function","stateMutability":"pure","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"tokenURI","inputs":[{"type":"uint256","name":"","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"transferOwnership","inputs":[{"type":"address","name":"newOwner","internalType":"address"}]}]'

BRIGHTID_NODE = 'https://app.brightid.org/node/v5'

VERIFICATIONS_URL = BRIGHTID_NODE + '/verifications'

NOT_FOUND = 2
NOT_SPONSORED = 4

LINK_CHECK_NUM = 2
LINK_CHECK_PERIOD = 2
SPONSOR_CHECK_NUM = 6
SPONSOR_CHECK_PERIOD = 10

BIND_RATE_LIMIT_DURATION_MINUTES = os.environ['BIND_RATE_LIMIT_DURATION_MINUTES']

RELAY_BASE_ROUTE = os.environ['RELAY_BASE_ROUTE']

RPC_URL = os.environ['RPC_URL']
CHAINID = os.environ['CHAINID']
# GAS = os.environ['GAS']
# GAS_PRICE = os.environ['GAS_PRICE']

HOST = os.environ['HOST']
PORT = os.environ['PORT']
CONTEXT = os.environ['CONTEXT']
CONTRACT_ADDRESS = os.environ['CONTRACT_ADDRESS']
RELAYER_ADDRESS = os.environ['RELAYER_ADDRESS']
RELAYER_PRIVATE = os.environ['RELAYER_PRIVATE']
