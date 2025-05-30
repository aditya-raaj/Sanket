# SignBridge: Speech-to-Sign Language Translator

SignBridge is a Flask-based web application that translates spoken English or Hindi into Indian Sign Language (ISL). It utilizes speech recognition, multilingual translation, and visual rendering via sign GIFs and alphabet-based spellout to enhance communication accessibility.

---

## 🚀 Features

* 🎤 Real-time Speech Recognition
* 🌐 Supports English and Hindi (auto-detect)
* 🔀 Automatic Translation (EN ↔ HI)
* 🎨 Indian Sign Language Rendering:

  * Prebuilt sentence GIFs
  * Alphabet image spell-out fallback
* ⚡ Fast local execution with offline mode fallback (CMU Sphinx)
* 🔊 Works with Microphone Input

---

## 📚 System Overview

1. User clicks "Begin Translation"
2. Speech is captured via microphone
3. Speech is converted to text (Google or Sphinx)
4. Language is detected
5. Translations are generated (Google Translate)
6. System matches sentence with existing GIFs or spells using alphabet images
7. Translated text and visual sign output are rendered on screen

---

## 📚 Tech Stack

* Python
* Flask
* SpeechRecognition
* googletrans
* CMU Sphinx (offline mode)
* HTML5 + JavaScript (Frontend)
* GIF/Image rendering for sign language

---

## 🚫 Known Limitations

* Exact match needed for prebuilt GIFs
* Google Speech API may return "Hinglish" instead of Devanagari
* Short words may cause inaccurate language detection
* Offline mode is limited to English and Sphinx capabilities

---

## 🛠️ Installation

```bash
pip install Flask SpeechRecognition googletrans==4.0.0-rc1 pyaudio
```

Ensure you have microphone support enabled and run:

```bash
python app.py
```

Then open: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 📂 Project Structure

```
SignBridge/
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── Indian_Speech_Language_GIFS/
│   └── Alphabets/
```

---

## 👁‍🗨 Future Enhancements

* Add fuzzy matching for GIF detection
* Expand translation to more Indian languages
* Include Text-to-Speech (TTS) playback
* Build desktop/mobile version
* Add replay and audio waveform visualization

---

## 📄 License

MIT License. Feel free to use, modify, and distribute with attribution.

---

## 💼 Author

Developed with care for inclusive communication. Contributions welcome!

