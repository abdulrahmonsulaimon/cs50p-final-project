import tkinter as tk
from halo import Halo
from os import path
import wave
import sys
import pyaudio
import threading
import speech_recognition as sr
import pyttsx3
from fpdf import FPDF

stopped = False


class StopError(Exception):
    def __init__(self, message="Stopped!"):
        self.message = message
        super().__init__(self.message)


def wav_to_txt(wav_path=None):
    if wav_path == None:
        audio_file = path.join(path.dirname(path.realpath(__file__)), "output.wav")

    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)

    try:
        text = r.recognize_google(audio)
        with open("output.txt", "w") as file:
            file.write(text)

    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError as e:
        print(f"Request Error!: {e}")


def txt_to_pdf(input_file, output_pdf="output.pdf"):
    pdf = FPDF(format='A4')
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    with open(input_file, 'r') as text_file:
        lines = text_file.readlines()

    for line in lines:
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(output_pdf)

    print(f'Text file "{input_file}" has been converted to PDF: "{output_pdf}"!')

def read_txt(text=None, txt_path="output.txt"):
    with open(txt_path, "r") as file:
        text = file.readlines()

    for line in text:
        print(line)
        engine = pyttsx3.init()
        engine.say(line)
        engine.runAndWait()


# ++ spinner ++
spinner = Halo(text="Recording...", spinner="dots")


def show_spinner():
    spinner.start()


def hide_spinner():
    spinner.stop()


# ++ spinner ++


# === voice recording ===
def start_voice_recording(output_wav_file="output.wav", RECORD_SECONDS=360):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1 if sys.platform == "darwin" else 2
    RATE = 44100

    with wave.open(output_wav_file, "wb") as wf:
        p = pyaudio.PyAudio()
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

        try:
            for _ in range(0, res := int(RATE / CHUNK * RECORD_SECONDS)):
                if not stopped:
                    wf.writeframes(stream.read(CHUNK))
                else:
                    raise StopError()
        except StopError:
            ...

        stream.stop_stream()
        stream.close()
        p.terminate()
        wav_to_txt()
        file, _ = path.splitext(output_wav_file)
        txt_to_pdf(f"{file}.txt")


# === voice recording ===


def record():
    global stopped
    stopped = False
    show_spinner()
    threading.Thread(target=start_voice_recording).start()


def stop_record():
    global stopped
    stopped = True
    hide_spinner()
    print("Done!")


# <=== UI ===>
def main():
    window = tk.Tk()
    window.title("AudiSpeech")
    window.geometry("500x500")
    window.configure(bg="lightblue")

    label = tk.Label(
        window, text="Click to record", font=("Helvetica", 20, "bold"), bg="lightblue"
    )
    label.pack(pady=10)

    record_button = tk.Button(
        window,
        text="RECORD",
        bg="Green",
        fg="white",
        activebackground="#009e00",
        padx=100,
        pady=20,
        font=("Helvetica", 25, "bold"),
        command=record,
    )

    stop_record_button = tk.Button(
        window,
        text="Stop Recording...",
        bg="Red",
        fg="white",
        activebackground="#ff2e2e",
        padx=20,
        pady=15,
        font=("Helvetica", 18, "bold"),
        command=stop_record,
    )

    read_txt_button = tk.Button(
        window,
        text="Read Text...",
        bg="grey",
        fg="white",
        activebackground="grey",
        padx=20,
        pady=15,
        font=("Helvetica", 18, "bold"),
        command=read_txt,
    )
    record_button.pack(pady=10)
    stop_record_button.pack(pady=10)
    read_txt_button.pack(pady=10)

    window.mainloop()


# <=== UI ===>


if __name__ == "__main__":
    main()
