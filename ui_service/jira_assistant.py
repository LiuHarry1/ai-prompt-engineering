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


# In-memory storage for user cases
user_cases = []

# Endpoint to save feedback
@jira_assistant.route('/save-feedback', methods=['POST'])
def save_feedback():
    data = request.json

    # Extract the content and feedback from the received data
    user_input = data.get('userInput', '')
    summary = data.get('summary', '')
    description = data.get('description', '')
    acceptance_criteria = data.get('acceptanceCriteria', '')
    development_required = data.get('developmentRequired', '')
    story_point = data.get('storyPoint', '')
    feedback = data.get('feedback', '')

    # Save the data to the in-memory list
    user_case = {
        'userInput': user_input,
        'summary': summary,
        'description': description,
        'acceptanceCriteria': acceptance_criteria,
        'developmentRequired': development_required,
        'storyPoint': story_point,
        'feedback': feedback
    }
    user_cases.append(user_case)

    # Respond with a success message
    return jsonify({'message': 'Feedback received successfully'}), 200

# Endpoint to retrieve all user cases
@jira_assistant.route('/jira/user-cases', methods=['GET'])
def get_user_cases():
    return jsonify(user_cases), 200
