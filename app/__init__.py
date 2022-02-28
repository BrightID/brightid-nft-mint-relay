import json
from flask import Flask, request, jsonify

from config import *
from cors import *
from relay import *

app = Flask(__name__)

def format_error(e):
    if ("'code'" in str(e)) & ("'message'" in str(e)):
        errorJsonStr = str(e).replace("'", '"')
        errorJson = json.loads(errorJsonStr)

        app.logger.info(errorJson['code'])
        app.logger.info(errorJson['message'])
        app.logger.info(errorJson)
        app.logger.info('code' in errorJson)
        app.logger.info('message' in errorJson)

        if ('code' in errorJson) and ('message' in errorJson):
            return jsonify({'success': False, 'error': {'code': errorJson['code'], 'message': errorJson['message']}})

    if ('code' in e) and ('message' in e):
        return jsonify({'success': False, 'error': {'code': e['code'], 'message': e['message']}})

    if ('message' in e):
        return jsonify({'success': False, 'error': {'code': 0, 'message': e['message']}})

    return jsonify({'success': False, 'error': {'code': 0, 'message': str(e)}})

def format_success():
    return jsonify({'success': True})

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
        return cors_response(format_error('Missing address')), 400

    uuidHash = request.json and request.json.get('uuidHash', '')
    if not uuidHash:
        return cors_response(format_error('Missing  UUID Hash')), 400

    nonce = request.json and request.json.get('nonce', '')
    if not nonce:
        return cors_response(format_error('Missing nonce')), 400

    signature = request.json and request.json.get('signature', '')
    if not signature:
        return cors_response(format_error('Missing signature')), 400

    try:
        processBind(addr, uuidHash, nonce, signature, app.logger)
    except Exception as e:
        return cors_response(format_error(e)), 400

    return cors_response(format_success())

# Mint
@app.route(RELAY_BASE_ROUTE + '/mint', methods=['POST'])
def mint_endpoint():
    app.logger.info('mint_endpoint')

    # Check to make sure a wallet address is specified.
    addr = request.json and request.json.get('addr', '')
    if not addr:
        return cors_response(format_error('Missing address')), 400

    # Check to make sure a wallet address is specified.
    uuid = request.json and request.json.get('uuid', '')
    if not uuid:
        return cors_response(format_error('Missing uuid')), 400

    try:
        processMint(addr, uuid, app.logger)
    except Exception as e:
        return cors_response(format_error(e)), 400

    return cors_response(format_success())

# Test Bind
@app.route(RELAY_BASE_ROUTE + '/test-bind', methods=['GET'])
def test_bind_endpoint():
    app.logger.info('test_bind_endpoint')

    # Check to make sure a wallet address is specified.
    addr = request.args.get('addr', '')
    if not addr:
        return format_error('Missing address'), 400

    uuidHash = request.args.get('uuidHash', '')
    if not uuidHash:
        return format_error('Missing UUID Hash'), 400

    nonce = request.args.get('nonce', '')
    if not nonce:
        return format_error('Missing nonce'), 400

    signature = request.args.get('signature', '')
    if not signature:
        return format_error('Missing signature'), 400

    try:
        processBind(addr, uuidHash, nonce, signature, app.logger)
    except Exception as e:
        return format_error(e), 400

    return format_success()

# Test Mint
@app.route(RELAY_BASE_ROUTE + '/test-mint', methods=['GET'])
def test_mint_endpoint():
    app.logger.info('test_mint_endpoint')

    # Check to make sure a wallet address is specified.
    addr = request.args.get('addr', '')
    if not addr:
        return format_error('Missing address'), 400

    # Check to make sure a wallet address is specified.
    uuid = request.args.get('uuid', '')
    if not uuid:
        return format_error('Missing uuid'), 400

    try:
        processMint(addr, uuid, app.logger)
    except Exception as e:
        return format_error(e), 400

    return format_success()

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
