# File Monitor

![Python](https://img.shields.io/badge/Python-3.x-blue.svg) ![Tkinter](https://img.shields.io/badge/Tkinter-GUI-green.svg) ![Pygame](https://img.shields.io/badge/Pygame-Audio-orange.svg)

## 📌 Description

**File Monitor** is a Python application with a graphical user interface (GUI) designed to monitor a log file in real time. The program continuously checks for newly added lines and triggers an alarm if specific keywords are detected.

## 🚀 Features
- **Real-time monitoring** of a text file
- **Simple user interface** with Tkinter
- **Sound notifications** when keywords are detected
- **Saves and loads settings** from `config.properties`
- **Allows selection of file and alarm sound**

## 📂 Project Structure

```
file_monitor/
│── file_monitor.py  # Main script
│── config.properties  # Configuration file
│── README.md  # Documentation
│── ring.mp3  # Sample sound
│── requirements.txt  # Dependencies
```

## 🛠️ Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Cirou/File-Monitor.git
   cd File-Monitor
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the script:**
   ```sh
   python file_monitor.py
   ```

## ⚙️ Configuration
The `config.properties` file contains the settings:
```ini
[Settings]
file_path = file.txt
keywords = these, are, examples
alarm_sound = ring.mp3
check_interval = 1
memory_lines = 10
```
- `file_path`: Path of the file to monitor
- `keywords`: Comma-separated keywords
- `alarm_sound`: Audio file to play when an alarm is triggered
- `check_interval`: Update interval (seconds)
- `memory_lines`: Number of lines to keep in memory

## 🎮 Usage
- Launch the application.
- Select the file to monitor.
- Set the keywords.
- Press **Start Monitoring** to begin monitoring.
- The program will notify with a sound if keywords are detected.

## 📜 License
Distributed under the **MIT License**.

## ✨ Author
Created by [Cirou](https://github.com/Cirou) 🚀
