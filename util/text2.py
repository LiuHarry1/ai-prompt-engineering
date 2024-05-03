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


# Sample text with colons
text = """
Title: Introduction to Natural Language Processing
Author: John Doe
Date: January 1, 2024

Abstract: This paper provides an overview of Natural Language Processing (NLP) techniques and applications.

Keywords: NLP, Machine Learning, Text Analysis
"""

formatted_text = format_colon_text(text)
print(formatted_text)
