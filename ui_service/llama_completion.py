from flask import Blueprint, jsonify, request, jsonify, send_file
import os
from service import *
import util.logging_utils as logging_utils
# import pypandoc

logger = logging_utils.setup_logger('llama_completion')

llama_completion = Blueprint("llama_completion", __name__)


@llama_completion.route('/llama/completion', methods=['POST'])
def completion():
    print("completion....")

    data = request.json

    if data is None:
        return jsonify({"message": "Invalid JSON data in the request body."}), 400

    prompt = data.get('prompt')
    llm_name = data.get('llm_name')
    temperature = data.get('temp')
    top_p = data.get('topP')
    top_k = data.get('topK')
    n_predict = data.get('nPredict')
    frequency_penalty =  data.get('frequency_penalty')
    presence_penalty = data.get('presence_penalty')
    logger.info('completion() data:'+str(data))
    if prompt:
        result_completion = LLMFactory.create_llm(llm_name).completion(prompt, temperature, top_p, top_k, n_predict, presence_penalty, frequency_penalty )
        #Q: replace \begin{code}  with <code> in result_completion and replace \end{code} with </code>
        result_completion = result_completion.replace("\\begin{code}", "```")
        result_completion = result_completion.replace("\\end{code}", "```")
        # Q: replace \item with \n\n- in result_completion
        # result_completion = result_completion.replace("\\item", "\n\n-")
        #Q: convert the latex code in result_completion to text

        #Q HOW TO FIX THIS ERROR:
        #OSError: No pandoc was found: either install pandoc and add it

        # result_completion = pypandoc.convert_text(result_completion, 'plain', format='latex')
        print(result_completion)
        return jsonify({'completion': result_completion})

    return ""