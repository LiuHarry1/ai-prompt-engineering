from service import *

from narrative_format.format_prompt_engineering import *
from narrative_format.text_util import *
from narrative_format.format_postprocessing import *
from util.pickle_util import *
from config import *
import time

narrative_raw = Config.NARRATIVE_RAW
narrative_sentence_case = Config.NARRATIVE_SENTENCE_CASE
# narrative_list = Config.NARRATIVE_LIST

narrative_spell_correction = Config.NARRATIVE_SPELL_CORRECTION
narrative_formatted = Config.NARRATIVE_FORMATTED


def convert_into_paragraph(input_text):
    prompt = break_into_paragraphs_prompt(input_text)
    result = llama2Server.completion(prompt)
    return result

def get_formatted_sentence(input_text):

    # prompt = sentence_case_spelling_error_prompt(input_text)
    prompt = sentence_case_prompt(input_text)
    result = llama2Server.completion(prompt)
    return result

def format_into_sentence_case(input_text):

    prompt = sentence_case_prompt_old(input_text)
    result = llama2Server.completion(prompt)
    return result
def correct_spell_error(input_text):
    prompt = spell_error_prompt(input_text)
    result = llama2Server.completion(prompt)
    return result

def get_formated_sentences(input_text):

    chunks = break_into_chunk(input_text)
    # chunks = [chunks[1]]
    all_results = []
    for index, chunk in enumerate(chunks):
        result = get_formatted_sentence(chunk)
        if is_all_uppercase(result):
            # break it into smaller chunks and try again
            smaller_chunks = break_into_chunk(chunk, 300)
            for smaller_index, small_chunk in enumerate(smaller_chunks):
                smaller_result = get_formatted_sentence(small_chunk)
                all_results.append(smaller_result)
        else:
            all_results.append(result)

    print("========= print all results for get_formatted_sentences =============")
    for index, result in enumerate(all_results):
        print('===' + str(index), result)

    return all_results

def format_into_sentence_cases(input_text):

    chunks = break_into_chunk(input_text)
    # chunks = [chunks[1]]
    all_results = []
    for index, chunk in enumerate(chunks):
        result = format_into_sentence_case(chunk)
        all_results.append(result)

    print("========= print all results for format_into_sentence_cases =============")
    for index, result in enumerate(all_results):
        print('===' + str(index), result)

    return all_results

def correct_spell_errors(sentence_case_lists):
    all_results = []
    for index, chunk in enumerate(sentence_case_lists):
        result = correct_spell_error(chunk)
        all_results.append(result)

    print("========= print all results for correct_spell_error =============")
    for index, result in enumerate(all_results):
        print('===' + str(index), result)

    return all_results

def post_processing_formatted_sentences(formatted_sentences):

    postprocessed_results = completion_post_processing(formatted_sentences)
    print("===========after post_processing ============")
    for index, result in enumerate(postprocessed_results):
        print('===' + str(index), result)

    return postprocessed_results

def break_into_paragraphs(text):
    print("===========break into paragraph ============")
    result = convert_into_paragraph(text)
    print(result)
    return result


def format_into_paragraphs(file_name):
    start_time = time.time()

    text = read_file(os.path.join(narrative_raw, file_name))

    all_uppercase = is_all_uppercase(text)

    if all_uppercase:
        # no need to convert it into sentence case
        formatted_sentences = get_formated_sentences(text)
        serialize(formatted_sentences, os.path.join(narrative_sentence_case, file_name+".obj"))
        write_list_to_file(formatted_sentences, os.path.join(narrative_sentence_case, file_name))

        formatted_sentences = deserialize(os.path.join(narrative_sentence_case, file_name+".obj"))
        formatted_sentences = post_processing_formatted_sentences(formatted_sentences)
        write_list_to_file(formatted_sentences, os.path.join(narrative_sentence_case, file_name + ".list"))
    else:
        formatted_sentences = break_into_chunk(text)

    formatted_sentences = correct_spell_errors(formatted_sentences)
    formatted_sentences = post_processing_formatted_sentences(formatted_sentences)
    write_list_to_file(formatted_sentences, os.path.join(narrative_spell_correction, file_name))

    formatted_sentences = ' '.join(formatted_sentences)
    write_list_to_file(formatted_sentences, os.path.join(narrative_spell_correction, file_name+ ".oneline"))

    formatted_sentences = read_file(os.path.join(narrative_spell_correction, file_name+ ".oneline"))
    formatted_sentences = format_list(formatted_sentences)
    write_list_to_file(formatted_sentences, os.path.join(narrative_formatted, file_name))


    # formatted_sentences = read_file("../format_postprocessing/" + file_name)
    # format_text = break_into_paragraphs(formatted_sentences)
    # write_list_to_file(format_text, "../format_paragraph/"+file_name)
    #
    # format_text = read_file("../format_paragraph/" + file_name)
    # format_result = format_into_list(format_text)
    # write_list_to_file(format_result, "../format_into_list/" + file_name)

    elapsed_time = time.time() - start_time
    print("Excecution time :", elapsed_time)

    return formatted_sentences

def format_into_list(text):
    print("===========Convert into well-organized text ============")
    paragraphs = split_into_paragraphs(text)
    all_results = []
    for index, paragraph in enumerate(paragraphs):
        prompt = convert_into_list_prompt(paragraph)
        result = llama2Server.completion(prompt)
        all_results.append(result)
        print(index, "---", result)

    return result

if __name__ == '__main__':


    # file_name = "5.txt"
    # formatted_text = format_text(file_name)
    # file_name = "4.txt"
    # formatted_text = format_text(file_name)

    # file_name ="5.txt"
    # formatted_text = format_into_paragraphs(file_name)
    # print(formatted_text)
    #
    # file_name ="4.txt"
    # formatted_text = format_into_paragraphs(file_name)
    # print(formatted_text)
    #
    file_name ="6.txt"
    formatted_text = format_into_paragraphs(file_name)
    print(formatted_text)
    #
    # file_name ="7.txt"
    # formatted_text = format_into_paragraphs(file_name)
    # print(formatted_text)
    #
    # file_name ="8.txt"
    # formatted_text = format_into_paragraphs(file_name)
    # print(formatted_text)

