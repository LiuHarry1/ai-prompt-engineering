from flask import Blueprint, jsonify, request, jsonify, send_file
import os
from service import *
import util.logging_utils as logging_utils

logger = logging_utils.setup_logger('function_calling_robot')

function_calling_robot_pb = Blueprint("function_calling_robot", __name__)

@function_calling_robot_pb.route('/function-calling-robot', methods=['POST', 'GET'])
def react_bot():

    data = request.json
    print("completion...." + str(data))
    if data is None:
        return jsonify({"message": "Invalid JSON data in the request body."}), 400

    conversation = data.get('conversation')

    bot_response  = react_service.get_bot_response(conversation)

    return  jsonify({'bot_response': bot_response} )
