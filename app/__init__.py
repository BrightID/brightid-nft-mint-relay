from flask import Flask, request, jsonify

from config import *
from cors import *
from relay import *

app = Flask(__name__)

# Index
@app.route(RELAY_BASE_ROUTE + '/')
def index_endpoint():
    app.logger.info('index_endpoint')

    return 'running'

# Bind CORS Preflight
@app.route(RELAY_BASE_ROUTE + '/bind', methods=['OPTIONS'])
def bind_endpoint_options():
    app.logger.info('bind_endpoint_options')

    return cors_preflight_response()

# Mint CORS Preflight
@app.route(RELAY_BASE_ROUTE + '/mint', methods=['OPTIONS'])
def mint_endpoint_options():
    app.logger.info('mint_endpoint_options')

    return cors_preflight_response()

# Bind
@app.route(RELAY_BASE_ROUTE + '/bind', methods=['POST'])
def bind_endpoint():
    app.logger.info('bind_endpoint')

    # Check to make sure a wallet address is specified.
    addr = request.json and request.json.get('addr', '')
    if not addr:
        return cors_response(jsonify({'success': False, 'errorMessage': 'Missing address'})), 400

    uuidHash = request.json and request.json.get('uuidHash', '')
    if not uuidHash:
        return cors_response(jsonify({'success': False, 'errorMessage': 'Missing UUID Hash'})), 400

    nonce = request.json and request.json.get('nonce', '')
    if not nonce:
        return cors_response(jsonify({'success': False, 'errorMessage': 'Missing nonce'})), 400

    signature = request.json and request.json.get('signature', '')
    if not signature:
        return cors_response(jsonify({'success': False, 'errorMessage': 'Missing signature'})), 400

    try:
        processBind(addr, uuidHash, nonce, signature, app.logger)
    except Exception as e:
        return cors_response(jsonify({'success': False, 'errorMessage': str(e)})), 400

    return cors_response(jsonify({'success': True}))

# Mint
@app.route(RELAY_BASE_ROUTE + '/mint', methods=['POST'])
def mint_endpoint():
    app.logger.info('mint_endpoint')

    # http://localhost:5001/brightid-nft-mint-relay/test-mint?addr=0xe031628c95Df01073E95b411388deB48f09F33AA&uuid=d440cd0275534920a6083dbd957ef2da

    # Check to make sure a wallet address is specified.
    addr = request.json and request.json.get('addr', '')
    if not addr:
        return cors_response(jsonify({'success': False, 'errorMessage': 'Missing address'})), 400

    # Check to make sure a wallet address is specified.
    uuid = request.json and request.json.get('uuid', '')
    if not uuid:
        return cors_response(jsonify({'success': False, 'errorMessage': 'Missing uuid'})), 400

    try:
        processMint(addr, uuid, app.logger)
    except Exception as e:
        return cors_response(jsonify({'success': False, 'errorMessage': str(e)})), 400

    return cors_response(jsonify({'success': True}))

# Test Bind
@app.route(RELAY_BASE_ROUTE + '/test-bind', methods=['GET'])
def test_bind_endpoint():
    app.logger.info('test_bind_endpoint')

    # http://localhost:5001/brightid-nft-mint-relay/test-bind?addr=0xe031628c95Df01073E95b411388deB48f09F33AA&uuidHash=0x29defd00aa3991ab2a664af0644e7ad202ed3d347f1d02703bf87ed2157145a6&nonce=4937044&signature=0x014566e7ba27a28803a5e302203cfe11d3687ca899bc96a509c43e01d60b949503bd3215a4de002ac381da75e8f854213a8eb667aaf4fe2b4852386991b446af1b

    # http://localhost:5001/brightid-nft-mint-relay/test-bind?addr=0xe031628c95Df01073E95b411388deB48f09F33AA&uuidHash=0xc61618b7e38a233f1fcd244bf6504bfd5215377040437a52aeb740943c83c241&nonce=8670684&signature=0xb02f2cca5805241c280b2bc1d2ec9e2122d8839fbb58f2c8029c910cabb33658367fc83eda1a10e424f8546ac83eb8cd0fa499acecf03d7a4aa7564300d180e21b

    # Check to make sure a wallet address is specified.
    addr = request.args.get('addr', '')
    if not addr:
        return jsonify({'success': False, 'errorMessage': 'Missing address'}), 400

    uuidHash = request.args.get('uuidHash', '')
    if not uuidHash:
        return jsonify({'success': False, 'errorMessage': 'Missing UUID Hash'}), 400

    nonce = request.args.get('nonce', '')
    if not nonce:
        return jsonify({'success': False, 'errorMessage': 'Missing nonce'}), 400

    signature = request.args.get('signature', '')
    if not signature:
        return jsonify({'success': False, 'errorMessage': 'Missing signature'}), 400

    try:
        processBind(addr, uuidHash, nonce, signature, app.logger)
    except Exception as e:
        return jsonify({'success': False, 'errorMessage': str(e)}), 400

    return jsonify({'success': True})

# Test Mint
@app.route(RELAY_BASE_ROUTE + '/test-mint', methods=['GET'])
def test_mint_endpoint():
    app.logger.info('test_mint_endpoint')

    # Check to make sure a wallet address is specified.
    addr = request.args.get('addr', '')
    if not addr:
        return jsonify({'success': False, 'errorMessage': 'Missing address'}), 400

    # Check to make sure a wallet address is specified.
    uuid = request.args.get('uuid', '')
    if not uuid:
        return jsonify({'success': False, 'errorMessage': 'Missing uuid'}), 400

    try:
        processMint(addr, uuid, app.logger)
    except Exception as e:
        return jsonify({'success': False, 'errorMessage': str(e)}), 400

    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
