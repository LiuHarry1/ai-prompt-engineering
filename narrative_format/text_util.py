from util import file_util as file_reader
import nltk

from config import *
nltk.data.path.append(Config.NLTK_DATA)
from nltk.tokenize import sent_tokenize



def break_into_sentences(text):
    sentences = sent_tokenize(text)

    result_sentences = []
    for index, sentence in enumerate(sentences):
        print("===="+str(index),sentence)
        result_sentences.append(" ".join(sentence.split()))

    return result_sentences

def break_into_chunk(text, max_len_of_chunk=600):
    sentences = break_into_sentences(text)
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

def split_into_paragraphs(text :str):
    paragraphs = text.split("\n\n")

    return paragraphs

def is_all_uppercase(text :str):
    if text:
        if text[:50] == text[:50].upper():
            return True

    return False

if __name__ == '__main__':

    text = file_reader.read_file(os.path.join(Config.NARRATIVE_RAW,"4.txt"))
    # break_into_sentences(text)
    chunks = break_into_chunk(text)

    for index,  result in enumerate(chunks):
        print('==='+str(index),result)