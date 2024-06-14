from flask import Blueprint, jsonify, request, jsonify, send_file
import os
from service import *
import util.logging_utils as logging_utils

logger = logging_utils.setup_logger('chatbot')

chatbot_pb = Blueprint("chatbot", __name__)

@chatbot_pb.route('/chatbot', methods=['POST', 'GET'])
def chatbot():

    data = request.json
    print("completion...." + str(data))
    if data is None:
        return jsonify({"message": "Invalid JSON data in the request body."}), 400

    conversation = data.get('conversation')

    bot_response  = chat_service.get_bot_message(conversation)

    return  jsonify({'bot_response': bot_response} )
