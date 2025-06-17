# utils.py
import openai
import os
from dotenv import load_dotenv
from fpdf import FPDF

load_dotenv()


print("DEBUG: OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))
print("DEBUG: OPENAI_API_BASE =", os.getenv("OPENAI_API_BASE"))
print("DEBUG: MODEL_NAME =", os.getenv("MODEL_NAME"))


openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
model_name = os.getenv("MODEL_NAME")

def get_ai_summary(text):
    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a cybersecurity log analyst."},
                {"role": "user", "content": f"Summarize this log report in bullet points:\n{text}"}
            ],
            temperature=0.3,
            max_tokens=1000,
            headers={
                "Authorization": f"Bearer {openai.api_key}",
                "HTTP-Referer": "https://yourdomain.com",  # Optional
                "X-Title": "CerberusLogAnalyzer"  # Optional
            }
        )

        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"[AI Error]: {e}"

import unicodedata

def remove_non_latin1(text):
    return ''.join(c for c in text if ord(c) < 256)

def export_pdf(filename, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in content.split("\n"):
        line = remove_non_latin1(line)
        pdf.cell(200, 10, txt=line, ln=1)
    pdf.output(filename)

