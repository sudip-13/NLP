import re

def extract_session_id(session_str:str):

    match = re.search(r'sessions/(.*?)/contexts', session_str)
    if match:
        extracted_text = match.group(1)
        print(extracted_text)
        return extracted_text
    else:
        return ""


def get_str_from_food_dict(food_dict:dict):
    return ", ".join([f"{int(value)} {key}"for key,value in food_dict.items()])