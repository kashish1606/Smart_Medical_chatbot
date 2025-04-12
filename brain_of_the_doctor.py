#Step 1: Setup GROQ API Key
import os 
import brain_of_the_doctor
print(dir(brain_of_the_doctor))

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

#Step 2: Convert image to required format

import base64

#image_path = "C:/Users/kashish/OneDrive/Desktop/Python/acne.jpeg"
def encoded_image(image_path):
    

    image_file=open(image_path,"rb")
    return base64.b64encode(image_file.read()).decode('utf-8')


#Step 3: Setup multimodal LLM

from groq import Groq  # type: ignore

query="is there something wrong with my face?"
model= "llama-3.2-90b-vision-preview"

def analyze_image_with_query(query,model,encoded_image):
    client = Groq(api_key="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")
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query                 #Type1 is our text
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",           #type2 is we upload the image
                    },
                },
            ],
        }]
    chat_completion = client.chat.completions.create(
    messages = messages , 
    model = model
    )
    return chat_completion.choices[0].message.content

