from gtts import gTTS

class SpeechAgent:
    def text_to_speech(self, text, language, output_file="output.mp3"):
        tts = gTTS(text=text, lang=language)
        tts.save(output_file)
        print(f"Audio saved as {output_file}")
        return output_file