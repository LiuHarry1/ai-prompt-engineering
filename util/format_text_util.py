
def format_paragraphs(text, indent_size=4, width=80):
    paragraphs = text.strip().split('\n\n')
    formatted_text = []

    for paragraph in paragraphs:
        lines = paragraph.split('\n')
        formatted_lines = []

        for line in lines:
            words = line.split()
            formatted_line = ' ' * indent_size

            for word in words:
                if len(formatted_line) + len(word) + 1 <= width:
                    formatted_line += word + ' '
                else:
                    formatted_lines.append(formatted_line.rstrip())
                    formatted_line = ' ' * indent_size + word + ' '

            formatted_lines.append(formatted_line.rstrip())

        formatted_text.append('\n'.join(formatted_lines))

    return '\n\n'.join(formatted_text)


def format_colon_text(text):
    lines = text.strip().split('\n')
    formatted_text = []

    for line in lines:
        if ":" in line:
            header, content = line.split(":", 1)
            formatted_line = f"{header.strip().capitalize()}: {content.strip()}"
        else:
            formatted_line = line.strip()

        formatted_text.append(formatted_line)

    return '\n'.join(formatted_text)

def sentence_segmentation():

    import nltk
    from nltk.tokenize import sent_tokenize, word_tokenize

    # Sample text
    text = """
    Natural Language Processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language, in particular how to program computers to process and analyze large amounts of natural language data.
    NLP tasks include text translation, sentiment analysis, named entity recognition, speech recognition, and language generation.
    """

    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Tokenize each sentence into words
    tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]

    # Join the tokenized words back into sentences with proper punctuation
    formatted_sentences = [" ".join(sentence) for sentence in tokenized_sentences]

    # Join the formatted sentences into paragraphs
    formatted_text = "\n\n".join(formatted_sentences)

    print(formatted_text)
