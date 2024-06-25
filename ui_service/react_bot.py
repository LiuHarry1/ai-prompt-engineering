from flask import Blueprint, jsonify, request, jsonify, send_file
import os
from service import *
import util.logging_utils as logging_utils

logger = logging_utils.setup_logger('react_robot')

react_robot_pb = Blueprint("react_robot", __name__)

@react_robot_pb.route('/react_robot', methods=['POST', 'GET'])
def react_robot():

    data = request.json
    print("completion...." + str(data))
    if data is None:
        return jsonify({"message": "Invalid JSON data in the request body."}), 400

    conversation = data.get('conversation')

    bot_response, executed_tools  = react_service.get_bot_response(conversation)

    return  jsonify({'bot_response': bot_response, "executed_tools": executed_tools} )
