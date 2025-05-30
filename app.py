from flask import Flask, render_template, request
import os
import string
import socket
import speech_recognition as sr
from googletrans import Translator
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__)
translator = Translator()

gif_lst = [
    'goodbye','machine','magic','nail cutter','nail','hello','name','safe','calculator','google','kidnap','kite','knife','krishna','ball','balance','bag','balloon',
    'all the best', 'are you sick', 'any questions', 'are you angry', 'are you busy',
    'are you hungry', 'be careful', 'can we meet tomorrow', 'clean the room',
    'did you eat lunch', 'did you finish homework', 'do you go to office',
    'do you have money', 'do you want something to drink', 'do you watch tv',
    'dont worry', 'flower is beautiful', 'good afternoon', 'good morning',
    'good question', 'good evening', 'good night', 'happy journey',
    'what do you want tea or coffee', 'what is your name', 'how many people are in your family',
    'i am a clerk', 'i am bored', 'i am fine', 'i am sorry', 'i am thinking',
    'i am tired', 'i dont understand anything', 'i go to a theatre', 'i love to shop',
    'i had to say something but i forgot', 'i have a headache', 'i like pink colour',
    'lets go for lunch', 'my mother is a housewife', 'nice to meet you',
    'please dont smoke', 'open the door', 'call me later', 'please call the ambulance',
    'give me your pen', 'please wait for sometime', 'can i help you',
    'shall we go together tomorrow', 'sign language interpreter', 'sit down',
    'stand up', 'take care', 'there was a traffic jam', 'wait I am thinking',
    'what are you doing', 'what is the problem', 'what is todays date',
    'what does your father do', 'what is your job', 'what is your age',
    'what is your mobile number', 'what is your name', 'whats up',
    'when is your interview', 'when will we go', 'where do you live',
    'where is the bathroom', 'where is the police station', 'you are wrong'
]

alphabet_lst = list(string.ascii_lowercase)

def is_connected():
    try:
        socket.create_connection(("1.1.1.1", 80), 2).close()
        return True
    except:
        return False

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    recognizer = sr.Recognizer()
    english_text = ""
    original_hindi = ""
    gif_path = None
    alphabet_paths = []

    if is_connected():
        with sr.Microphone() as source:
            recognizer.pause_threshold = 0.7
            audio = recognizer.listen(source)

            try:
                # Try English first
                spoken_text = recognizer.recognize_google(audio, language="en-IN")
                detected_lang = translator.detect(spoken_text).lang
                print("Detected language (first attempt):", detected_lang)

                if detected_lang == "en":
                    english_text = spoken_text
                    original_hindi = translator.translate(spoken_text, src="en", dest="hi").text
                else:
                    raise ValueError("Not English, fallback to Hindi recognition")
            except:
                try:
                    # Retry in Hindi mode
                    spoken_text = recognizer.recognize_google(audio, language="hi-IN")
                    detected_lang = translator.detect(spoken_text).lang
                    print("Detected language (fallback):", detected_lang)

                    if detected_lang == "hi":
                        original_hindi = spoken_text
                        english_text = translator.translate(spoken_text, src="hi", dest="en").text
                    else:
                        original_hindi = spoken_text
                        english_text = "(Could not translate properly)"
                except:
                    return render_template("index.html", english="Error recognizing.", hindi="Try again.")
    else:
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            try:
                english_text = recognizer.recognize_sphinx(audio)
                original_hindi = "(Offline mode)"
            except:
                return render_template("index.html", english="Error recognizing.", hindi="Try again.")

    cleaned_text = english_text.lower().translate(str.maketrans('', '', string.punctuation))

    if cleaned_text in gif_lst:
        gif_file = f"Indian_Speech_Language_GIFS/{cleaned_text}.gif"
        if os.path.exists(os.path.join("static", gif_file)):
            gif_path = gif_file
    else:
        for char in cleaned_text:
            if char in alphabet_lst:
                img_file = f"Alphabets/{char}.jpg"
                if os.path.exists(os.path.join("static", img_file)):
                    alphabet_paths.append(img_file)

    return render_template("index.html",
                           english=english_text,
                           hindi=original_hindi,
                           gif_path=gif_path,
                           alphabet_paths=alphabet_paths)

if __name__ == "__main__":
    app.run(debug=True)
