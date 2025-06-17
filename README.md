
````markdown
# 🔐 AI Log Analyser — Smart Threat Detection from Logs

Welcome to **AI Log Analyser**, your automated AI-powered assistant for identifying brute-force attacks, SQL injection attempts, and suspicious SSH activity from raw log files.

✨ Built for sysadmins, cybersecurity analysts, and DevOps engineers who want **clarity in chaos**.

---

## 🚀 Features

- 🧠 AI-Powered Summary: Instantly understand what's happening inside your logs without reading every line.
- 🔐 Brute Force Detection: Identifies aggressive IPs attempting to break into your system.
- 🛡️ SQL Injection Pattern Scan: Flags suspicious queries that resemble injection attacks.
- 💻 SSH Attack Recognition: Detects unusual or targeted SSH login attempts (e.g., against root).
- 📊 Threat Level Estimation: Rates the overall threat score from 0 to 10.
- ⚠️ Actionable Recommendations: Security hardening tips generated based on detected behavior.
- 🧼 Clean Output: No markdown bold characters — perfect for CLI use or automation scripts.

---

## 📂 How It Works

Feed any raw log file (Apache, Nginx, auth.log, or custom logs) into the tool, and it will:
1. Scan for brute force IPs
2. Look for SQL injection-like patterns
3. Detect repeated SSH login failures
4. Summarize threat patterns with severity
5. Suggest practical mitigation strategies

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-log-analyser.git
cd ai-log-analyser
````

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

> ✅ Requirements include:
>
> * Python built-ins: `re`, `collections`, `os`
> * Third-party: `colorama`

---

## 🧪 Usage

### Step 1: Place Your Log File

Put your log file in the same directory or use the full path.

Example:

```
path/to/your/file/file_name.log
```

### Step 2: Run the Tool

```bash
python main.py path/to/your/file/file_name.log
```

You’ll get a detailed summary in your terminal 
## 📊 Sample Input Format

A few log entries your file might contain:


## 🔧 Security Recommendations

From your logs, the tool may suggest:

* Blocking brute-force IPs
* Disabling remote root logins
* Enabling SSH key-based authentication
* Setting up rate limiting (fail2ban / iptables)
* Verifying suspicious root login events

---

## 👥 Who Should Use This?

* 🔐 Cybersecurity learners & pros
* 💻 DevOps and sysadmins
* 🎓 Final-year students building real-world projects
* 🧪 Anyone doing log analysis or forensic review

---

## 🛠 Future Improvements

* [ ] JSON/CSV export of reports
* [ ] Real-time log monitoring (daemon mode)
* [ ] ELK/Graylog integration
* [ ] Web UI Dashboard

---

## 🤝 Contributing

Found a bug or have a feature idea?
Create a pull request or open an issue — contributions are welcome!

---

<!-- ## 👨‍💻 Author

Created with 💻 by **A V S Sai Teja**
Cybersecurity & Automation Enthusiast
[LinkedIn](https://linkedin.com/in/yourprofile) • [GitHub](https://github.com/your-username) -->



