from chat import get_chat, build_chat_prompt
import os
import argparse
from flask import Flask, send_file
import azure.cognitiveservices.speech as speechsdk
import datetime

speech_key = os.environ["SPEECH_KEY"]
speech_region = os.environ["SPEECH_REGION"]


app = Flask(__name__)

# Routes
@app.route('/')
# A simple page that says hello
def hello():
    return 'Hello, World!'

@app.route('/generate_nsdr', methods=['POST'])
def generate_nsdr():
    script = generate_script()
    audio_file_path = generate_audio(script)
    return send_file(audio_file_path, as_attachment=True, mimetype='audio/mp3', download_name='audio.mp3')

def generate_script():
    prompt = "Generate a 5 min NSDR (non sleep deep relaxation) script"
    prompt_with_params = build_chat_prompt(prompt)
    chat = get_chat()
    results = chat(prompt_with_params)
    script = results.content

    return script

def generate_audio(text):
    text_with_params = build_script_with_params(text)
    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
    audio_file_name = f"nsdr_{current_timestamp}.mp3"
    audio_folder = "audio_files"

    # Create the audio_files folder if it doesn't exist
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)

    audio_file_path = os.path.join(audio_folder, audio_file_name)
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_file_path)

    speech_config.speech_synthesis_output_format = "Audio48Khz192KBitRateMonoMp3"
    
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml=text_with_params).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

    return audio_file_path

def build_script_with_params(script):
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate NSDR script and download audio file')
    parser.add_argument('--download', action='store_true', help='Download the audio file')

    args = parser.parse_args()

    if args.download:
        with app.test_client() as client:
            response = client.post('/generate_script')
            if response.status_code == 200:
                with open('audio.wav', 'wb') as f:
                    f.write(response.data)
                print('Audio file downloaded successfully.')
            else:
                print('Error occurred while generating the script.')
    else:
        # Save the audio file without playing it
        audio_file_path = generate_audio("Generate a 5 min NSDR (non sleep deep relaxation) script")
        print(f'Audio file saved at {audio_file_path}')


