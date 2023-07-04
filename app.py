# # app.py

# # 1. git clone https://github.com/sce-tts/TTS.git
# # 1-1. TTS -> TTS -> utils구조인데, 두번째 TTS가 app.py와 같은 위치에 오도록 설정
# # 2. git clone https://github.com/sce-tts/g2pK.git


# import streamlit as st
# import pandas as pd
# import numpy as np
# from PIL import Image
# from time import sleep


# from IPython.display import HTML, Audio


# import re
# import sys
# from unicodedata import normalize
# import IPython
# from TTS.utils.synthesizer import Synthesizer

# import streamlit as st
# from bokeh.models.widgets import Button
# from bokeh.models import CustomJS
# from streamlit_bokeh_events import streamlit_bokeh_events


# import streamlit as st
# import librosa
# from pydub import AudioSegment
# import numpy as np
# import io
# import g2pk


# # 페이지 기본 설정
# st.set_page_config(
#     page_icon="🐶",
#     page_title="침착맨연KU소의 스트림릿",
#     layout="wide",
# )

# # 버튼 누르고 말하면 알아서 멈춘 뒤에 input text로 stt 반환한다.
# stt_button = Button(label="Speak", width=100)

# stt_button.js_on_event("button_click", CustomJS(code="""
#     var recognition = new webkitSpeechRecognition();
#     recognition.continuous = true;
#     recognition.interimResults = true;
 
#     recognition.onresult = function (e) {
#         var value = "";
#         for (var i = e.resultIndex; i < e.results.length; ++i) {
#             if (e.results[i].isFinal) {
#                 value += e.results[i][0].transcript;
#             }
#         }
#         if ( value != "") {
#             document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
#         }
#     }
#     recognition.start();
#     """))

# result = streamlit_bokeh_events(
#     stt_button,
#     events="GET_TEXT",
#     key="listen",
#     refresh_on_update=False,
#     override_height=75,
#     debounce_time=0)

# input_text = ''
# if result:
#     if "GET_TEXT" in result:
#         st.write(result.get("GET_TEXT"))
#         input_text = result.get("GET_TEXT") # mic의 input


# # 챗봇 들어갈 자리


# # 파일 위치 변경해야 함!
# synthesizer = Synthesizer(
#     "./glowtts-v2/model_file.pth.tar",
#     "./glowtts-v2/config.json",
#     None,
#     "./hifigan-v2/model_file.pth.tar",
#     "./hifigan-v2/config.json",
#     None,
#     None,
#     False,
# )
# symbols = synthesizer.tts_config.characters.characters

# g2p = g2pk.G2p()

# def normalize_text(text):
#     text = text.strip()

#     for c in ",;:":
#         text = text.replace(c, ".")
#     text = remove_duplicated_punctuations(text)

#     text = jamo_text(text)

#     text = g2p.idioms(text)
#     text = g2pk.english.convert_eng(text, g2p.cmu)
#     text = g2pk.utils.annotate(text, g2p.mecab)
#     text = g2pk.numerals.convert_num(text)
#     text = re.sub("/[PJEB]", "", text)

#     text = alphabet_text(text)

#     # remove unreadable characters
#     text = normalize("NFD", text)
#     text = "".join(c for c in text if c in symbols)
#     text = normalize("NFC", text)

#     text = text.strip()
#     if len(text) == 0:
#         return ""

#     # only single punctuation
#     if text in '.!?':
#         return punctuation_text(text)

#     # append punctuation if there is no punctuation at the end of the text
#     if text[-1] not in '.!?':
#         text += '.'

#     return text


# def remove_duplicated_punctuations(text):
#     text = re.sub(r"[.?!]+\?", "?", text)
#     text = re.sub(r"[.?!]+!", "!", text)
#     text = re.sub(r"[.?!]+\.", ".", text)
#     return text


# def split_text(text):
#     text = remove_duplicated_punctuations(text)

#     texts = []
#     for subtext in re.findall(r'[^.!?\n]*[.!?\n]', text):
#         texts.append(subtext.strip())

#     return texts


# def alphabet_text(text):
#     text = re.sub(r"(a|A)", "에이", text)
#     text = re.sub(r"(b|B)", "비", text)
#     text = re.sub(r"(c|C)", "씨", text)
#     text = re.sub(r"(d|D)", "디", text)
#     text = re.sub(r"(e|E)", "이", text)
#     text = re.sub(r"(f|F)", "에프", text)
#     text = re.sub(r"(g|G)", "쥐", text)
#     text = re.sub(r"(h|H)", "에이치", text)
#     text = re.sub(r"(i|I)", "아이", text)
#     text = re.sub(r"(j|J)", "제이", text)
#     text = re.sub(r"(k|K)", "케이", text)
#     text = re.sub(r"(l|L)", "엘", text)
#     text = re.sub(r"(m|M)", "엠", text)
#     text = re.sub(r"(n|N)", "엔", text)
#     text = re.sub(r"(o|O)", "오", text)
#     text = re.sub(r"(p|P)", "피", text)
#     text = re.sub(r"(q|Q)", "큐", text)
#     text = re.sub(r"(r|R)", "알", text)
#     text = re.sub(r"(s|S)", "에스", text)
#     text = re.sub(r"(t|T)", "티", text)
#     text = re.sub(r"(u|U)", "유", text)
#     text = re.sub(r"(v|V)", "브이", text)
#     text = re.sub(r"(w|W)", "더블유", text)
#     text = re.sub(r"(x|X)", "엑스", text)
#     text = re.sub(r"(y|Y)", "와이", text)
#     text = re.sub(r"(z|Z)", "지", text)

#     return text


# def punctuation_text(text):
#     # 문장부호
#     text = re.sub(r"!", "느낌표", text)
#     text = re.sub(r"\?", "물음표", text)
#     text = re.sub(r"\.", "마침표", text)

#     return text


# def jamo_text(text):
#     # 기본 자모음
#     text = re.sub(r"ㄱ", "기역", text)
#     text = re.sub(r"ㄴ", "니은", text)
#     text = re.sub(r"ㄷ", "디귿", text)
#     text = re.sub(r"ㄹ", "리을", text)
#     text = re.sub(r"ㅁ", "미음", text)
#     text = re.sub(r"ㅂ", "비읍", text)
#     text = re.sub(r"ㅅ", "시옷", text)
#     text = re.sub(r"ㅇ", "이응", text)
#     text = re.sub(r"ㅈ", "지읒", text)
#     text = re.sub(r"ㅊ", "치읓", text)
#     text = re.sub(r"ㅋ", "키읔", text)
#     text = re.sub(r"ㅌ", "티읕", text)
#     text = re.sub(r"ㅍ", "피읖", text)
#     text = re.sub(r"ㅎ", "히읗", text)
#     text = re.sub(r"ㄲ", "쌍기역", text)
#     text = re.sub(r"ㄸ", "쌍디귿", text)
#     text = re.sub(r"ㅃ", "쌍비읍", text)
#     text = re.sub(r"ㅆ", "쌍시옷", text)
#     text = re.sub(r"ㅉ", "쌍지읒", text)
#     text = re.sub(r"ㄳ", "기역시옷", text)
#     text = re.sub(r"ㄵ", "니은지읒", text)
#     text = re.sub(r"ㄶ", "니은히읗", text)
#     text = re.sub(r"ㄺ", "리을기역", text)
#     text = re.sub(r"ㄻ", "리을미음", text)
#     text = re.sub(r"ㄼ", "리을비읍", text)
#     text = re.sub(r"ㄽ", "리을시옷", text)
#     text = re.sub(r"ㄾ", "리을티읕", text)
#     text = re.sub(r"ㄿ", "리을피읍", text)
#     text = re.sub(r"ㅀ", "리을히읗", text)
#     text = re.sub(r"ㅄ", "비읍시옷", text)
#     text = re.sub(r"ㅏ", "아", text)
#     text = re.sub(r"ㅑ", "야", text)
#     text = re.sub(r"ㅓ", "어", text)
#     text = re.sub(r"ㅕ", "여", text)
#     text = re.sub(r"ㅗ", "오", text)
#     text = re.sub(r"ㅛ", "요", text)
#     text = re.sub(r"ㅜ", "우", text)
#     text = re.sub(r"ㅠ", "유", text)
#     text = re.sub(r"ㅡ", "으", text)
#     text = re.sub(r"ㅣ", "이", text)
#     text = re.sub(r"ㅐ", "애", text)
#     text = re.sub(r"ㅒ", "얘", text)
#     text = re.sub(r"ㅔ", "에", text)
#     text = re.sub(r"ㅖ", "예", text)
#     text = re.sub(r"ㅘ", "와", text)
#     text = re.sub(r"ㅙ", "왜", text)
#     text = re.sub(r"ㅚ", "외", text)
#     text = re.sub(r"ㅝ", "워", text)
#     text = re.sub(r"ㅞ", "웨", text)
#     text = re.sub(r"ㅟ", "위", text)
#     text = re.sub(r"ㅢ", "의", text)

#     return text

# def normalize_multiline_text(long_text):
#     texts = split_text(long_text)
#     normalized_texts = [normalize_text(text).strip() for text in texts]
#     return [text for text in normalized_texts if len(text) > 0]

# def synthesize(text):
#     wavs = synthesizer.tts(text, None, None)
#     return wavs

# # def wav_to_bytes(wav_array, sample_rate=22050):
# #     audio_segment = AudioSegment(
# #         wav_array.tobytes(),
# #         frame_rate=sample_rate,
# #         sample_width=wav_array.dtype.itemsize, 
# #         channels=1
# #     )
# #     byte_io = io.BytesIO()
# #     audio_segment.export(byte_io, format="wav")
# #     byte_wav = byte_io.getvalue()
# #     byte_io.close()
# #     return byte_wav

# # for text in normalize_multiline_text(input_text):
# #     wav = synthesizer.tts(text, None, None)

# #     #IPython.display.display(IPython.display.Audio(wav, rate=22050))
# #     st.audio(wav, format="audio/wav",sample_rate =22050 )
#     # 버전 문제 발생
#     # st.audio만 확인해보면 될듯. wav에 nuarray형태가 들어가야 함.

# # text를 통해 wav가 생성됐을 때 wav를 출력할 수 있는 streamlit 함수만 넣으면 됨.

# from io import BytesIO
# from scipy.io.wavfile import write

# sample_text = "안녕하세요"

# for text in normalize_multiline_text(sample_text):
#     wav = synthesizer.tts(text, None, None)
#     type(wav)
#     IPython.display.display(IPython.display.Audio(wav, rate=22050))
#     wav_norm = np.int16(wav/np.max(np.abs(wav)) * 32767)
#     virtual_file = BytesIO()
#     write(virtual_file, 22050, wav_norm)
#     virtual_file.seek(0)
#     st.audio(virtual_file.read(), format = 'audio/wav')

# # 문제점 - mic - input_text가 안됨. 

# import streamlit as st
# from bokeh.models.widgets import Button
# from bokeh.models import CustomJS

# text = st.text_input("Say what ?")

# tts_button = Button(label="Speak", width=100)

# tts_button.js_on_event("button_click", CustomJS(code=f"""
#     var u = new SpeechSynthesisUtterance();
#     u.text = "{text}";
#     u.lang = 'en-US';

#     speechSynthesis.speak(u);
#     """))
# st.bokeh_chart(tts_button)

# app.py

# import streamlit as st
# import pandas as pd
# import numpy as np
# from PIL import Image
# from time import sleep


# # 페이지 기본 설정
# st.set_page_config(
#     page_icon="🐶",
#     page_title="빅공잼의 스트림릿 배포하기",
#     layout="wide",
# )

# # 로딩바 구현하기
# with st.spinner(text="페이지 로딩중..."):
#     sleep(2)

# # 페이지 헤더, 서브헤더 제목 설정
# st.header("빅공잼 페이지에 오신걸 환영합니다👋")
# st.subheader("스트림릿 기능 맛보기")

# # 페이지 컬럼 분할(예: 부트스트랩 컬럼, 그리드)
# cols = st.columns((1, 1, 2))
# cols[0].metric("10/11", "15 °C", "2")
# cols[0].metric("10/12", "17 °C", "2 °F")
# cols[0].metric("10/13", "15 °C", "2")
# cols[1].metric("10/14", "17 °C", "2 °F")
# cols[1].metric("10/15", "14 °C", "-3 °F")
# cols[1].metric("10/16", "13 °C", "-1 °F")

# # 라인 그래프 데이터 생성(with. Pandas)
# chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=['a', 'b', 'c'])

# # 컬럼 나머지 부분에 라인차트 생성
# cols[2].line_chart(chart_data)


import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

stt_button = Button(label="Speak", width=100)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
