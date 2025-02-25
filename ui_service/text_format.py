import datetime

from flask import Blueprint, jsonify, request, jsonify, send_file
import os
from config import *
import util.file_util as file_util
import util.text_util as text_util
from service import *
import time
import narrative_format.format_prompt_engineering as format_prompt_engineering
import util.logging_utils as logging_utils
from prompts import *

logger = logging_utils.setup_logger('text_format')
text_format = Blueprint("text_format", __name__)


@text_format.route('/text/format', methods=['POST'])
def text_async_format():
    print("format ....")

    data = request.json

    if data is None:
        return jsonify({"message": "Invalid JSON data in the request body."}), 400
    logger.info("starting to format text"+data)
    text = data.get('text')
    file_name = data.get('name')

    filename = os.path.join(Config.NARRATIVE_RAW, file_name)
    file_util.write_txt_to_file(text, filename)
    logger.info("Finished to format text"+ data)
    return jsonify("success")


@text_format.route('/text/sync_format', methods=['POST'])
def text_sync_format():
    print("format ....")

    data = request.json

    if data is None:
        return jsonify({"message": "Invalid JSON data in the request body."}), 400

    text = data.get('text')
    if text:
        start_time = time.time()
        logger.info("Starting to format text, text="+text)
        completion = llama3Server.completion(text)

        elapsed_time = time.time() - start_time
        logger.info("elapsed_time:"+ str(elapsed_time) +"formatted text="+completion)
        return jsonify(completion)
    else:
        return jsonify({})


@text_format.route('/text/formatted_results',  methods=['POST'])
def formatted_results():
    files = os.listdir(Config.NARRATIVE_FORMATTED)
    file_details = []
    for file in files:
        if file.endswith(".oneline"):
            continue
        filepath = os.path.join(Config.NARRATIVE_FORMATTED, file)
        created_time= os.path.getctime(filepath)
        created_date = datetime.datetime.fromtimestamp(created_time).strftime('%Y-%m-%d %H:%M:%S')
        file_details.append({'name': file, 'created_date': created_date})
    sorted_files =sorted(file_details, key=lambda  x : x['created_date'],  reverse=True)
    return jsonify(sorted_files)


@text_format.route('/text/raw_results')
def raw_results():
    files = os.listdir(Config.NARRATIVE_RAW)
    file_details = []
    for file in files:
        filepath = os.path.join(Config.NARRATIVE_RAW, file)
        created_time= os.path.getctime(filepath)
        created_date = datetime.datetime.fromtimestamp(created_time).strftime('%Y-%m-%d %H:%M:%S')
        file_details.append({'name':file, 'created_date': created_date})
    sorted_files =sorted(file_details, key=lambda  x : x['created_date'])
    return jsonify(sorted_files)


@text_format.route('/text/formatted_result/download/<filename>')
def download_formatted_file(filename):
    filepath = os.path.join(Config.NARRATIVE_FORMATTED, filename)
    return send_file(filepath, as_attachment=True)

@text_format.route('/text/raw_result/download/<filename>')
def download_raw_file(filename):
    filepath = os.path.join(Config.NARRATIVE_RAW, filename)
    return send_file(filepath, as_attachment=True)


@text_format.route('/text/format_result',  methods=['GET'])
def get_formatted_text():
    file_name = request.args.get('file_name')

    formatted_filepath = os.path.join(Config.NARRATIVE_FORMATTED, file_name)

    # formatted_filepath = os.path.join(Config.NARRATIVE_FORMATTED, file_name)

    formatted_text = file_util.read_file(formatted_filepath)
    formatted_text = text_util.break_into_sentence_enhancement(formatted_text)

    raw_filepath = os.path.join(Config.NARRATIVE_RAW, file_name)
    raw_text = file_util.read_file(raw_filepath)
    raw_text = text_util.break_into_sentence_enhancement(raw_text)


    return jsonify({'raw_text':raw_text, 'formatted_text': formatted_text})

@text_format.route('/text/text_format_prompt',  methods=['GET'])
def get_text_format_prompt():

    return jsonify({'prompt':format_prompt_engineering.format_sentence_case_prompt})

@text_format.route('/text/text_summary_prompt',  methods=['GET'])
def get_text_summary_prompt():

    return jsonify({'prompt':format_prompt_engineering.text_summary_prompt})

@text_format.route('/text/prompt_templates',  methods=['GET'])
def get_all_prompts():

    all_prompt_templates = [{'title': 'common Prompt', 'prompt': format_prompt_engineering.common_prompt},
                            {'title': 'Text Summary Prompt', 'prompt':  format_prompt_engineering.text_summary_prompt},
                            {'title': 'Text Format Prompt', 'prompt':  format_prompt_engineering.format_sentence_case_prompt},
                            {'title': "Text Translation Prompt", 'prompt': format_prompt_engineering.text_translation_prompt},
                            {'title': "Function Calling Prompt", 'prompt': format_prompt_engineering.tool_choose_prompt},
                            {'title': "Problem Resolver Prompt", "prompt": format_prompt_engineering.problem_resolver_prompt},
                            {'title': "ReAct Prompt", "prompt": react_prompt.react_agent_prompt_template},
                            {'title': "Chatbot Prompt", "prompt": chatbot_prompt.prompt_template},
                            ]

    return jsonify(all_prompt_templates)
