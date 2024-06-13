import util.logging_utils as logging_utils

logger = logging_utils.setup_logger('draft_email_generating_prompt')

order_chatbot_prompt = """
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
You are OrderBot, an automated service to collect orders for a pizza restaurant.
You first greet the customer, then collects the order,
and then asks if it's a pickup or delivery. 
You wait to collect the entire order, then summarize it and ctime if the customer wants to add anything else.
If it's a delivery, you ask for an address.
Finally you collect the payment. it supports credit card, alipay.
Make sure to clarify all options, extras and sizes to uniquely identify the item from the menu. 
You respond in a short, very conversational friendly style.
The menu includes 
pepperoni pizza 12.95, 10.00，7.00
cheese pizza 10.95，9.25，6.50
eggplant pizza 11.95，9.75，6.75
fries 4.50，3.50
greek salad 7.25

Toppings:
extra cheese 2.00，
mushrooms 1.50
sausage 3.00
canadian bacon 3.50
AI sauce 1.50
peppers 1.00

Drinks:
coke 3.00，2.00，1.00
sprite 3.00，2.00，1.00 
bottled water 5.00
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""


def get_order_food_prompt(previous_prompt, conversations,  user_query = ''):
    try:
        global order_chatbot_prompt

        conversation_prompt = ""
        if user_query and conversations:
            for message in conversations:
                message_type=  message['type']
                message_content = message['text']
                if message_type == 'bot':
                    conversation_prompt = conversation_prompt + f"""{message_content}<|eot_id|><|start_header_id|>user<|end_header_id|>"""
                if message_type == 'user':
                    conversation_prompt = conversation_prompt + f"""{message_content}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""


            order_chatbot_prompt = order_chatbot_prompt+ conversation_prompt
            logger.info(order_chatbot_prompt)
            return order_chatbot_prompt.strip()
    except Exception as e:
        logger.exception(e)
        return None

    return None