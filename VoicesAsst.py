import tkinter as tk
import speech_recognition as sr
import pyttsx3
import datetime
import subprocess
import webbrowser


# Initialize Tkinter
root = tk.Tk()
root.title("Voice Assistant GUI")

# Create the main frame
frame = tk.Frame(root, bg='#ffffff', height=500, width=800)
frame.pack_propagate(False)  # To prevent the frame from adjusting its size based on its content
frame.pack()

# Voice Assistant Label
voice_label = tk.Label(frame, text="Voice Assistant", font=("Inter-ExtraBold", 32, "bold"), fg='#000000', bg='#ffffff')
voice_label.place(x=275, y=18)

# Rectangle-1 Component for bot's speech
rectangle_1 = tk.Frame(frame, bg='#d9d9d9', width=614, height=292)
rectangle_1.place(x=93, y=87)

# Create speech recognition and text-to-speech objects
recognizer = sr.Recognizer()
engine = pyttsx3.init()


# Function to speak and display text in Rectangle-1
def speak_and_display(text):
    engine.say(text)
    engine.runAndWait()
    text_label.config(text=text)


# Function to recognize user's speech
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-us')
        print("User said:", query)
        return query
    except Exception as e:
        print("Error:", str(e))
        return ""


# Function to handle user's commands
def handle_command():
    command = recognize_speech()
    if command:
        if "ken" in command.lower():
            speak_and_display("Hello! How can I help you?")
        elif "time" in command.lower():
            now = datetime.datetime.now().strftime("%H:%M")
            speak_and_display(f"The current time is {now}")
        elif "date" in command.lower():
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            speak_and_display(f"Today's date is {today}")
        elif "search" in command.lower():
            speak_and_display("What do you want me to search for?")
            query = recognize_speech()
            if query:
                search_url = "https://www.google.com/search?q=" + query
                webbrowser.open(search_url)
        elif "play" in command.lower() and "music" in command.lower():
            speak_and_display("What music would you like to listen to?")
            query = recognize_speech()
            if query:
                music_url = "https://www.youtube.com/results?search_query=" + query.replace(" ", "+")
                webbrowser.open(music_url)

        elif "open" in command.lower():
            # Extract the application name from the command
            app_name = command.lower().replace("open", "").strip()
            speak_and_display(f"Opening {app_name}.")

            try:
                # Use subprocess to open the application dynamically
                subprocess.run([app_name + ".exe"])
            except FileNotFoundError:
                speak_and_display(f"Sorry, I couldn't find {app_name}.")
        elif "exit" in command.lower():
            speak_and_display("Goodbye!")
            root.destroy()  # Close the Tkinter GUI
        else:
            speak_and_display("Sorry, I didn't understand that.")

    root.after(100, handle_command)  # Schedule the next call to handle_command


# Label to display bot's speech in Rectangle-1
text_label = tk.Label(rectangle_1, text="", font=("Arial", 14), bg='#d9d9d9')
text_label.pack(expand=True, fill ="both")

# Start the Tkinter main loop
root.geometry('800x500')
root.after(100, handle_command)  # Schedule the first call to handle_command
root.mainloop()
