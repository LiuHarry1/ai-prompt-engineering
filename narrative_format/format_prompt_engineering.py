# input_text will be sentence

format_sentence_case_prompt = """please format the following text into sentence case only, no answer and explanation required. don't miss any words.
Input Text: "(QUOTE) (TO THE AGENT) I/WE, AN APPLYING SHAREHOLDER, HEREBY MAKE THE REPRESENTATIONS AND ASSURANCE, UPON THE APPLIC ATION FOR TENDER OFFER (HEREAFTER REFERS TO 'THE OFFER') FOR THE COMMON STO CKS OF PAYROLL INC. (4489/JP3836150007)."
Formatted Text: "(Quote) (To the agent) I/we, an applying shareholder, hereby make the representations and assurance, upon the application for tender offer (hereafter refers to 'the offer') for the common stocks of Payroll Inc. (4489/JP3836150007)."
Input Text: "THERE IS BLANK SPACE IN THE MID DLE OF WORDS"
Formatted Text: "There is blank space in the middle of words"
Input Text: "{text}"
Formatted Text: """

text_summary_prompt = """summarize the following text. 
text: "{text}"
summarized text: """

common_prompt = """
<s>[INST] <<SYS>>
{{ system_prompt }}
<</SYS>>

{{ user_message }} [/INST]
"""

text_translation_prompt = """translate the following text to English language only, no answer and explanation required. don't miss any words.
text:"{text}"
result:
"""

problem_resolver_prompt = """You are a helpful, respectful and honest assistant. Always answer as helpfully as possible.
User: {text}
Assistant:
"""

tool_choose_prompt = """Tool Descriptions:

1. Calculator Tool: Performs basic arithmetic operations such as addition, subtraction, multiplication, and division. Parameters: Operation, Number 1, Number 2
2. Weather Tool: Provides current weather information and forecasts based on location input. Parameters: Location, Date
3. Translation Tool: Translates text from one language to another. Parameters: Source Language, Target Language, Text
4. Dictionary Tool: Provides definitions, synonyms, antonyms, and examples of word usage. Parameters: Word

User Query:

"What will the weather be like in New York tomorrow?"

Task:

Based on the user's query and the descriptions of the available tools, decide which tool is most suitable for addressing the query. If a suitable tool is found, also provide the necessary parameters. If none of the tools are appropriate for the query, output "NA". the template of response would be [tool name:xxx, parameters:xxx] .
Response:
"""


def sentence_case_prompt_old(input_text):
    prompt = """
format the following text into sentence case, no answer and explanation required, no note required, don't miss any words.
Input Text: "THERE IS BLANK SPACE IN THE MID DLE OF WORDS"
Formatted Text: "There is blank space in the middle of words"
Input Text: "EACH NON-TRANSFERABLE CVR REPRESENTS THE RIGHT TO RECEIVE A CONTINGENT PAYMENT OF UP TO USD 5.00 IN CASH (THE MILESTONE PAYMENT)"
Formatted Text: "Each non-transferable CVR represents the right to receive a contingent payment of up to USD 5.00 in cash (the milestone payment),"
Input Text:"{text}"
Formatted Text:
    """
    prompt = prompt.format(text=input_text)
    print(prompt)
    return prompt

def spell_error_prompt(input_text):
    prompt = """correct spell error word only, no answer and explanation required, no note required, don't miss any words.
Input Text: "{text}"
Formatted Text: """
    prompt = prompt.format(text=input_text)
    print(prompt)
    return prompt

def sentence_case_prompt(input_text):
    prompt = format_sentence_case_prompt
    prompt = prompt.format(text=input_text)
    print(prompt)
    return prompt

def sentence_case_spelling_error_prompt(input_text):
    prompt = """
format the following text into sentence case and correct spelling error, no answer and explanation required, no note required, no Input Text requried,  don't miss any words.
Input Text: "THERE IS BLANK SPACE IN THE MID DLE OF WORDS."
Formatted Text: "There is blank space in the middle of words."
Input Text: "EACH NON-TRANSFERABLE CVR REPRESENTS THE RIGHT TO RECEIVE A CONTINGENT PAYMENT OF UP TO USD 5.00 IN CASH (THE MILESTONE PAYMENT),"
Formatted Text: "Each non-transferable CVR represents the right to receive a contingent payment of up to USD 5.00 in cash (the milestone payment),"
Input Text:"{text}"
Formatted Text:
        """
#     prompt = """
# format the following text into sentence case  and correct spelling error, no answer and explanation required, no note required, don't miss any words.
# Input Text: "THERE IS BLANK SPACE IN THE MID DLE OF WORDS"
# Formatted Text: "There is blank space in the middle of words"
# Input Text: "EACH NON-TRANSFERABLE CVR REPRESENTS THE RIGHT TO RECEIVE A CONTINGENT PAYMENT OF UP TO USD 5.00 IN CASH (THE MILESTONE PAYMENT)"
# Formatted Text: "Each non-transferable CVR represents the right to receive a contingent payment of up to USD 5.00 in cash (the milestone payment),"
# Input Text:"{text}"
# Formatted Text:
#     """

#     prompt = """
# format the following text with sentence case  and correct spelling error, no answer and explanation required, no note required.
# Input Text: "FORMAT TEXT INCLUDES BELOW POINTS (I) FORMAT IT INTO SENTENCE CASE, (II) CORRECT SPELLING ERROR."
# Formatted Text: "Format text includes below points
# (I) Format it into sentence case.
# (II) Correct spelling error."
# Input Text: "THERE IS ALANK SPACE IN THE MID DLE OF WORDS"
# Formatted Text: "There is blank space in the middle of words"
# Input Text:"{text}"
# Formatted Text:
#     """

#     prompt = """
# format the following text with sentence case and if it has a certain type of list (like (1) (2) or 1) 2) or A) B) ..) then format it to well-structured list  and correct spelling error, no answer and explanation required.
# Input Text: "FORMAT TEXT INCLUDES BELOW POINTS (I) FORMAT IT INTO SENTENCE CASE, (II) CORRECT SPELLING ERROR."
# Formatted Text: "Format text includes below points
# (I) Format it into sentence case.
# (II) Correct spelling error."
# Input Text:"{text}"
# Formatted Text:
#         """
#     prompt = """
# format the following text with sentence case and if it has a certain type of list (like (1) (2) or 1) 2) or A) B) ..) then format it to well-structured list and correct spelling error, no answer and explanation required.
# Input Text:"{text}"
# Formatted Text:
#     """
    prompt = prompt.format(text=input_text)
    print(prompt)
    return prompt

def break_into_paragraphs_prompt(input_text):

    prompt = """
Convert the following raw text into a neatly formatted multiple paragraphs using space character and line break.
Input Text:"{text}"
Formatted Text:
    """

#     prompt = """
# break the following text into paragraphs, ensure you are not missing any words
# Input Text:"{text}"
# Formatted Text:
#             """
#     prompt = """
# format the following text into multiple paragraphs.The following text includes numbered lists, bulleted lists and alphabetical lists.  don't miss any words
# Input Text:"{text}"
# Formatted Text:
#         """

    prompt = prompt.format(text=input_text)
    print(prompt)
    return prompt

def convert_into_list_prompt(input_text):
    prompt = """There is a following plain input text that contains a mixture of numbered lists and bullet lists. Your goal is to reformat this text into a more visually appealing and well-structured format by adding space characters and line breaks where necessary.
    Input Text:"{text}"
    Formatted Text:
        """
#     prompt = """format the following text into good-structured text like adding line break before lists (numbered lists or bullet lists or list like (i) (ii) ). no answer and explanation required, no note required. don't miss any words.
# Input Text:"{text}"
# Formatted Text:
#     """
#     prompt = """structure and format the following text by adding line break before lists (numbered lists or bullet lists or list like (i) (ii) ). no answer and explanation required, no note required. don't miss any words.
# Input Text:"{text}"
# Formatted Text:
#     """
#     prompt = """There is a following plain input text that contains a mixture of numbered lists and bullet lists.
# Your goal is to reformat this text into a more visually appealing and well-structured format by adding space characters and line breaks where necessary.
#
# Input Text:"{text}"
# Formatted Text:
#     """
#     prompt = """
# please format the following plain text with below instructions.
# 1. Carefully examine the following text to identify numbered lists and bullet lists.
# 2. Insert a space character before each list item.
# 3. Add a line break after each list item to create clear separation.
# 4. Ensure consistent formatting throughout the document.
# 5. Pay attention to the original order and hierarchy of the lists.
#
# Input Text:"{text}"
# Formatted Text:
#     """
#     prompt = """[INST]There is a following plain text document that contains a mixture of numbered lists and bullet lists.
# Your goal is to reformat this text into a more visually appealing and well-structured format by adding space characters and line breaks where necessary.
#
# Below are the instructions for reformatting:
#
# Carefully examine the following text to identify numbered lists and bullet lists.
# Insert a space character before each list item.
# Add a line break after each list item to create clear separation.
# Ensure consistent formatting throughout the document.
# Pay attention to the original order and hierarchy of the lists.
#
# input:"{text}"
# output:[/INST]
#     """

#     prompt = """
# please add space characters or line break to format the following text.
# Input Text: "(I) RESPIRATORY SYNCYTIAL VIRUS (RSV) AND (II) AT LEAST ONE OF HUMAN METAPNEUMOVIRUS (HMPV) OR HUMAN PARAINFLUENZA VIRUS 3,"
# Formatted Text: "(I) RESPIRATORY SYNCYTIAL VIRUS (RSV) AND
# (II) AT LEAST ONE OF HUMAN METAPNEUMOVIRUS (HMPV) OR HUMAN PARAINFLUENZA VIRUS 3,"
# Input Text:"{text}"
# Formatted Text:
# """

#     prompt = """
# format the following text which has numbered lists, bulleted lists and alphabetical lists.
# Input Text: "Format text includes below points (A) Format it into sentence case, (B) Correct spelling error."
# Formatted Text: "Format text includes below points
# (A) Format it into sentence case.
# (B) Correct spelling error."
# Input Text:"{text}"
# Formatted Text:
# """
#     prompt = """
# format the following text into multiple paragraphs.The following text includes numbered lists, bulleted lists and alphabetical lists.  don't miss any words
# Input Text:"{text}"
# Formatted Text:

    prompt = prompt.format(text=input_text)
    print(prompt)
    return prompt