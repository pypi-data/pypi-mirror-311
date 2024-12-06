import subprocess
import sys
from pathlib import Path
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from update_checker import update_check
import importlib.metadata
import threading
import time

## Check for updates
def check_package_update(package_name):
    try:
        # Get the currently installed version
        installed_version = importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        return f"{package_name} is not installed."

    # Check for updates
    res = update_check(package_name, installed_version)
    if res:
        return f"New version of {package_name} is available: {res['latest_version']} (Installed: {installed_version})"
    else:
        return f"{package_name} is up to date (Version: {installed_version})."

# Function to select a folder
def select_folder():
    global path_to_outdirs
    new_folder = filedialog.askdirectory(title="Select the projects folder")
    if new_folder:
        path_to_outdirs = new_folder
        folder_label.config(text=f"Selected Folder: {path_to_outdirs}")
    else:
        folder_label.config(text=f"Using previous folder: {path_to_outdirs}")

# Function to run the Streamlit app
def run_streamlit_app():
    try:
        print('Press CTRL + C to close APSCALE!')
        subprocess.call(['streamlit', 'run', './taxontabletools_2.0.py', '--theme.base', 'light' ])
    except KeyboardInterrupt:
        sys.exit()

# Function to close the tkinter app and continue with the script
def start_app():
    if not path_to_outdirs:
        messagebox.showwarning("Warning", "Please select a projects folder before continuing.")
        return

    # Save the selected folder to user_preferences.xlsx
    save_folder_to_preferences()

    # Hide window
    root.withdraw()

    # Run the Streamlit app in a new thread to avoid freezing the GUI
    threading.Thread(target=run_streamlit_app).start()

# Function to save the selected folder to the preferences file
def save_folder_to_preferences():
    user_preferences_df.loc[user_preferences_df['Variable'] == 'path_to_outdirs', 'Value'] = path_to_outdirs
    user_preferences_df.to_excel(user_preferences_xlsx, index=False)

# Tkinter window setup
root = tk.Tk()
root.title("TaxonTableTools Start Window")
root.geometry("400x200")

# Check for APSCALE package update
update_info = check_package_update('taxontabletools')

# Update label
update_label = tk.Label(root, text=update_info, wraplength=300, justify="left")
update_label.pack(pady=10)

# Paths and user preferences setup
path_to_ttt = Path(__file__).resolve().parent
user_preferences_xlsx = path_to_ttt.joinpath('user_preferences.xlsx')

# Read user preferences from the file
user_preferences_df = pd.read_excel(user_preferences_xlsx).fillna('')
path_to_outdirs = user_preferences_df.loc[user_preferences_df['Variable'] == 'path_to_outdirs', 'Value'].values[0]

# Display the current folder
folder_label = tk.Label(root, text=f"Current folder: {path_to_outdirs if path_to_outdirs else 'No folder selected'}")
folder_label.pack(pady=10)

# Button to select a new folder
select_button = tk.Button(root, text="Select Projects Folder", command=select_folder)
select_button.pack(pady=10)

# Start button to continue with the script
start_button = tk.Button(root, text="Start", command=start_app)
start_button.pack(pady=10)

# Run tkinter main loop
root.mainloop()