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
    

