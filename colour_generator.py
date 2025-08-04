import tkinter as tk
from tkinter import messagebox
import google.generativeai as genai
from PIL import Image, ImageTk
import io, re
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_palette(prompt):
    try:
        response = model.generate_content(
           f"Generate a 5-color palette (hex codes only) for the theme: {prompt}. Return the hex codes, comma-seperated."
        )
        text = response.text
        codes = re.findall(r"#(?:[0-9a-fA-F]{3}){1,2}", text)
        return codes[:5]
    except Exception as e:
        print("Gemini error", e)
        return []
    

app = tk.Tk()
app.title("colour palette hehehhe")
app.geometry("500x400")
app.resizable(False, False)

tk.Label(app, text="Enter a theme:")
entry = tk.Entry(app, width=40)
entry.pack()

swatch_frame = tk.Frame(app)
swatch_frame.pack(pady=20)

swatches = []

for i in range(5):
    frame = tk.Frame(swatch_frame)
    frame.grid(row=0, column=i, padx=5)

    canvas = tk.Canvas(frame, width=60, height=60, bg="#ffffff", highlightthickness=1, highlightbackground="black")
    canvas.pack()
    
    label = tk.Label(frame, text="#------")
    label.pack()
    swatches.append((canvas, label))

def generate_palette():
    theme = entry.get().strip()
    if not theme:
        messagebox.showwarning("Input Required", "Please enter a theme")
        return
    
    colours = get_palette(theme)
    if not colours:
        messagebox.showerror("Error", "Could not generate palette. Try another theme")
        return
    
    for (canvas, label), colour in zip(swatches, colours):
        canvas.config(bg=colour)
        label.config(text=colour)

tk.Button(app, text="Generate Palette", 
          command=generate_palette, bg="lightblue").pack(pady=10)

app.mainloop()



