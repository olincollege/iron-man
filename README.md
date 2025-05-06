# The Iron Man Project

## Purpose

The `iron-man` project is designed to simulate advanced voice-controlled
functionalities inspired by the Iron Man suit. It provides a framework for
executing commands and interacting with Jarvis, the AI voice assistant in Tony
Stark's ear. This repository contains the back-end logic for the Jarvis AI
integrated onto a RaspberryPi 5 attached to our physical helmet to execute
commands with the Arduino Nano uploaded with the `JarvisArduino.ino` script.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/eddydpan/iron-man.git
   cd iron-man
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python3 jarvis_v3.py
   ```

## Voice Commands

- Jarvis, activate
- Jarvis, say cheese
- Jarvis, open helmet
- Jarvis, close helmet
