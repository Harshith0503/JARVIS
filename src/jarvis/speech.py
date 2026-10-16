import pyttsx3
import speech_recognition as sr


class SpeechService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self._speaker = None

    def listen_once(self) -> str:
        with sr.Microphone() as microphone:
            self.recognizer.adjust_for_ambient_noise(
                microphone,
                duration=0.4
            )
            audio = self.recognizer.listen(
                microphone,
                timeout=5,
                phrase_time_limit=8
            )
        return self.recognizer.recognize_google(
            audio,
            language="en-IN"
        )

    def speak(self, text: str) -> None:
        if self._speaker is None:
            self._speaker = pyttsx3.init()
        self._speaker.stop()
        self._speaker.say(text)
        self._speaker.runAndWait()