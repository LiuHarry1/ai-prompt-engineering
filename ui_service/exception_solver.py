from flask import Blueprint, jsonify, request, jsonify, send_file
import os
from service import *
import util.logging_utils as logging_utils

logger = logging_utils.setup_logger('exception_solver')

exception_solver_pb = Blueprint("exception_solver", __name__)

@exception_solver_pb.route('/fix-exception', methods=['POST'])
def fix_exception():
    data = request.json
    # exception_stack = data['exceptionStack']
    # code_snippets = data['codeSnippets']

    print(data)
    # print(exception_stack)
    # print(code_snippets)

    response= exception_solver_service.get_fixedcode_and_rootcause(data)

    # Process the data and determine the fixed code and root cause
    # This is a placeholder for your actual logic
    # fixed_code = "Fixed code based on the provided stack and snippets"
    # root_cause = "Determined root cause of the exception"

    return jsonify({'data': response})

