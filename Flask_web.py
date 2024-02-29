from flask import Flask, request, jsonify
import json
from flask_cors import CORS
from ui_service import *
from config import *
import sys
from narrative_format.narrative_format_thread import narrative_format_thread

print('sys.path:',sys.path)
sys.path.append('/export/app/aspen-prompt-engineering')


app = Flask(__name__)
CORS(app)

app.register_blueprint(llama_completion)
app.register_blueprint(text_format)

# Running a daemon thread in backend to format narrative in narrative folder
narrative_format_thread.start()


@app.route('/')
def index():
    return 'welcome to my webpage!'

@app.route('/info')
def info():
    return 'This is prompt engineering project in aspen'


if __name__=="__main__":
    # app.run(use_reloader=False, port=2020,host="127.0.0.1",debug=False)

    from waitress import serve
    serve(app, host="0.0.0.0", port=2020)
