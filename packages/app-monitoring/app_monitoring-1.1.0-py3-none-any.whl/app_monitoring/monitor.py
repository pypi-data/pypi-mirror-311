# Clean up messages of information when fortifai starts up

# # Output

# Handle command line options                                                      [Success]
# Checking license file                                                            [Success]
# Setup Signal Handler                                                             [Success]
# Loading configuration file                                                       [Success]
# Initializing runtime configuration                                               [Success]
# Initializing Platform                                                            [Success]
# Initializing Directors                                                           [Success]
# Initializing Outputs                                                             [Success]
# Initializing Cameras                                                             [Success]
# Load detection model for camera 1                                                [Success]
# Load single object tracking model for camera 1                                   [Success]
# Load multiple object tracking model for camera 1                                 [Success]
# Initializing WsServer                                                            [Success]
# Initializing Radars                                                              [Success]
# Fortifai is running...                                                           [Success]
# Fortifai is exiting...                                                           [Success]

import os
import time
from collections import OrderedDict

# Path to the log file
LOG_FILE = "app.log"

# List of steps and their keywords to monitor
STEPS = OrderedDict({
    "Handle command line options": {"Success": ["Command line options handled successfully"], "Failed": ["Failed to handle command line options"]},
    "Checking license file": {"Success": ["License file checked successfully"], "Failed": ["Failed to check license file"]},
    "Setup Signal Handler": {"Success": ["Signal handler set up successfully"], "Failed": ["Signal handler set up failed"]},
    "Loading configuration file": {"Success": ["Configuration file loaded successfully"], "Failed": ["Failed to load configuration file"]},
    "Initializing runtime configuration": {"Success": ["Runtime configuration initialized successfully"], "Failed": ["Runtime configuration initialized failed"]},
    "Initializing Platform": {"Success": ["Platform initialized successfully"], "Failed": ["Failed to initialize Platform"]},
    "Initializing Directors": {"Success": ["Directors initialized successfully"], "Failed": ["Failed to initialize Directors"]},
    "Initializing Outputs": {"Success": ["Outputs initialized successfully"], "Failed": ["Failed to initialize Outputs", "LLVM ERROR: out of memory"]},
    "Initializing Cameras": {"Success": ["Cameras initialized successfully"], "Failed": ["Failed to initialize Cameras"]},
    "Initializing WsServer": {"Success": ["WsServer initialized successfully"], "Failed": ["Failed to initialize WsServer"]},
    "Initializing Radars": {"Success": ["Radars initialized successfully"], "Failed": ["Failed to initialize Radars"]},
    "Load detection model for camera 1": {"Success": ["Load detection model for camera 1 successfully"], "Failed": ["Failed to initialise detection for camera 1"]},
    "Load detection model for camera 2": {"Success": ["Load detection model for camera 2 successfully"], "Failed": ["Failed to initialise detection for camera 2"]},
    "Load detection model for camera 3": {"Success": ["Load detection model for camera 3 successfully"], "Failed": ["Failed to initialise detection for camera 3"]},
    "Load detection model for camera 4": {"Success": ["Load detection model for camera 4 successfully"], "Failed": ["Failed to initialise detection for camera 4"]},
    "Load single object tracking model for camera 1": {"Success": ["Load single object tracking model for camera 1 successfully"], "Failed": ["Failed to initialise single object tracking for camera 1"]},
    "Load single object tracking model for camera 2": {"Success": ["Load single object tracking model for camera 2 successfully"], "Failed": ["Failed to initialise single object tracking for camera 2"]},
    "Load single object tracking model for camera 3": {"Success": ["Load single object tracking model for camera 3 successfully"], "Failed": ["Failed to initialise single object tracking for camera 3"]},
    "Load single object tracking model for camera 4": {"Success": ["Load single object tracking model for camera 4 successfully"], "Failed": ["Failed to initialise single object tracking for camera 4"]},
    "Load multiple object tracking model for camera 1": {"Success": ["Load multiple object tracking model for camera 1 successfully"], "Failed": ["Failed to initialise multiple object tracking for camera 1"]},
    "Load multiple object tracking model for camera 2": {"Success": ["Load multiple object tracking model for camera 2 successfully"], "Failed": ["Failed to initialise multiple object tracking for camera 2"]},
    "Load multiple object tracking model for camera 3": {"Success": ["Load multiple object tracking model for camera 3 successfully"], "Failed": ["Failed to initialise multiple object tracking for camera 3"]},
    "Load multiple object tracking model for camera 4": {"Success": ["Load multiple object tracking model for camera 4 successfully"], "Failed": ["Failed to initialise multiple object tracking for camera 4"]},
    "Load pose estimation model for camera 1": {"Success": ["Load pose estimation model for camera 1 successfully"], "Failed": ["Failed to initialise pose estimation for camera 1"]},
    "Load pose estimation model for camera 2": {"Success": ["Load pose estimation model for camera 2 successfully"], "Failed": ["Failed to initialise pose estimation for camera 2"]},
    "Load pose estimation model for camera 3": {"Success": ["Load pose estimation model for camera 3 successfully"], "Failed": ["Failed to initialise pose estimation for camera 3"]},
    "Load pose estimation model for camera 4": {"Success": ["Load pose estimation model for camera 4 successfully"], "Failed": ["Failed to initialise pose estimation for camera 4"]},
    "Load colour recognition model for camera 1": {"Success": ["Load colour recognition model for camera 1 successfully"], "Failed": ["Failed to initialise colour recognition for camera 1"]},
    "Load colour recognition model for camera 2": {"Success": ["Load colour recognition model for camera 2 successfully"], "Failed": ["Failed to initialise colour recognition for camera 2"]},
    "Load colour recognition model for camera 3": {"Success": ["Load colour recognition model for camera 3 successfully"], "Failed": ["Failed to initialise colour recognition for camera 3"]},
    "Load colour recognition model for camera 4": {"Success": ["Load colour recognition model for camera 4 successfully"], "Failed": ["Failed to initialise colour recognition for camera 4"]},
    "Load ReID model for camera 1": {"Success": ["Load ReID model for camera 1 successfully"], "Failed": ["Failed to initialise ReID for camera 1"]},
    "Load ReID model for camera 2": {"Success": ["Load ReID model for camera 2 successfully"], "Failed": ["Failed to initialise ReID for camera 2"]},
    "Load ReID model for camera 3": {"Success": ["Load ReID model for camera 3 successfully"], "Failed": ["Failed to initialise ReID for camera 3"]},
    "Load ReID model for camera 4": {"Success": ["Load ReID model for camera 4 successfully"], "Failed": ["Failed to initialise ReID for camera 4"]},
    "Load OCR model for camera 1": {"Success": ["Load OCR model for camera 1 successfully"], "Failed": ["Failed to initialise OCR for camera 1"]},
    "Load OCR model for camera 2": {"Success": ["Load OCR model for camera 2 successfully"], "Failed": ["Failed to initialise OCR for camera 2"]},
    "Load OCR model for camera 3": {"Success": ["Load OCR model for camera 3 successfully"], "Failed": ["Failed to initialise OCR for camera 3"]},
    "Load OCR model for camera 4": {"Success": ["Load OCR model for camera 4 successfully"], "Failed": ["Failed to initialise OCR for camera 4"]},
    "Setup Object direction for camera 1": {"Success": ["Failed to initialise Object direction for camera 1"], "Failed": []},
    "Setup Object direction for camera 2": {"Success": ["Failed to initialise Object direction for camera 2"], "Failed": []},
    "Setup Object direction for camera 3": {"Success": ["Failed to initialise Object direction for camera 3"], "Failed": []},
    "Setup Object direction for camera 4": {"Success": ["Failed to initialise Object direction for camera 4"], "Failed": []},
    "Load Violence detection model for camera 1": {"Success": ["Load Violence detection model for camera 1 successfully"], "Failed": ["Failed to initialise Violence detection for camera 1"]},
    "Load Violence detection model for camera 2": {"Success": ["Load Violence detection model for camera 2 successfully"], "Failed": ["Failed to initialise Violence detection for camera 2"]},
    "Load Violence detection model for camera 3": {"Success": ["Load Violence detection model for camera 3 successfully"], "Failed": ["Failed to initialise Violence detection for camera 3"]},
    "Load Violence detection model for camera 4": {"Success": ["Load Violence detection model for camera 4 successfully"], "Failed": ["Failed to initialise Violence detection for camera 4"]},
    "Load NSFW model for camera 1": {"Success": ["Load NSFW model for camera 1 successfully"], "Failed": ["Failed to initialise NSFW for camera 1"]},
    "Load NSFW model for camera 2": {"Success": ["Load NSFW model for camera 2 successfully"], "Failed": ["Failed to initialise NSFW for camera 2"]},
    "Load NSFW model for camera 3": {"Success": ["Load NSFW model for camera 3 successfully"], "Failed": ["Failed to initialise NSFW for camera 3"]},
    "Load NSFW model for camera 4": {"Success": ["Load NSFW model for camera 4 successfully"], "Failed": ["Failed to initialise NSFW for camera 4"]},
    "Fortifai is running...": {"Success": ["Terminate Application: Set Exit Flag"], "Failed": []},
    "Fortifai is exiting...": {"Success": ["Fortifai stopped...", "Terminate Application: Force Interrupt"], "Failed": []}
})
STEPS_LIST = []
for key, value in STEPS.items():
    STEPS_LIST.extend([key, *value["Success"], *value["Failed"]])

# Status dictionary
STATUS = dict({})

INTERVAL_BETWEEN_2_UPDATES = 0.3 # seconds
terminated_flag = False

def clear_terminal():
    """Clear the terminal screen."""
    print("\033[2J\033[H", end="")


def display_status():
    """Display the current status of all steps."""
    if len(STEPS.items()) == 0:
        print("Waiting for aiserver to start...")

    # Print steps with "Success" or "Failed" or process icon
    for step, status in STATUS.items():
        if status == "[Success]":
            print(f"{step:<60} \033[92m{status}\033[0m")
        elif status == "[Failed]":
            print(f"{step:<60} \033[91m{status}\033[0m")
        elif status in ["[\\]", "[|]", "[/]", "[-]"]:
            print(f"{step:<60} \033[93m{status}\033[0m")

    time.sleep(0.1)

def update_status(line=""):
    global terminated_flag
    """Update the status of steps based on a log line."""
    for step, keywords in STEPS.items():
        success_keywords = keywords["Success"]
        failure_keywords = keywords["Failed"]

        # all(step not in line for step in STEPS_LIST):
        if any(kw in line for kw in success_keywords):
            STATUS[step] = "[Success]"
        if any(kw in line for kw in failure_keywords):
            STATUS[step] = "[Failed]"
        elif step in STATUS.keys():
            if STATUS[step] == "[\\]":
                STATUS[step] = "[|]"
            elif STATUS[step] == "[|]":
                STATUS[step] = "[/]"
            elif STATUS[step] == "[/]":
                STATUS[step] = "[-]"
            elif STATUS[step] == "[-]":
                STATUS[step] = "[\\]"
        elif step in line:
            STATUS[step] = "[\\]"

        if ("Fortifai is exiting..." == step) and ((STATUS.get(step, "") == "[Success]") or (STATUS.get(step) == "[Failed]")):
            terminated_flag = True

def monitor_log_file(log_file):
    """Monitor the log file for updates."""
    while not terminated_flag:
        if os.path.exists(log_file):
            with open(log_file, "r") as file:
                time_epoch_last_update = time.time() - INTERVAL_BETWEEN_2_UPDATES # ensure update the first time
                while not terminated_flag:
                    line = file.readline().strip()

                    if not line:
                        time.sleep(0.1)
                        now = time.time()
                        if (now - time_epoch_last_update < INTERVAL_BETWEEN_2_UPDATES):
                            continue
                        time_epoch_last_update = now
                    elif all(step not in line for step in STEPS_LIST):
                        now = time.time()
                        if (now - time_epoch_last_update < INTERVAL_BETWEEN_2_UPDATES):
                            continue
                        time_epoch_last_update = now

                    update_status(line)
                    clear_terminal()
                    display_status()

    os.remove(log_file)

if __name__ == "__main__":
    try:
        monitor_log_file(LOG_FILE)
    except KeyboardInterrupt:
        pass
