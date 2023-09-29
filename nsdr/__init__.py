from chat import get_chat, build_chat_prompt
import os
from flask import Flask, send_file
import datetime
import requests

app = Flask(__name__)

# Routes
@app.route('/')
# A simple page that says hello
def hello():
    return 'Hello, World!'

@app.route('/generate_nsdr', methods=['POST'])
def generate_nsdr():
    script = generate_script()
    audio_file_path = generate_audio_with_eleven(script)
    print(f"Audio file path: {audio_file_path}")
    return '', 200
    # return send_file(audio_file_path, as_attachment=True, mimetype='audio/mp3', download_name='audio.mp3')

def generate_script():
    prompt = "Generate an NSDR (non sleep deep relaxation) script"
    prompt_with_params = build_chat_prompt(prompt)
    chat = get_chat()
    results = chat(prompt_with_params)
    script = results.content

    return script

def get_audio_file_path():
    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
    audio_file_name = f"nsdr_{current_timestamp}.mp3"
    audio_folder = "audio_files"

    # Create the audio_files folder if it doesn't exist
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)

    audio_file_path = os.path.join(audio_folder, audio_file_name)
    return audio_file_path

def generate_audio_with_eleven(text):
    audio_file_path = get_audio_file_path()

    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/LcfcDJNUP1GQjkzn1xUU" # Voice ID for Emily

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.environ["ELEVEN_LABS_API_KEY"]
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)
    with open(audio_file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    return audio_file_path
    # Good options:
    # 'en-US-AshleyNeural'
    # "en-US-SaraNeural"
    speaker_langauge_with_accent = "en-US"
    speaker = "AshleyNeural"
    semicolan_silance = "500ms"
    speech_rate = "-10.00%"
    return f"""
        <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
            <voice name="Microsoft Server Speech Text to Speech Voice ({speaker_langauge_with_accent}, {speaker})" semicolonsilence-exact="{semicolan_silance}">
                <prosody rate="{speech_rate}">
                    {script}
                </prosody>
            </voice>
        </speak>
    """
