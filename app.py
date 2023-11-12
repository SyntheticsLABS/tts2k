# Crie um arquivo chamado app.py e adicione o seguinte código:

# app.py
import streamlit as st
from elevenlabs import generate
import string
import io
from pydub import AudioSegment
import simpleaudio

def split_sentence(sentence, max_length):
    sentences = []
    current_chunk = ""

    for char in sentence:
        current_chunk += char
        if len(current_chunk) >= max_length and char in string.punctuation:
            sentences.append(current_chunk.strip())
            current_chunk = ""

    if current_chunk:
        sentences.append(current_chunk.strip())

    if len(sentences[-1]) < max_length and len(sentence) > max_length:
        remaining_chunk = sentence[len(sentences[-1]):]
        for char in remaining_chunk:
            current_chunk += char
            if len(current_chunk) >= max_length and char in string.punctuation:
                sentences.append(current_chunk.strip())
                current_chunk = ""

    return sentences

def generate_audio(sentence, max_length):
    sentence = sentence[:2000]
    sentences = split_sentence(sentence, max_length)

    audios = []
    for sentence_part in sentences:
        # Substitua esta parte pelo seu código real para gerar áudio
        audio = generate(text=sentence_part, voice="Callum", model='eleven_multilingual_v1')
        audio_data = io.BytesIO(audio)
        audio_segment = AudioSegment.from_mp3(audio_data)
        audios.append(audio_segment)

    combined_audio = AudioSegment.empty()
    for audio_segment in audios:
        combined_audio += audio_segment

    # Converte para bytes e reproduz usando simpleaudio
    audio_bytes = combined_audio.export(format='wav').read()
    wave_obj = simpleaudio.WaveObject.from_buffer(audio_bytes, num_channels=combined_audio.channels, sample_width=combined_audio.sample_width, sample_rate=combined_audio.frame_rate)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def main():
    st.title("Gerador de Áudio")

    sentence = st.text_area("Digite sua sentença (máximo de 2000 caracteres):")
    max_length = st.slider("Selecione o comprimento máximo de cada parte", 230, 245, value=230)

    if st.button("Gerar Áudio"):
        generate_audio(sentence, max_length)

if __name__ == "__main__":
    main()
