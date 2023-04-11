import os
import openai
import azure.cognitiveservices.speech as speechsdk
import time

speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
speech_config.speech_recognition_language="en-US"

# https://platform.openai.com/account/api-keys
openai.api_key = os.getenv("OPENAI_API_KEY")

messages = []

utterance = ""

# Speech recognition callbacks
#
# See link for more info:
# https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/b4257370e1d799f0b8b64be9bf2a34cad8b1a251/samples/python/console/speech_sample.py#L290

def stop_cb(evt):
    # Callback that signals to stop continuous recognition upon receiving an event `evt`
    print('CLOSING on {}'.format(evt))
    global get_utterance_done
    get_utterance_done = True

def recognizing_cb(evt):
    # Callback for recognizing event
    if evt.result.reason == speechsdk.ResultReason.RecognizingKeyword:
        print('RECOGNIZING KEYWORD: {}'.format(evt))
    elif evt.result.reason == speechsdk.ResultReason.RecognizingSpeech:
        print('RECOGNIZING: {}'.format(evt))

def recognized_cb(evt):
    # Callback for recognized event
    if evt.result.reason == speechsdk.ResultReason.RecognizedKeyword:
        print('RECOGNIZED KEYWORD: {}'.format(evt))
    elif evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print('RECOGNIZED: {}'.format(evt))
        global utterance
        utterance = evt.result.text
    elif evt.result.reason == speechsdk.ResultReason.NoMatch:
        print('NOMATCH: {}'.format(evt))

def get_utterance():
    # Wait to listen for the keyword and get the utterance that follows. Returns a string.

    # Load the keyword file
    model = speechsdk.KeywordRecognitionModel("ChatGPT.table")

    # The phrase your keyword recognition model triggers on.
    keyword = "ChatGPT"

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    global get_utterance_done
    get_utterance_done = False

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # Stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start keyword recognition
    speech_recognizer.start_keyword_recognition(model)
    print('Say something starting with "{}" followed by whatever you want...'.format(keyword))
    while not get_utterance_done:
        time.sleep(.5)

    speech_recognizer.stop_keyword_recognition()

    # Try to clean up the utterance since the keyword comes along with it.
    # There has to be a better way to handle this.
    global utterance
    
    utterance = utterance.removeprefix('Church PPT')
    utterance = utterance.removeprefix('Check GPT')
    utterance = utterance.removeprefix('Check TPT')
    utterance = utterance.removeprefix('Chat GPT')
    utterance = utterance.removeprefix('ChatGPT')
    
    print(utterance)
    
    return utterance

    
def get_chat_response(utterance):
    # Sends an utterance to the ChatGPT API, returns a string
    
    global messages

    # Arbitrarily limit messages to 20. Could set up a token count to limit to 4096
    del messages[20:]
    
    content = utterance
    messages.append({"role": "user", "content": content})
    
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    chat_response = completion.choices[0].message.content
    print(f'ChatGPT: {chat_response}')
    messages.append({"role": "assistant", "content": chat_response})
    return chat_response

def say_chat_response(response):
    # Sends the ChatGPT response to the TTS API, outputs audio
    
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # The language of the voice that speaks. Check speech.microsoft.com for options.
    speech_config.speech_synthesis_voice_name='en-US-JaneNeural'

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Get text from the console and synthesize to the default speaker.
    text = response

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

while True:
    # Loop forever. It will wait for the "ChatGPT" keyword each time
    
    utterance = get_utterance()
    chat_response = get_chat_response(utterance)
    say_chat_response(chat_response)
