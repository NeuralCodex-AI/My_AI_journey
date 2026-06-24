import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS


st.title("Traslation App")

google_translate_dict = {
    "urdu": "ur",
    "english": "en",
    "arabic": "ar",
    "Chinese": "zh-CN",
    "german": "de",
    "spanish": "es",
    "french": "fr",
    "hindi": "hi",
    "bengali": "bn",
    "punjabi": "pa",
    "sindhi": "sd",
    "japanese": "ja",
    "korean": "ko",
    "russian": "ru",
    "italian": "it",
    "turkish": "tr",
    "persian": "fa",
    "pashto": "ps",
    "dutch": "nl",
    "portuguese": "pt"
}
Selected_Language= st.selectbox(
        "source_Lang",
        list(google_translate_dict.keys())
    )
Target_lang=st.selectbox(
        "Target_lang",
        list(google_translate_dict.keys())
    )
source_code = google_translate_dict[Selected_Language]
target_code = google_translate_dict[Target_lang]


text=st.text_input("enter the text to translate")
if st.button("Translation&Speak"):
    if text.strip():
        translated=GoogleTranslator(
            source=source_code,
            target=target_code  
        ).translate(text)
        st.success(f"Text_Translated:{translated} ")

        tts=gTTS(
            text=translated,
            lang=target_code
        )
        filename="translates_audio.mp3"
        tts.save(filename)
        st.audio(filename, format="audio/mp3")
    else:
        st.warning("please enter some text first")



