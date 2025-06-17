# 🔍 AI Log Analyzer — Smart Threat Detection from System Logs

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-ff69b4.svg)](https://github.com/your-username/ai-log-analyzer/issues)

An intelligent and minimal CLI tool to **analyze log files** and detect brute-force attempts, SQL injections, and SSH-based intrusions in real-time.

> 💡 Ideal for sysadmins, DevOps engineers, forensic analysts, and cybersecurity learners.

---

<!-- ## 📸 Demo Preview

> 📍 Example terminal output:

![Demo Screenshot Placeholder](https://via.placeholder.com/800x300.png?text=CLI+Demo+Coming+Soon)

--- -->

## 🚀 Features

- 🧠 AI-generated log summaries
- 🔐 Detects brute-force login attempts from logs
- 🧪 Flags SQL injection-like query patterns
- 💻 Highlights SSH root login or repeated access attempts
- 📊 Calculates a **Threat Level Score** (0 to 10)
- 🛡️ Provides security recommendations
- 🧼 CLI-friendly output (no markdown formatting issues)

---

## 🧰 Installation

### 📦 Step 1: Clone the Repo

```bash
git clone https://github.com/Cerbrus-Sec-Solutions/ai-log-analyzer.git
cd ai-log-analyzer
```

### 🧪 Step 2: (Optional) Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 📥 Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

> 🔸 Uses `colorama` for terminal coloring and Python's built-in modules.

---

## 🧪 Usage

### 🗂 Step 1: Provide a Log File

Place your `.log` file inside the project folder or specify the full path.

Example:
```
logs/auth.log
```

### ▶️ Step 2: Run the Analyzer

```bash
python main.py logs/auth.log
```

---

## 📊 Sample Input Format

Your `.log` file may contain entries like:

```
Failed password for root from 182.73.212.10 port 22 ssh2
Accepted password for user from 192.168.0.1 port 22 ssh2
Invalid user admin from 60.30.224.116 port 54321
Possible SQL Injection attempt: ' OR 1=1 --
```

---

## 🔐 Security Suggestions (Auto-Generated)

Depending on the threats detected, the analyzer may recommend:

- 🔒 Blocking IPs via `iptables`, `ufw`, or `.htaccess`
- 🚫 Disabling root login in `sshd_config`
- 🗝️ Enabling SSH key-based authentication
- 🔄 Installing tools like `fail2ban` or enabling firewall rules

---

## 🧠 Perfect For

- Cybersecurity students
- Threat analysts
- System admins/DevOps
- SOC teams and security tool builders

---

## 🌱 Future Enhancements

- [ ] Export reports as JSON / CSV
- [ ] Real-time log monitoring (background daemon)
- [ ] ELK Stack integration
- [ ] Web dashboard with charts and filters

---

## 🤝 Contributing

We welcome community contributions! Here's how:

1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Open a pull request with a clear explanation

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
