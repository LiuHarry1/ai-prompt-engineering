from flask import Blueprint, jsonify, request, jsonify, send_file
import os


admin_bp = Blueprint("admin", __name__)

base_url_file = './data/'

@admin_bp.route('/admin/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return jsonify({"message": "No file part" })

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    if file:
        filename = os.path.join(base_url_file, file.filename)
        file.save(filename)

        return jsonify({"message": "File uploaded successfully"})

    return jsonify({"message": "file is empty"})


@admin_bp.route('/admin/download', methods=['GET'])
def download_file():
    filename = base_url_file+'knowledge_base.xlsx'  # Adjust the path as needed
    return send_file(filename, as_attachment=True)
