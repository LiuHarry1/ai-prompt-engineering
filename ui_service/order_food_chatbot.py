from flask import Blueprint, jsonify, request, jsonify, send_file
import os
from service import *
import util.logging_utils as logging_utils

logger = logging_utils.setup_logger('order_food_chatbot')

order_food_chatbot = Blueprint("order_food_chatbot", __name__)

@order_food_chatbot.route('/order-food-support', methods=['POST', 'GET'])
def order_food():
    print("completion....")

    data = request.json

    if data is None:
        return jsonify({"message": "Invalid JSON data in the request body."}), 400

    last_prompt = data.get('last_prompt')
    user_query = data.get('user_message')
    conversations = data.get('conversation')

    bot_response, last_prompt  = order_food_service.order_food(last_prompt, user_query, conversations)


    return  jsonify({'last_prompt': last_prompt, 'bot_response': bot_response} )
