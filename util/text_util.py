from util import file_util as file_reader
import nltk

from config import *
nltk.data.path.append(Config.NLTK_DATA)
from nltk.tokenize import sent_tokenize
import re


def break_into_sentences(text):
    text = " ".join(text.split())
    sentences = sent_tokenize(text)

    result_sentences = []
    for index, sentence in enumerate(sentences):
        print("===="+str(index),sentence)
        result_sentences.append(" ".join(sentence.split()))

    return result_sentences

def break_into_sentence_enhancement(text):
    result_sentences = break_into_sentences(text)
    result_sentences = remove_period_sentence(result_sentences)
    result_sentences = others(result_sentences)
    raw_text = '\n\n'.join(result_sentences)
    return raw_text

def others(sentences):
    appended_text = []
    number_list_text = ""

    for sentence in sentences:
        if re.match(r'^\d+\.$', sentence.strip()):
            number_list_text = sentence
        else:
            if number_list_text:
                appended_text.append(number_list_text + " " + sentence)
                number_list_text = ""
            else:
                appended_text.append(sentence)


    return appended_text

def remove_period_sentence(sentences):
    sentences = [sentence for sentence in sentences if sentence !="."]

    # for i in range(len(sentences)):
    #     print(i)
    #     if sentences[i]==".":
    #         del sentences[i]
    return sentences



def break_into_chunk(text, max_len_of_chunk=600):
    sentences = break_into_sentences(text)
    sentences = break_into_smaller_text(sentences)
    cur_chunk = ""
    chunks = []
    for index ,sentence in enumerate(sentences):

        if len(cur_chunk) + len(sentence)< max_len_of_chunk:
            cur_chunk = cur_chunk +" " +sentence
        else:
            if len(cur_chunk)==0:
                chunks.append(sentence)
            else:
                chunks.append(cur_chunk)
                cur_chunk = sentence
    if len(cur_chunk) != 0:
        chunks.append(cur_chunk)

    return chunks

def break_into_smaller_text(sentences, max_len_of_chunk=600):
    smaller_sentence = []
    for index, sentence in enumerate(sentences):
        if len(sentence) >max_len_of_chunk:
            smaller_sentences = sentence.split(',')
            smaller_sentences = [smaller_sentence + "," for smaller_sentence in smaller_sentences]
            smaller_sentence.extend(smaller_sentences)
        else:
            smaller_sentence.append(sentence)

    return smaller_sentence

def split_into_paragraphs(text :str):
    paragraphs = text.split("\n\n")

    return paragraphs

def is_all_uppercase(text :str):
    if text:
        if text[:50] == text[:50].upper():
            return True

    return False