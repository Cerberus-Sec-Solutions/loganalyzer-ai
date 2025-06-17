import openai
import os
from dotenv import load_dotenv
from fpdf import FPDF
import re

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
model_name = os.getenv("MODEL_NAME")

def clean_ai_response(text):
    """Remove all markdown formatting from AI response"""
    # Remove bold formatting **text** -> text
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    # Remove italic formatting *text* -> text  
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    # Remove any remaining single asterisks
    text = re.sub(r'\*', '', text)
    # Remove markdown headers ### -> 
    text = re.sub(r'#{1,6}\s*', '', text)
    # Remove code backticks `code` -> code
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Clean up extra spaces and newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()

def get_ai_summary(text):
    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a cybersecurity log analyst. Provide clear, simple analysis without any markdown formatting or bold text."},
                {"role": "user", "content": f"Summarize this log report in simple bullet points without bold formatting:\n{text}"}
            ],
            temperature=0.3,
            max_tokens=1000,
            headers={
                "Authorization": f"Bearer {openai.api_key}",
                "HTTP-Referer": "https://yourdomain.com",
                "X-Title": "CerberusLogAnalyzer"
            }
        )
        
        ai_response = response['choices'][0]['message']['content']
        # Clean the AI response before returning
        return clean_ai_response(ai_response)
        
    except Exception as e:
        return f"[AI Error]: {e}"

def improvement_suggestions(text):
    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert. Provide hardening recommendations in plain text without markdown formatting."},
                {"role": "user", "content": f"Suggest security hardening steps based on this log report (no bold text):\n{text}"}
            ],
            temperature=0.3,
            max_tokens=800
        )
        ai_response = response['choices'][0]['message']['content']
        return clean_ai_response(ai_response)
    except Exception as e:
        return f"[AI Error]: {e}"

def explain_alerts(text):
    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a cybersecurity teacher. Explain security alerts in simple terms without markdown formatting."},
                {"role": "user", "content": f"Explain these security alerts in simple terms (no bold formatting):\n{text}"}
            ],
            temperature=0.3,
            max_tokens=800
        )
        ai_response = response['choices'][0]['message']['content']
        return clean_ai_response(ai_response)
    except Exception as e:
        return f"[AI Error]: {e}"

def cleanup_advice(text):
    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a log management expert. Provide advice in plain text without markdown."},
                {"role": "user", "content": f"Explain what log entries are noise vs signal (no formatting):\n{text}"}
            ],
            temperature=0.3,
            max_tokens=800
        )
        ai_response = response['choices'][0]['message']['content']
        return clean_ai_response(ai_response)
    except Exception as e:
        return f"[AI Error]: {e}"

def rate_threat_level(text):
    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a threat analyst. Rate threats in plain text without any bold formatting."},
                {"role": "user", "content": f"Rate threat level 1-10 with simple explanation (no bold text):\n{text}"}
            ],
            temperature=0.3,
            max_tokens=600
        )
        ai_response = response['choices'][0]['message']['content']
        return clean_ai_response(ai_response)
    except Exception as e:
        return f"[AI Error]: {e}"

def remove_non_latin1(text):
    return ''.join(c for c in text if ord(c) < 256)

def export_pdf(filename, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Also clean content before PDF export
    content = clean_ai_response(content)
    for line in content.split("\n"):
        line = remove_non_latin1(line)
        pdf.cell(200, 10, txt=line, ln=1)
    pdf.output(filename)

# Test the cleaning function
if __name__ == "__main__":
    test_ai_output = """
    **Log Summary:**
    - **Brute Force Attempts**: 28 unique IPs detected
    - **High-frequency attempts**: 150.183.249.110 with **80 failed attempts**
    - `Root user` targeted multiple times
    """
    
    
    print("\nCleaned output:")
    print(clean_ai_response(test_ai_output))