from flask import Blueprint, jsonify, request, jsonify, send_file
import os
from service import *
import util.logging_utils as logging_utils

logger = logging_utils.setup_logger('order_food_chatbot')

order_food_chatbot = Blueprint("order_food_chatbot", __name__)

@order_food_chatbot.route('/order_food', methods=['POST', 'GET'])
def order_food():
    print("completion....")

    data = request.json

    if data is None:
        return jsonify({"message": "Invalid JSON data in the request body."}), 400

    previous_prompt = data.get('previous_prompt')
    user_query = data.get('user_query')

    prompt, conversation = order_food_service.order_food(previous_prompt, user_query)


    return  jsonify({'prompt': prompt, 'conversation': conversation} )
