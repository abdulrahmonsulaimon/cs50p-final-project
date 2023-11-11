import tkinter as tk
from halo import Halo
import time
import wave
import sys
import pyaudio
import threading

stopped = False
class StopError(Exception):
    def __init__(self, message="Stopped!"):
        self.message = message
        super().__init__(self.message)

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
    CHANNELS = 1 if sys.platform == 'darwin' else 2
    RATE = 44100

    with wave.open(output_wav_file, 'wb') as wf:
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
    sys.exit("Done!")

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
        command=record
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
        command=stop_record
    )

    record_button.pack(pady=10)
    stop_record_button.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    main()
