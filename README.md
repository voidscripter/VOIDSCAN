# VOIDSCAN

> A lightweight Linux system analyzer built for the terminal.

**VOIDSCAN** is an open-source Linux system analyzer that scans your system and displays useful information about your hardware, performance, network, and operating system directly in the terminal.

The project is designed to be lightweight, readable, modular, and easy to modify.

## ✨ Features

* 🖥️ System information
* ⚙️ CPU information and usage
* 🎮 GPU detection
* 🧠 RAM usage
* 💾 Disk usage
* 📊 System performance
* 🌐 Network information
* 🌡️ Temperature detection when available
* 📄 JSON report generation
* 🎨 Clean terminal interface
* 🐧 Designed for Linux
* 🔓 Fully open-source source code

## 🛠️ Built With

* Python 3
* [psutil](https://github.com/giampaolo/psutil)
* [Rich](https://github.com/Textualize/rich)
* Python Standard Library

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/voidscripter/VOIDSCAN.git
cd VOIDSCAN
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🚀 Usage

Run VOIDSCAN:

```bash
python -m voidscan
```

Available commands:

```text
--help
--version
--hardware
--performance
--network
--report
```

Example:

```bash
python -m voidscan --hardware
```

Generate a system report:

```bash
python -m voidscan --report
```

This generates:

```text
voidscan-report.json
```

## 📊 Example

```text
╭──────────────────────────────────────╮
│               VOIDSCAN               │
│          System Analyzer             │
╰──────────────────────────────────────╯

SYSTEM
  OS        CachyOS
  Kernel    6.16.x
  Uptime    4h 32m

HARDWARE
  CPU       AMD Ryzen 5 5600
  GPU       NVIDIA RTX 3050
  RAM       16 GB
  Disk      412 GB / 1 TB

PERFORMANCE
  CPU       ███████░░░ 67%
  RAM       █████░░░░░ 48%
  DISK      ███░░░░░░░ 31%

NETWORK
  Status    ● Connected
  Download  82.4 MB/s
  Upload    11.2 MB/s

──────────────────────────────────────

✓ System scan completed
```

## 📁 Project Structure

```text
VOIDSCAN/
├── src/
│   └── voidscan/
│       ├── __init__.py
│       ├── main.py
│       ├── system.py
│       ├── hardware.py
│       ├── performance.py
│       ├── network.py
│       ├── display.py
│       └── report.py
├── tests/
├── README.md
├── requirements.txt
├── pyproject.toml
├── LICENSE
├── CONTRIBUTING.md
└── .gitignore
```

## 🔓 Open Source

VOIDSCAN is **open-source**.

The complete source code is available in this repository. You are free to inspect the code, learn from it, modify it, and contribute improvements according to the project's license.

## 🤝 Contributing

Contributions are welcome.

You can:

* Report bugs
* Suggest features
* Improve documentation
* Improve performance
* Submit pull requests
* Add Linux compatibility improvements

Please read `CONTRIBUTING.md` before contributing.

## 🔒 Privacy & Safety

VOIDSCAN is designed to be **read-only by default**.

It does not:

* Modify system files
* Require root access for normal operation
* Execute arbitrary shell commands
* Collect passwords or secrets
* Upload system information to a remote server

## 📜 License

This project is distributed under the license included in the `LICENSE` file.

## 👤 Author

**VoidScripter**

GitHub: https://github.com/voidscripter

---

### VOIDSCAN

**Scan your system. Know your machine.**
