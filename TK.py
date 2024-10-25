import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from transformers import pipeline

# Create the chatbot using a Hugging Face model
chatbot = pipeline("text-generation", model="gpt2")  # Use gpt-neo if your system allows

def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        audio = recognizer.listen(source)
        status_label.config(text="Processing audio...")
    try:
        text = recognizer.recognize_google(audio, language="en-US")
        input_text.insert(tk.END, text)
        status_label.config(text="Audio captured successfully!")
    except sr.UnknownValueError:
        status_label.config(text="Could not understand the audio.")
    except sr.RequestError:
        status_label.config(text="API error; please check your connection.")

def send_to_chatbot():
    prompt = input_text.get("1.0", tk.END).strip()
    if not prompt:
        messagebox.showwarning("Warning", "Please provide input text.")
        return

    # Modify the prompt to encourage direct responses
    formatted_prompt = f"Please answer the following question directly: '{prompt}'"

    try:
        status_label.config(text="Getting response from chatbot...")
        response = chatbot(
            formatted_prompt,
            max_length=50,  # Limit length for concise responses
            num_return_sequences=1,
            temperature=0.3  # Lower temperature for more focused responses
        )
        answer = response[0]['generated_text'].strip()
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, answer)
        status_label.config(text="Response received successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get response: {e}")

# Setup the Tkinter GUI
root = tk.Tk()
root.title("Speech-to-Chatbot")

# Input text area
tk.Label(root, text="Input Text:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
input_text = tk.Text(root, height=5, width=50)
input_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Output text area
tk.Label(root, text="Chatbot Response:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
output_text = tk.Text(root, height=5, width=50)
output_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Buttons
record_button = tk.Button(root, text="Record Audio", command=record_audio)
record_button.grid(row=4, column=0, padx=5, pady=10, sticky="e")

send_button = tk.Button(root, text="Send to Chatbot", command=send_to_chatbot)
send_button.grid(row=4, column=1, padx=5, pady=10, sticky="w")

# Status label
status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=5, column=0, columnspan=2)

root.mainloop()
