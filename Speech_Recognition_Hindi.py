import tkinter as tk
from tkinter import ttk, Text, messagebox
from PIL import Image, ImageTk
from itertools import count
import speech_recognition as sr
from googletrans import Translator
import socket
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import string
import os
import warnings

# Listening
# GIF personlised
# Instructions
# Extra Langugage
# Correct Translation 
# 

# Suppress Unicode and font warnings
warnings.filterwarnings("ignore", category=UserWarning)

# ✅ Set a Hindi-compatible font for Matplotlib
# Try preferred fonts in order
for font in ["Mangal", "Nirmala UI", "Arial Unicode MS"]:
    if font in matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf'):
        plt.rcParams['font.family'] = font
        break

translator = Translator()

gif_lst = [
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

alphabet_lst = list("abcdefghijklmnopqrstuvwxyz")

def is_connected():
    try:
        host = socket.gethostbyname("one.one.one.one")
        socket.create_connection((host, 80), 2).close()
        return True
    except:
        return False

class ImageLabel(tk.Label):
    def load(self, img_path):
        img = Image.open(img_path)
        self.frames = []
        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(img.copy()))
                img.seek(i)
        except EOFError:
            pass
        self.delay = img.info.get('duration', 100)
        if self.frames:
            self.config(image=self.frames[0])
            self.loc = 0
            self.after(self.delay, self.next_frame)

    def next_frame(self):
        self.loc = (self.loc + 1) % len(self.frames)
        self.config(image=self.frames[self.loc])
        self.after(self.delay, self.next_frame)

def animate_display(text, full_text, container, gif_label, response_box):
    gif_label.pack_forget()
    response_box.pack_forget()

    if text in gif_lst:
        gif_path = f'Indian_Speech_Language_GIFS/{text}.gif'
        if os.path.exists(gif_path):
            gif_label.load(gif_path)
            gif_label.pack(pady=10)
        else:
            messagebox.showerror("GIF Missing", f"No GIF found for: {text}")
    else:
        for char in text:
            if char in alphabet_lst:
                img_path = f'Alphabets/{char}.jpg'
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    img_np = np.asarray(img)
                    plt.imshow(img_np)
                    plt.axis('off')
                    plt.title(full_text, fontsize=14)
                    plt.pause(0.8)
        plt.close()

    response_box.delete("1.0", tk.END)
    response_box.insert(tk.END, full_text)
    response_box.pack(pady=10)

def take_command():
    recognizer = sr.Recognizer()
    english_text = ""
    original_hindi = ""

    if is_connected():
        with sr.Microphone() as source:
            recognizer.pause_threshold = 0.7
            status_var.set("Listening (Online)...")
            root.update()
            audio = recognizer.listen(source)
            try:
                status_var.set("Recognizing...")
                original_hindi = recognizer.recognize_google(audio, language="hi-IN")
                english_text = translator.translate(original_hindi, src="hi", dest="en").text
            except Exception:
                status_var.set("Couldn't recognize, try again.")
                return
    else:
        with sr.Microphone() as source:
            status_var.set("Listening (Offline)...")
            audio = recognizer.listen(source)
            try:
                english_text = recognizer.recognize_sphinx(audio)
                original_hindi = "(Offline mode — Hindi unavailable)"
            except:
                status_var.set("Couldn't recognize, try again.")
                return

    cleaned_text = english_text.lower().translate(str.maketrans('', '', string.punctuation))
    full_display = f"Hindi: {original_hindi}\nEnglish: {english_text}"
    animate_display(cleaned_text, full_display, root, gif_label, response_box)
    status_var.set("Ready")

# 🌈 Main GUI Window
root = tk.Tk()
root.title("SignBridge")
root.configure(bg="#f3d9e0")

# 🖥 Center the window
window_width = 1000
window_height = 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# 🖼️ Banner Image
banner_img = Image.open("SignLanguage.png")
banner_img = banner_img.resize((150, 150), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(banner_img)
tk.Label(root, image=photo, bg="#f3d9e0").pack(pady=10)

# 🧠 Heading
heading = tk.Label(root,
                   text="SignBridge - Speech to Sign Language Translator",
                   font=("Arial", 18, "bold"),
                   bg="#89cff0", fg="white", padx=10, pady=10)
heading.pack(fill='x')

# 🎛️ Button Frame
btn_frame = tk.Frame(root, bg="#f3d9e0")
btn_frame.pack(pady=20)

style = ttk.Style()
style.theme_use('clam')
style.configure("TButton",
                font=("Arial", 13, "bold"),
                padding=10,
                foreground="white",
                background="#6ca966",
                borderwidth=2)
style.map("TButton",
          background=[("active", "#4d804d")],
          foreground=[("active", "white")])

speak_btn = ttk.Button(btn_frame, text="Speak 🎤", command=take_command)
speak_btn.grid(row=0, column=0, padx=20)

exit_btn = ttk.Button(btn_frame, text="Exit ❌", command=root.quit)
exit_btn.grid(row=0, column=1, padx=20)

# 📟 Status
status_var = tk.StringVar()
status_var.set("Ready")
status_lbl = tk.Label(root, textvariable=status_var, font=("Arial", 11, "italic"),
                      fg="#555555", bg="#f3d9e0")
status_lbl.pack(pady=5)

# 🎞️ Image/GIF label
gif_label = ImageLabel(root, bg="#f3d9e0")

# 📝 Text box for translated speech (supports Hindi)
response_box = Text(root, height=5, font=("Mangal", 13), wrap=tk.WORD,
                    bg="#fffccf", bd=3, relief=tk.GROOVE, fg="#333333")

# 🚀 Start the app
root.mainloop()
