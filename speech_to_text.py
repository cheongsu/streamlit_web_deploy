# import os
# import numpy as np
# import streamlit as st
# from io import BytesIO
# import streamlit.components.v1 as components
# import speech_recognition as sr
# from st_custom_components import st_audiorec

# wav_audio_data = st_audiorec()

# if wav_audio_data is not None:
#     # display audio data as received on the backend
#     st.audio(wav_audio_data, format='audio/wav')
    


# r = sr.Recognizer()
# with sr.AudioFile(wav_audio_data) as source:
#     audio = r.record(source)  # 전체 audio file 읽기

# # 구글 웹 음성 API로 인식하기 (하루에 제한 50회)
# try:
#     print("Google Speech Recognition thinks you said : " + r.recognize_google(audio, language='ko'))
# except sr.UnknownValueError:
#     print("Google Speech Recognition could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Google Speech Recognition service; {0}".format(e))



import os
import numpy as np
import streamlit as st
from io import BytesIO
import streamlit.components.v1 as components
from st_custom_components import st_audiorec
wav_audio_data = st_audiorec()
import speech_recognition as sr
import scipy.io.wavfile as wavf




out_f = 'output.wav'
wavf.write(out_f, sr, wav_audio_data)
r = sr.Recognizer()
with sr.AudioFile(out_f) as source:
    audio = r.record(source)  # 전체 audio file 읽기

input_text = r.recognize_google(audio, language='ko')
print(input_text)
# r = sr.Recognizer()
# with sr.AudioFile(wav_audio_data) as source:
#     audio = r.record(source)  # 전체 audio file 읽기

# # 구글 웹 음성 API로 인식하기 (하루에 제한 50회)
# try:
#     print("Google Speech Recognition thinks you said : " + r.recognize_google(audio, language='ko'))
# except sr.UnknownValueError:
#     print("Google Speech Recognition could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Google Speech Recognition service; {0}".format(e))

    