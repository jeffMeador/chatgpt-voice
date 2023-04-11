# chatgpt-voice

# Environment Setup

## Prerequisites

1. You have an OpenAI account to access the API
1. You have an Azure account. You've created a speech resource created in the Azure Portal.

## Install Requirements

```
pip install -r requirements.txt
```

## Setup Private Keys

API keys are stored in environment variables rather than in the code.  
  
Get the OpenAI API Key from https://platform.openai.com/account/api-keys  
Get the Speech Key from https://portal.azure.com  
Get the Speech Regio from https://portal.azure.com  

### Windows

```
setx SPEECH_KEY your-key
setx SPEECH_REGION your-region
setx OPENAI_API_KEY your-openai-key
```

### Linux/macOS

```
export SPEECH_KEY=your-key 
export SPEECH_REGION=your-region 
export OPENAI_API_KEY=your-openai-key
```

# Run Application

```
python chatgpt-voice.py
```

Logic flow of application:
1. Waits for user to say 'ChatGPT' as a wakeword/keyword. This processes locally
1. Speech after 'ChatGPT' is recorded until a set amount of silence and converted to text
1. The text utterance is sent to the ChatGPT API to get a text response
1. The text response from ChatGPT is output via text-to-speech as audio

# Helpful links

https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/quickstarts/setup-platform

https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-text-to-speech

https://speech.microsoft.com/

https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/custom-keyword-basics

https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-speech-to-text

https://platform.openai.com/docs/guides/chat

https://github.com/openai/tiktoken
