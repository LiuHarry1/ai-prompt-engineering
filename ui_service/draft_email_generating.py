from flask import Blueprint, jsonify, request, jsonify, send_file
import os
from service import *
import util.logging_utils as logging_utils

logger = logging_utils.setup_logger('draft_email_generating')

draft_email_generating = Blueprint("draft_email_generating", __name__)

@draft_email_generating.route('/generate_draft_email', methods=['POST', 'GET'])
def generate_draft_email():
    print("completion....")

    data = request.json
    print(len(data), data)

    if data is None:
        return jsonify({"message": "Invalid JSON data in the request body."}), 400
    conversations = data["conversations"]
    print(type(conversations))
    conversation = conversations[0]

    # generated_draft_email =draft_email_generating_service.generate_draft_email(conversations)

    generated_draft_email = """
Hi xx,

please check this 1.

Thanks
Harry
                    """

    return  jsonify({'generated_draft_email': generated_draft_email} )



