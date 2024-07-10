import time
import tkinter as tk
import threading
import pyttsx3
from faster_whisper import WhisperModel
import speech_recognition as sr

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set speaking speed

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize Whisper model
model = WhisperModel("small")  # you can choose other model sizes: tiny, small, medium, large

# Map spelled-out numbers to their corresponding integers
number_map = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5,
    "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10,
    "One.": 1, "Two.": 2, "Three.": 3, "Four.": 4, "Five.": 5,
    "Six.": 6, "Seven.": 7, "Eight.": 8, "Nine.": 9, "Ten.": 10,
    "1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
    "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10,
    "First": 1, "Second": 2, "Third": 3, "Fourth": 4, "Fifth": 5,
    "Sixth": 6, "Seventh": 7, "Eighth": 8, "Ninth": 9, "Tenth": 10,
}

def recognize_speech_from_mic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # Save the audio to a file
    with open("microphone-results.wav", "wb") as f:
        f.write(audio.get_wav_data())

    # Path to the audio file you want to transcribe
    audio_path = "microphone-results.wav"
    
    # Transcribe the audio file
    segments, info = model.transcribe(audio_path)
    
    # Concatenate the transcribed segments into a single string
    transcription = "".join([segment.text for segment in segments])
    
    # Print the transcribed text
    print(transcription)
    return transcription

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
    instruction_label.config(text="Say something!")  # Update the label to prompt the user
    command = recognize_speech_from_mic()
    instruction_label.config(text="")  # Clear the label after recognizing the speech
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
        open = ["open", "Open", "open the door", "Open the door","Open."]
        close = ["close", "Close", "close the door", "Close the door","Close."]
        emergency = ["emergency", "Emergency", "emergency button", "Emergency button","Emergency."]
        if any(word in command for word in open):
            open_door()
        elif any(word in command for word in close):
            close_door()
        elif any(word in command for word in emergency):
            simulate_emergency()
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

current_floor_var = tk.IntVar(value=1)  # Default current floor is 1
floor_label = tk.Label(elevator_panel, textvariable=current_floor_var, font=("Arial", 24), bg="#F0F0F0")
floor_label.pack(pady=10, side=tk.LEFT, padx=20)

arrow_label = tk.Label(elevator_panel, text="", font=("Arial", 24), bg="#F0F0F0")
arrow_label.pack(pady=10, side=tk.LEFT, padx=20)

slider = tk.Scale(elevator_panel, from_=max_floors, to=1, orient=tk.VERTICAL, length=450, tickinterval=1, font=("Arial", 12), bg="#F0F0F0", fg="#333333", width=40)
slider.set(current_floor_var.get())
slider.pack(pady=20)

door_status_var = tk.StringVar(value="Closed")
door_status_label = tk.Label(elevator_panel, textvariable=door_status_var, font=("Arial", 16), bg="#F0F0F0")
door_status_label.pack(pady=10, side=tk.LEFT, padx=20)

instruction_label = tk.Label(elevator_panel, text="", font=("Arial", 16), bg="light grey", fg="blue")
instruction_label.pack(pady=10, side=tk.LEFT, padx=20)

# Start the speech recognition thread
def start_voice_recognition():
    while True:
        handle_voice_command()

voice_thread = threading.Thread(target=start_voice_recognition)
voice_thread.daemon = True
voice_thread.start()

root.mainloop()
