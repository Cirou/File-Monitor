import os
import sys
import time
import threading
from datetime import datetime
import configparser
import tkinter as tk
from tkinter import filedialog, scrolledtext

# Ensure pygame is installed
try:
    import pygame
except ImportError:
    os.system(f"{sys.executable} -m pip install pygame")
    import pygame

CONFIG_FILE = "config.properties"

def load_config():
    """Loads the configuration file and dynamically generates the file path if necessary."""
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as file:
            file.write("""[Settings]
file_path = file.txt
keywords = these, are, examples
alarm_sound = ring.mp3
check_interval = 1
memory_lines = 10
""")

    config = configparser.RawConfigParser()
    config.read(CONFIG_FILE)

    file_path = config.get("Settings", "file_path", fallback="file.txt")
    keywords = config.get("Settings", "keywords", fallback="these, are, examples")
    alarm_sound = config.get("Settings", "alarm_sound", fallback="ring.mp3")
    check_interval = config.getint("Settings", "check_interval", fallback=1)
    memory_lines = config.getint("Settings", "memory_lines", fallback=10)

    return file_path, keywords, alarm_sound, check_interval, memory_lines

def save_config(file_path_template, keywords, alarm_sound, check_interval, memory_lines):
    """Saves updated settings to the configuration file."""
    config = configparser.RawConfigParser()
    config.read(CONFIG_FILE)
    config["Settings"] = {
        "file_path": file_path_template,
        "keywords": keywords,
        "alarm_sound": alarm_sound,
        "check_interval": str(check_interval),
        "memory_lines": str(memory_lines),
    }
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)

def play_sound(sound_file):
    """Plays the alarm sound using pygame."""
    if not os.path.exists(sound_file):
        print("❌ Error: The sound file does not exist!")
        return
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

def follow_file(file_path):
    """Monitors the file in real-time, reading only newly added lines."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file.seek(0, os.SEEK_END)
            while True:
                line = file.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                yield line.strip()
    except FileNotFoundError:
        while not os.path.exists(file_path):
            time.sleep(1)
        follow_file(file_path)

def check_keywords_in_memory(memory, keywords):
    """Checks if any keyword is present in the last N lines (case insensitive)."""
    keyword_list = [kw.strip().lower() for kw in keywords.split(",")]  # Convert keywords to lowercase
    return any(any(keyword in line.lower() for keyword in keyword_list) for line in memory)  # Convert line to lowercase

class FileMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Monitor")
        self.root.geometry("500x550")  # Increased height for notification
        self.root.resizable(False, False)

        self.monitoring = False
        self.thread = None

        # Load saved settings
        file_path, keywords, alarm_sound, check_interval, memory_lines = load_config()

        # File Path Section
        tk.Label(root, text="File Path:").pack(pady=(10, 0))
        file_frame = tk.Frame(root)
        file_frame.pack(pady=(0, 10))
        
        self.file_path_var = tk.StringVar(value=file_path)
        self.file_path_entry = tk.Entry(file_frame, textvariable=self.file_path_var, width=50)
        self.file_path_entry.grid(row=0, column=0, padx=(0, 5))
        
        self.browse_button = tk.Button(file_frame, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=1)


        # Keywords Section
        tk.Label(root, text="Keywords (comma separated):").pack(pady=(0, 0))
        self.keywords_var = tk.StringVar(value=keywords)
        self.keywords_entry = tk.Entry(root, textvariable=self.keywords_var, width=60)
        self.keywords_entry.pack(pady=(0, 10))

        # Alarm Sound Section with Play Button
        tk.Label(root, text="Alarm Sound File:").pack(pady=(0, 0))
        sound_frame = tk.Frame(root)
        sound_frame.pack(pady=(0, 10))

        self.alarm_sound_var = tk.StringVar(value=alarm_sound)
        self.alarm_sound_entry = tk.Entry(sound_frame, textvariable=self.alarm_sound_var, width=50)
        self.alarm_sound_entry.grid(row=0, column=0, padx=(0, 5))

        self.play_button = tk.Button(sound_frame, text="▶ Play", command=self.test_sound)
        self.play_button.grid(row=0, column=1)
        
        # Check Interval & Memory Lines Section
        settings_frame = tk.Frame(root)
        settings_frame.pack(pady=(0, 10))

        tk.Label(settings_frame, text="Check Interval (sec):").grid(row=0, column=0, padx=5)
        self.check_interval_var = tk.IntVar(value=check_interval)
        self.check_interval_entry = tk.Entry(settings_frame, textvariable=self.check_interval_var, width=5)
        self.check_interval_entry.grid(row=0, column=1, padx=5)

        tk.Label(settings_frame, text="Memory Lines:").grid(row=0, column=2, padx=5)
        self.memory_lines_var = tk.IntVar(value=memory_lines)
        self.memory_lines_entry = tk.Entry(settings_frame, textvariable=self.memory_lines_var, width=5)
        self.memory_lines_entry.grid(row=0, column=3, padx=5)

        # Notification Bar
        self.notification_var = tk.StringVar(value="The monitoring is not active")
        self.notification_label = tk.Label(root, textvariable=self.notification_var, fg="red")
        self.notification_label.pack(pady=(5, 5))

        # Log Display Section
        tk.Label(root, text="Recent File Entries:").pack(pady=(0, 0))
        self.log_display = scrolledtext.ScrolledText(root, width=50, height=12, state="disabled")
        self.log_display.configure(font=("Courier", 10))
        self.log_display.pack(pady=(0, 10))

        # Start/Stop Buttons Section
        button_frame = tk.Frame(root)
        button_frame.pack(pady=(0, 10))

        self.start_button = tk.Button(button_frame, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.grid(row=0, column=0, padx=15)

        self.stop_button = tk.Button(button_frame, text="Stop Monitoring", command=self.stop_monitoring, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=15)

        # Bind config change detection
        self.bind_config_events()

    def bind_config_events(self):
        """Detects when any configuration field is changed and shows a warning."""
        fields = [self.file_path_var, self.keywords_var, 
                  self.alarm_sound_var, self.memory_lines_var, self.check_interval_var]
        for field in fields:
            field.trace_add("write", self.config_modified)

    def config_modified(self, *args):
        """Updates the notification bar when a config is modified."""
        self.notification_var.set("Restart monitoring to apply the new configuration")

    def start_monitoring(self):
        """Starts monitoring the file and saves configuration before starting."""
        self.notification_var.set("Monitoring started with the applied configuration")
        save_config(self.file_path_var.get(), 
                    self.keywords_var.get(),
                    self.alarm_sound_var.get(), 
                    self.check_interval_var.get(), 
                    self.memory_lines_var.get())
        self.monitoring = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.thread = threading.Thread(target=self.monitor_file, daemon=True)
        self.thread.start()

    def stop_monitoring(self):
        """Stops monitoring the file."""
        self.monitoring = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.notification_var.set("The monitoring is not active")
        
    def test_sound(self):
        """Plays the selected alarm sound from the UI."""
        sound_file = self.alarm_sound_var.get()
        play_sound(sound_file)

    def monitor_file(self):
        """Monitors the file and updates the UI in real-time."""

        file_path = self.file_path_var.get()
        keywords = self.keywords_var.get()
        alarm_sound = self.alarm_sound_var.get()
        check_interval = self.check_interval_var.get()
        memory_lines = self.memory_lines_var.get()
        
        memory = []

        for line in follow_file(file_path):
            if not self.monitoring:
                break
            memory.append(line)
            if len(memory) > memory_lines:
                memory.pop(0)
            self.update_log_display(memory)
            if check_keywords_in_memory(memory, keywords):
                play_sound(alarm_sound)
            time.sleep(check_interval)  # Wait for the next check

    def update_log_display(self, memory):
        """Updates the log display area with the latest lines and scrolls automatically."""
        self.log_display.config(state="normal")  # Enable editing
        self.log_display.delete(1.0, tk.END)  # Clear old content
        self.log_display.insert(tk.END, "\n".join(memory) + "\n")  # Add new lines
        self.log_display.see(tk.END)  # Auto-scroll to bottom
        self.log_display.config(state="disabled")  # Disable editing
        self.log_display.update_idletasks()  # Force UI update

    def browse_file(self):
        """Opens a file dialog to select the log file."""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_var.set(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileMonitorApp(root)
    root.mainloop()
