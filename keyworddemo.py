import os
import azure.cognitiveservices.speech as speechsdk

import time

speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))

# Creates an instance of a keyword recognition model. Update this to
# point to the location of your keyword recognition model.
model = speechsdk.KeywordRecognitionModel("ChatGPT.table")

# The phrase your keyword recognition model triggers on.
keyword = "ChatGPT"

speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

utterance = ""
done = False

def stop_cb(evt):
    """callback that signals to stop continuous recognition upon receiving an event `evt`"""
    print('CLOSING on {}'.format(evt))
    global done
    done = True

def recognizing_cb(evt):
    """callback for recognizing event"""
    if evt.result.reason == speechsdk.ResultReason.RecognizingKeyword:
        print('RECOGNIZING KEYWORD: {}'.format(evt))
    elif evt.result.reason == speechsdk.ResultReason.RecognizingSpeech:
        print('RECOGNIZING: {}'.format(evt))

def recognized_cb(evt):
    """callback for recognized event"""
    if evt.result.reason == speechsdk.ResultReason.RecognizedKeyword:
        print('RECOGNIZED KEYWORD: {}'.format(evt))
    elif evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print('RECOGNIZED: {}'.format(evt))
        global utterance
        utterance = evt.result.text
    elif evt.result.reason == speechsdk.ResultReason.NoMatch:
        print('NOMATCH: {}'.format(evt))

# Connect callbacks to the events fired by the speech recognizer
speech_recognizer.recognizing.connect(recognizing_cb)
speech_recognizer.recognized.connect(recognized_cb)
speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
# stop continuous recognition on either session stopped or canceled events
speech_recognizer.session_stopped.connect(stop_cb)
speech_recognizer.canceled.connect(stop_cb)

# Start keyword recognition
speech_recognizer.start_keyword_recognition(model)
print('Say something starting with "{}" followed by whatever you want...'.format(keyword))
while not done:
    time.sleep(.5)

speech_recognizer.stop_keyword_recognition()

print(utterance)
