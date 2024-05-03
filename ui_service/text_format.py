import datetime

from flask import Blueprint, jsonify, request, jsonify, send_file
import os
from config import *
import util.file_util as file_util
from service import *
import time
text_format = Blueprint("text_format", __name__)


@text_format.route('/text/format', methods=['POST'])
def text_async_format():
    print("format ....")

    data = request.json

    if data is None:
        return jsonify({"message": "Invalid JSON data in the request body."}), 400
    print("starting to format text", data)
    text = data.get('text')
    file_name = data.get('name')

    filename = os.path.join(Config.NARRATIVE_RAW, file_name)
    file_util.write_txt_to_file(text, filename)
    print("Finished to format text", data)
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
        print("Starting to format text, text=", text)
        # completion = llama2Server.completion(text)
        completion = "he he "
        elapsed_time = time.time() - start_time
        print("elapsed_time",elapsed_time, "formatted text=",completion)
        return jsonify(completion)
    else:
        return jsonify({})


@text_format.route('/text/formatted_results',  methods=['POST'])
def formatted_results():
    files = os.listdir(Config.NARRATIVE_FORMATTED)
    file_details = []
    for file in files:
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


@text_format.route('/text/format_result/<filename>',  methods=['POST'])
def get_formatted_text(filename):
    formmatted_filepath = os.path.join(Config.NARRATIVE_FORMATTED, filename)
    formatted_text = file_util.read_file(formmatted_filepath)

    raw_filepath = os.path.join(Config.NARRATIVE_RAW, filename)
    raw_text = file_util.read_file(raw_filepath)

    return jsonify({'raw_text':raw_text, 'formatted_text': formatted_text})
