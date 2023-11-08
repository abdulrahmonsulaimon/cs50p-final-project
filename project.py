import tkinter as tk
from halo import Halo
from tqdm import tqdm
import time


spinner = Halo(text="Recording...", spinner="dots")

def show_spinner():
    spinner.start()
    
def hide_spinner():
    spinner.stop()
  
  
    
def record():
    record_button.pack_forget()
    stop_record_button.pack()
    show_spinner()
    
    
def stop_record():
    stop_record_button.pack_forget()
    record_button.pack()
    hide_spinner()

    for _ in tqdm(range(1), desc="Saving...", ncols=75):
        time.sleep(0.1) # replace
    print("\nSaved!")
    

def btn_hover(e):
    ...


def main():
    window = tk.Tk()
    window.title("AudiSpeech")
    window.geometry("500x500")
    window.configure(bg="lightblue")

    label = tk.Label(
        window, text="Click to record", font=("Helvetica", 20, "bold"), bg="lightblue"
    )
    label.pack(pady=10)
    
    global record_button, stop_record_button

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


    stop_record_button.pack_forget()
    record_button.pack(pady=10)
    
    # stop_record_button.bind("<Enter>", btn_hover)
    # record_button.bind("<Enter>", btn_hover)


    window.mainloop()


if __name__ == "__main__":
    main()
