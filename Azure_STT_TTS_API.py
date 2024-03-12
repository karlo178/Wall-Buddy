import azure.cognitiveservices.speech as speechsdk

def text_to_speech(text, language='en-US'):
    
    speech_key = "0ba13fe28d6442238eeeb2d445521770"
    service_region = "northeurope"

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Set the desired voice and language
    speech_config.speech_synthesis_voice_name = language

    result = speech_synthesizer.speak_text_async(text).get()
    
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesis successful.")
    else:
        print(f"Speech synthesis failed: {result.reason}")

def speech_to_text():
    
    speech_key = "0ba13fe28d6442238eeeb2d445521770"
    service_region = "northeurope"

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    result = speech_recognizer.recognize_once()
    print(result.text)
    return result.text

# if __name__ == "__main__":
#     input_text = input("Enter the text you want to convert to speech: ")
#     text_to_speech(input_text)

#     spoken_text = speech_to_text()
#     print("Spoken text:", spoken_text)
#     print(type(spoken_text))
