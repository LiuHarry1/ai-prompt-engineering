from flask import Blueprint, jsonify, request, jsonify, send_file
import os
from service import *
import util.logging_utils as logging_utils

logger = logging_utils.setup_logger('jira_assistant')

jira_assistant = Blueprint("jira_assistant", __name__)

@jira_assistant.route('/generate-jira-message', methods=['POST', 'GET'])
def generate_jira_message():

    data = request.json
    print("completion...." + str(data))
    if data is None:
        return jsonify({"message": "Invalid JSON data in the request body."}), 400

    user_input = data.get('user_input')

    jira_message  = jira_assistant_service.get_jira_message(user_input)

    return  jsonify({'jira_message': jira_message} )
