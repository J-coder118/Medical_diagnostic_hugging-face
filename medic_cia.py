import streamlit as st
from streamlit_chat import message as st_message
# from audiorecorder import audiorecorder
# import streamlit_audiorecorder
import time
import json
import requests

import pyaudio


token_hugging_face = "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"

headers = {"Authorization": f"Bearer {token_hugging_face}"} #TOKEN HUGGING FACE
API_URL_RECOGNITION = "https://api-inference.huggingface.co/models/openai/whisper-tiny.en"
API_URL_DIAGNOSTIC = "https://api-inference.huggingface.co/models/abhirajeshbhai/symptom-2-disease-net"


def recognize_speech(audio_file):

    with open(audio_file, "rb") as f:

        data = f.read()

    time.sleep(1)

    while True:
            
        try:

            response = requests.request("POST", API_URL_RECOGNITION, headers=headers, data=data)

            output = json.loads(response.content.decode("utf-8"))

            final_output = output['text']

            break

        except KeyError:

            continue

    return final_output


def diagnostic_medic(voice_text):

    synthomps = {"inputs": voice_text}

    data = json.dumps(synthomps)

      

    time.sleep(1)

    while True:

        try:

            response = requests.request("POST", API_URL_DIAGNOSTIC, headers=headers, data=data)  

            output = json.loads(response.content.decode("utf-8"))

            final_output = output[0][0]['label']

            break

        except KeyError:

            continue

    return final_output

def record_audio(duration):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    input_device_index = 0 
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=input_device_index)

    frames = []
    st.write('Recording started...')
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    st.write('Recording finished.')

    stream.stop_stream()
    stream.close()
    p.terminate()

    return b''.join(frames)

def generate_answer(audio):



    with st.spinner("Consultation in progress..."):

        # To save audio to a file:
        wav_file = open("audio.wav", "wb")

        wav_file.write(audio.tobytes())
                
        # Voice recognition model
        
        text = recognize_speech("./audio.wav")


        #Disease Prediction Model

        diagnostic = diagnostic_medic(text)
 

        #Save conversation
        st.session_state.history.append({"message": text, "is_user": True})
        st.session_state.history.append({"message": f" Your disease would be {diagnostic}", "is_user": False})


        st.success("Medical consultation done") 

           



if __name__ == "__main__":
    

    # remove the hamburger in the upper right hand corner and the Made with Streamlit footer
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

        
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')

        
    with col2:
        st.image("./logo_.png", width = 200)

        
    with col3:
        st.write(' ')

    
    if "history" not in st.session_state:

        st.session_state.history = []

    st.title("Medical Diagnostic Assistant")

    
    #Show Input
    # audio = audiorecorder("Start recording", "Recording in progress...")

    # if len(audio) > 0:
    duration = st.slider('Recording Duration (seconds)', min_value=1, max_value=10, value=5)
    # generate_answer(audio)
    if st.button("start Recording..."):
        audio_data = record_audio(duration)
        generate_answer(audio_data)

    for i, chat in enumerate(st.session_state.history): #Show historical consultation

        st_message(**chat, key =str(i))




       
