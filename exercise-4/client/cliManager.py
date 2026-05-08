"""
cliManager — TCP Chat Client (Exercise 4)

Author      : Gianpaolo Detomaso
Date        : 2026-05-06
Version     : 1.0
"""


import sys
import threading
import termios
import tty

import socketManager

# Shared state
inputBuffer = ""
lock = threading.Lock()


def clearLine():
    """Clear the current terminal line (used to keep the prompt tidy)."""
    sys.stdout.write("\r\033[K")


def redrawPrompt():
    """Redraw the prompt showing the current typed buffer."""
    sys.stdout.write(f"\r{socketManager.username}: {inputBuffer}")
    sys.stdout.flush()


def print(message):
    """Thread-safe print that preserves the interactive prompt."""
    with lock:
        clearLine()
        sys.stdout.write(f"{message}\n")
        redrawPrompt()


def readInput():
    """
    Read user input character-by-character.

    - Enter (\n) sends the current buffer to the server.
    - Typing "exit" (then Enter) stops the input loop.
    - Backspace deletes the last character.

    The loop runs while `socketManager.running` is True.
    """
    global inputBuffer

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)  # read char-by-char

        while socketManager.running:
            ch = sys.stdin.read(1)

            with lock:
                if ch == "\n":  # Enter
                    clearLine()

                    if inputBuffer.lower() == "exit":
                        # Stop input loop (note: server/client shutdown behavior is driven by socketManager.running)
                        socketManager.running = False
                        break

                    socketManager.sendMessage(inputBuffer)
                    inputBuffer = ""

                elif ch == "\x7f":  # Backspace
                    inputBuffer = inputBuffer[:-1]

                else:
                    inputBuffer += ch

                clearLine()
                redrawPrompt()

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

