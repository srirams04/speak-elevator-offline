import time
import tkinter as tk
import threading
import pyttsx3
from vosk import Model, KaldiRecognizer
import pyaudio
import json

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set speaking speed

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize Vosk model and recognizer
model_path = r"C:\Users\srira\Downloads\vosk-model-en-in-0.5"
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# Map spelled-out numbers to their corresponding integers
number_map = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
}

def recognize_speech_from_mic():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
    stream.start_stream()
    print("Listening...")

    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = json.loads(result).get("text", "")
            if text:
                return text

def move_elevator(target_floor):
    if door_status_var.get() == "Open":
        floor_label.config(text="Please close the door first")
        speak("Please close the door first")
        return
    current_floor = current_floor_var.get()
    if current_floor == target_floor:
        speak(f"Already at Floor {target_floor}")
        floor_buttons[target_floor - 1].config(bg="white", state=tk.NORMAL)
        return
    direction = 1 if target_floor > current_floor else -1
    floors = range(current_floor, target_floor + direction, direction)
    for floor in floors:
        current_floor_var.set(floor)
        floor_label.config(text=f"Floor: {floor}")
        slider.set(floor)
        update_arrow_direction(current_floor, target_floor)
        root.update()
        time.sleep(0.8)
    close_door()
    speak(f"Arrived at Floor {target_floor}")
    floor_buttons[target_floor - 1].config(bg="white", state=tk.NORMAL)

def update_arrow_direction(current_floor, target_floor):
    if current_floor < target_floor:
        arrow_label.config(text="↑")
    elif current_floor > target_floor:
        arrow_label.config(text="↓")
    else:
        arrow_label.config(text="")
    root.update()

def open_door():
    door_status_var.set("Open")
    door_status_label.config(text="Door: Opened")

def close_door():
    door_status_var.set("Closed")
    door_status_label.config(text="Door: Closed")

def handle_floor_button(target_floor):
    if door_status_var.get() == "Open":
        floor_label.config(text="Please close the door first")
        speak("Please close the door first")
    else:
        floor_buttons[target_floor - 1].config(state=tk.DISABLED, bg="yellow")
        move_elevator(target_floor)

def handle_voice_command():
    command = recognize_speech_from_mic()
    print(f"You said: {command}")
    target_floor = 0
    try:
        for word, number in number_map.items():
            if word in command:
                target_floor = number
                break
        if target_floor > max_floors or target_floor < 1:
            floor_label.config(text="Invalid floor number")
            speak("Invalid floor number")
        elif target_floor == 0:
            speak("Unable to recognize")
        else:
            handle_floor_button(target_floor)
        if "open" in command:
            open_door()
        elif "close" in command:
            close_door()
        elif "emergency" in command:
            simulate_emergency()
        else:
            floor_label.config(text="Unable to recognize")
            speak("Unable to recognize")
    except Exception as e:
        print(e)
        speak("Unable to recognize")

def simulate_emergency():
    speak("Emergency button pressed. Elevator stopped.")
    root.destroy()

root = tk.Tk()
root.title("Voice-Activated Elevator Interface")
root.geometry("1000x600")
root.configure(bg="powder blue")

heading_label = tk.Label(root, text="Voice-Activated Elevator Interface", font=("Arial", 24, "bold"), bg="powder blue", fg="navy blue")
heading_label.pack(pady=10)

panel_frame = tk.Frame(root, bg="powder blue")
panel_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

floor_panel = tk.Frame(panel_frame, bg="light grey", padx=20, pady=20)
floor_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

floor_panel_label = tk.Label(floor_panel, text="Floor Panel", font=("Arial", 16, "bold"), bg="light grey", fg="navy blue")
floor_panel_label.pack(pady=10)

floor_button_frame = tk.Frame(floor_panel, bg="light grey")
floor_button_frame.pack(pady=10)

max_floors = 9
floor_buttons = []
for floor in range(1, max_floors + 1):
    button = tk.Button(floor_button_frame, text=f"Floor {floor}", command=lambda f=floor: handle_floor_button(f), font=("Arial", 12), bg="white", fg="coral", padx=20, pady=20, activebackground="coral", activeforeground="white")
    button.grid(row=(floor-1)//3, column=(floor-1)%3, padx=5, pady=5)
    floor_buttons.append(button)

additional_button_frame = tk.Frame(floor_panel, bg="light grey")
additional_button_frame.pack(pady=10)

open_button = tk.Button(additional_button_frame, text="Open Door", command=open_door, font=("Arial", 12), bg="white", fg="green", padx=20, pady=20, activebackground="green", activeforeground="white")
open_button.grid(row=0, column=0, padx=5, pady=5)

close_button = tk.Button(additional_button_frame, text="Close Door", command=close_door, font=("Arial", 12), bg="white", fg="red", padx=20, pady=20, activebackground="red", activeforeground="white")
close_button.grid(row=0, column=1, padx=5, pady=5)

emergency_button = tk.Button(additional_button_frame, text="Emergency", command=simulate_emergency, font=("Arial", 12), bg="white", fg="orange", padx=20, pady=20, activebackground="orange", activeforeground="white")
emergency_button.grid(row=0, column=2, padx=5, pady=5)

elevator_panel = tk.Frame(panel_frame, bg="light grey", padx=20, pady=20)
elevator_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

current_floor_label = tk.Label(elevator_panel, text="Current Floor: ", font=("Arial", 16), bg="light grey")
current_floor_label.pack(pady=10, side=tk.LEFT, padx=20)

current_floor_var = tk.IntVar(value=1)
floor_label = tk.Label(elevator_panel, textvariable=current_floor_var, font=("Arial", 24), bg="#F0F0F0")
floor_label.pack(pady=10, side=tk.LEFT, padx=20)

arrow_label = tk.Label(elevator_panel, text="", font=("Arial", 24), bg="#F0F0F0")
arrow_label.pack(pady=10, side=tk.LEFT, padx=20)

slider = tk.Scale(elevator_panel, from_=max_floors, to=1, orient=tk.VERTICAL, length=450, tickinterval=1, font=("Arial", 12), bg="#F0F0F0", fg="#333333", width=40)
slider.set(current_floor_var.get())
slider.pack(pady=20)

door_status_var = tk.StringVar(value="Closed")
door_status_label = tk.Label(elevator_panel, textvariable=door_status_var, font=("Arial", 16), bg="#F0F0F0")
door_status_label.pack(pady=20)

def listen_for_voice_commands():
    while True:
        handle_voice_command()

voice_thread = threading.Thread(target=listen_for_voice_commands)
voice_thread.daemon = True
voice_thread.start()

root.mainloop()
