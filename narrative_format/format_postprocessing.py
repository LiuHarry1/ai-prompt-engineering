import re

from util.file_util import *

def substring_to_word(input_string:str, word):
    index = input_string.find(word)

    if index != -1:
        return input_string[:index]
    else:
        return input_string


def remove_notes(completion):
    completion = substring_to_word(completion, "Note:")
    return completion

def remove_repetive_examples(completion):
    completion = substring_to_word(completion, "Input Text:")

    return completion



def completion_post_processing(completion_list):

    processed_completions =[]
    for completion in completion_list:
        completion = remove_notes(completion)
        completion = remove_repetive_examples(completion)
        completion = substring_to_word(completion, "Please provide the next input text.")
        completion = substring_to_word(completion, "Explanation:")
        completion = completion.strip()
        completion = remove_line_breaks(completion)
        processed_completions.append(completion)

    return processed_completions

def format_list_old(text):


    lists = ['B)', 'A)', 'C)', 'D)','E)','1)', '2)', '3)', '4)','1.', '2.', '3.', '4.', '(i)', '(ii)', '(iii)', '(a)', '(b)', '(c)', '(d)']
    words = []
    spaces = []
    for word in text.split():
        if word in lists:
            words.append('\n')
        words.append(word)


    return " ".join(words);


def format_list(text):
    lists_dict = {
        "list1":[ 'A)', 'B)', 'C)', 'D)'],
        "list2": ['1)', '2)', '3)', '4)'],
        "list3": ['1.', '2.', '3.', '4.'],
        "list4": ['(i)', '(ii)', '(iii)'],
        "list5": ['(a)', '(b)', '(c)', '(d)'],
        "list6": ['(A)', '(B)', '(C)', '(D)']

    }
    words = []
    list_name_stack = []

    for word in text.split():
        is_list_word = False
        for list_name, list_value in lists_dict.items():
            if word in list_value:
                is_list_word =True
                # print('is_list_word', word)
            if word == list_value[0]:
                list_name_stack.append(list_name)
                # print('append()', list_name, word)
            elif word in list_value[1:]:
                if len(list_name_stack) ==0:
                    list_name_stack.append(list_name)
                if  list_name != list_name_stack[len(list_name_stack)-1]:
                    # print('pop()', word)
                    list_name_stack.pop()
        if is_list_word:
            words.append('\n')
            if len(list_name_stack) >1:
                words.append((len(list_name_stack)-1) *'  ')
                # print('indent:', len(list_name_stack) *' ')

        words.append(word)

    return " ".join(words);



def remove_line_breaks(text: str):
    # return text.replace('\n', ' ').replace('\r', '')
    return " ".join([word for word in text.split()])

def remove_line_breaks_old(text):
    # Remove multiple line breaks from the beginning and end of the text
    cleaned_text = re.sub(r'^\n+', '', text)
    cleaned_text = re.sub(r'\n+$', '', cleaned_text)
    return cleaned_text

if __name__ == '__main__':

    # file_name = "4.txt"
    # formatted_sentences = read_file("../format_postprocessing/" + file_name)
    #
    # text = format_list(formatted_sentences)
    # print(text)

    file_name = "4.txt"
    formatted_sentences = read_file("../format_result/format_postprocessing/" + file_name)

    text = format_list(formatted_sentences)
    print(text)



