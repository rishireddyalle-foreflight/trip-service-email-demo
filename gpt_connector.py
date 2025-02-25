import openai
import json
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
def get_chatgpt_response(prompt, isJsonFormatted):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,  
            temperature=0.1, 
            response_format =  { "type": "json_object" } if isJsonFormatted == True else { "type": "text" }
        )
        # print(response['choices'][0]['message']['content'])
        return  f"{response['choices'][0]['message']['content']}"
    
    except Exception as e:
        return f"An error occurred: {str(e)}"
