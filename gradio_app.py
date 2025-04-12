#VoiceBot UI with Gradio
import os
print(os.getcwd()) 
os.environ["ELEVENLABS_API_KEY"] = "sk_4288560eb40da278acdcbef1db91a3fe7e40154ae3e1acf3"

os.environ["GROQ_API_KEY"] = "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"


import sys
sys.path.append(r'C:\Users\kashish\OneDrive\Desktop\Python')
import os
import gradio as gr

from brain_of_the_doctor import analyze_image_with_query,encoded_image

from voice_of_the_patient import record_audio, transcribe_with_groq

from voice_of_the_doctor import text_to_speech_with_gtts,text_to_speech_with_elevenlabs

system_prompt="""You have to act as an Professional doctor, I Know you are not but this is for a learning purpose What's in this image?. Do you find anything wrong with it medically?
                If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
                your response, your response should be in one long paragraph, also always as if you are aswering to a real person.
                donot say 'In the image I see' but say 'With what I see, I think you have......'
                Donot respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot,
                Keep your answer concise(max 2 sentences). No preamble, start your answer right away please"""

# def process_inputs(audio_filepath,image_filepath):
#     print("Processing inputs...")
#     speech_to_text_output = transcribe_with_groq(GROQ_API_KEY= os.environ.get("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"),
#                                                  audio_filepath=audio_filepath,
#                                                  stt_model= "whisper-large-v3")

def process_inputs(audio_filepath, image_filepath):
    print("Processing inputs...")  # Debugging line
    speech_to_text_output = transcribe_with_groq(
        GROQ_API_KEY=os.environ.get("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"),
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
    )
    print("Speech to text result:", speech_to_text_output)

    #Handle the image input
    if image_filepath:
        doctor_response = analyze_image_with_query(query=system_prompt+speech_to_text_output, model="llama-3.2-11b-vision-preview",encoded_image= encoded_image(image_filepath))
    else:
        doctor_response="No image provided for me to analyze"

    voice_of_doctor = text_to_speech_with_elevenlabs(input_text=doctor_response,output_filepath="final.mp3") #Replace with actual path if different
    
    return speech_to_text_output, doctor_response, voice_of_doctor
    

'''
#create the interface
iface = gr.Interface(
    fn= process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"],type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's response"),
        gr.Audio("Temp.mp3")
    ],
    title="AI Doctor with vision and voice"
    #description= "Upload an image and interact via voice input and audio response."
)

iface.launch(debug=True)'''

print(" Starting the app...")  # Debugging start

iface = gr.Interface(
    fn= process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's response"),
        gr.Audio("Temp.mp3")
    ],
    title="AI Doctor with vision and voice"
)

print("✅ Gradio Interface created!")  # Debugging checkpoint

iface.launch(debug=True)

print("✅ Gradio launched!")  # Final confirmation
