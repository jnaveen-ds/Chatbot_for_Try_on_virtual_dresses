import os


import openai
from dotenv import load_dotenv
load_dotenv()


client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

model_id = 'gpt-3.5-turbo'#'gpt-4'

def ChatGPT_conversation(conversation):
    
    system_list = [item for item in conversation if item['role'] == 'system']
    
    # response = openai.ChatCompletion.create(
    response=client.chat.completions.create(
        model=model_id,
        messages=system_list,
        temperature=0
        
    )
    print("Before :",system_list)
    system_list.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    print("After :",system_list)
    return system_list
