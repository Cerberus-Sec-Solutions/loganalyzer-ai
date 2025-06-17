# # main.py

# import argparse
# from analyzer import analyze_log_file
# from utils import get_ai_summary, export_pdf

# from colorama import init, Fore, Style
# init(autoreset=True)

# def main():
#     parser = argparse.ArgumentParser(description="🧠 logsentinel-ai: Smart Log Analyzer (CLI)")
#     parser.add_argument("--file", type=str, required=True, help="Path to your log file")
#     args = parser.parse_args()

#     print(Fore.CYAN + "\n📄 ANALYZING LOG FILE...\n" + Style.RESET_ALL)

#     report = analyze_log_file(args.file)

#     print(Fore.GREEN + "\n=== LOG ANALYSIS REPORT ===\n" + Style.RESET_ALL)
#     print(report)

#     # Ask for AI summary
#     use_ai = input(Fore.YELLOW + "\n🤖 Want AI Summary? (y/n): ").lower()
#     if use_ai == 'y':
#         print(Fore.YELLOW + "\n🔍 Generating AI Summary...\n")
#         ai = get_ai_summary(report)
#         print(Fore.MAGENTA + "\n=== AI SUMMARY ===\n")
#         print(ai)

#     # Ask for PDF export
#     save = input(Fore.CYAN + "\n📝 Save report to PDF? (y/n): ").lower()
#     if save == 'y':
#         filename = input("📁 Enter PDF filename (example: report.pdf): ")
#         export_pdf(filename, report)
#         print(Fore.GREEN + f"\n✅ PDF saved as {filename}")

# if __name__ == "__main__":
#     main()








# main.py (Merged Full Tool)

import argparse
import os
import re
from collections import Counter, defaultdict
from datetime import datetime
from colorama import init, Fore, Style
from fpdf import FPDF
from dotenv import load_dotenv
import openai

init(autoreset=True)
load_dotenv()

# ========== OpenAI Setup ==========
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
model_name = os.getenv("MODEL_NAME")

# ========== Core Log Analyzer ==========
def analyze_log_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            logs = f.readlines()
    except Exception as e:
        return f"❌ Error reading file: {e}", [], []

    brute_force_ips = Counter()
    error_paths = Counter()
    suspicious_queries = []
    unusual_commands = []
    file_access_issues = []
    tampering_signs = []
    timestamps = []
    ip_list = set()

    for line in logs:
        if "login failed" in line.lower() or "authentication failure" in line.lower():
            ip = re.search(r'[0-9]+(?:\.[0-9]+){3}', line)
            if ip:
                brute_force_ips[ip.group()] += 1
                ip_list.add(ip.group())

        err = re.search(r'"\s(\d{3})\s', line)
        if err and err.group(1) in ['403', '404', '500']:
            path = re.search(r'"(?:GET|POST)\s(.*?)\sHTTP', line)
            if path:
                error_paths[path.group(1)] += 1

        if re.search(r"(UNION|SELECT|DROP|INSERT|OR\s+1=1|--)", line, re.IGNORECASE):
            suspicious_queries.append(line.strip())

        if re.search(r'sudo|root|passwd|chmod|chown|nmap|bash|/etc/passwd', line):
            unusual_commands.append(line.strip())

        if re.search(r'/etc/passwd|\.bash_history|/var/log', line):
            file_access_issues.append(line.strip())

        if "log rotated" in line.lower() or "file truncated" in line.lower():
            tampering_signs.append(line.strip())

        ts = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', line)
        if ts:
            timestamps.append(ts.group(1))

    report = []
    if brute_force_ips:
        report.append("🛑 Brute Force Attempts:")
        for ip, count in brute_force_ips.items():
            report.append(f"  - {ip} failed to login {count} times")
    else:
        report.append("✅ No brute force attempts.")

    if error_paths:
        report.append("\n⚠️  Error Paths:")
        for path, count in error_paths.items():
            report.append(f"  - {path} returned errors {count} times")
    else:
        report.append("✅ No major error activity.")

    if suspicious_queries:
        report.append("\n🚨 SQLi Patterns Detected:")
        for line in suspicious_queries[:5]:
            report.append(f"  - {line}")
        if len(suspicious_queries) > 5:
            report.append(f"  - ...and {len(suspicious_queries) - 5} more lines")
    else:
        report.append("✅ No SQLi attempts.")

    if unusual_commands:
        report.append("\n🧑‍💻 Unusual Commands:")
        report.extend([f"  - {cmd}" for cmd in unusual_commands[:5]])

    if file_access_issues:
        report.append("\n🚪 Sensitive File Access:")
        report.extend([f"  - {path}" for path in file_access_issues[:5]])

    if tampering_signs:
        report.append("\n🧼 Log Tampering Signs:")
        report.extend([f"  - {sign}" for sign in tampering_signs[:5]])

    return "\n".join(report), timestamps, list(ip_list)

# ========== AI Features ==========
def get_ai_summary(text):
    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a cybersecurity log analyst."},
                {"role": "user", "content": f"Summarize this log report in bullet points:\n{text}"}
            ],
            temperature=0.3,
            max_tokens=800
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"[AI Error]: {e}"

def improvement_suggestions(text):
    return get_ai_summary(f"Suggest hardening steps based on this log report:\n{text}")

def explain_alerts(text):
    return get_ai_summary(f"Explain in simple terms the following security alerts:\n{text}")

def cleanup_advice(text):
    return get_ai_summary(f"Tell what kind of log entries are noise vs signal:\n{text}")

def rate_threat_level(text):
    return get_ai_summary(f"Rate threat level of the following log summary from 1-10 with justification:\n{text}")

# ========== PDF Export ==========
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


# ========== Other Features ==========
def keyword_search(file_path, keyword):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return "\n".join([line.strip() for line in f if keyword.lower() in line.lower()])
    except:
        return "[Error reading file]"

def count_log_levels(file_path):
    levels = defaultdict(int)
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if "INFO" in line: levels["INFO"] += 1
                if "ERROR" in line: levels["ERROR"] += 1
                if "WARN" in line: levels["WARN"] += 1
                if "DEBUG" in line: levels["DEBUG"] += 1
        return "\n".join([f"{k}: {v}" for k, v in levels.items()])
    except:
        return "[Failed to read log levels]"

def visualize_timeline(timestamps):
    time_counter = defaultdict(int)
    for t in timestamps:
        t_bin = t[:13]  # Hourly bin
        time_counter[t_bin] += 1
    for t, c in sorted(time_counter.items()):
        print(f"{t}: {'#' * c} ({c})")

def geoip_lookup(ip_list):
    for ip in ip_list:
        print(f"  - {ip} => [GeoIP Lookup Placeholder - Use offline DB/API if needed]")

# ========== Main CLI ==========
def main():
    parser = argparse.ArgumentParser(description="🧠 Cerberus Log Analyzer")
    parser.add_argument("--file", type=str, required=True, help="Path to your log file")
    parser.add_argument("--keyword", type=str, help="Keyword to search in logs")
    args = parser.parse_args()

    print(Fore.CYAN + "\n📄 ANALYZING LOG FILE...\n" + Style.RESET_ALL)
    report, timeline_data, ip_list = analyze_log_file(args.file)

    print(Fore.GREEN + "\n=== LOG ANALYSIS REPORT ===\n" + Style.RESET_ALL)
    print(report)

    if args.keyword:
        print(Fore.BLUE + f"\n🔍 Search Results for '{args.keyword}':\n")
        print(keyword_search(args.file, args.keyword))

    print(Fore.YELLOW + "\n📊 Log Level Stats:\n")
    print(count_log_levels(args.file))

    print(Fore.CYAN + "\n🕒 Timeline Visualization:\n")
    visualize_timeline(timeline_data)

    print(Fore.YELLOW + "\n🌍 GeoIP Lookup (Offline Mode):\n")
    geoip_lookup(ip_list)

    use_ai = input(Fore.YELLOW + "\n🤖 Want AI Summary & Suggestions? (y/n): ").lower()
    if use_ai == 'y':
        print(Fore.YELLOW + "\n🔍 Generating AI Summary...\n")
        ai = get_ai_summary(report)
        print(Fore.MAGENTA + "\n=== AI SUMMARY ===\n")
        print(ai)

        print(Fore.CYAN + "\n💡 Threat Level Rating:\n")
        print(rate_threat_level(report))

        print(Fore.BLUE + "\n📌 Hardening Recommendations:\n")
        print(improvement_suggestions(report))

        print(Fore.MAGENTA + "\n🧠 Pattern Explanations:\n")
        print(explain_alerts(report))

        print(Fore.YELLOW + "\n🧾 Log Cleanup Tips:\n")
        print(cleanup_advice(report))

    save = input(Fore.CYAN + "\n📝 Save report to PDF? (y/n): ").lower()
    if save == 'y':
        filename = input("📁 Enter PDF filename (example: report.pdf): ")
        export_pdf(filename, report)
        print(Fore.GREEN + f"\n✅ PDF saved as {filename}")

if __name__ == "__main__":
    main()
