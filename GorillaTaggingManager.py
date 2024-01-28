import os
import psutil
import pyttsx3
import requests
from zipfile import ZipFile
import subprocess
import time

def kill_running_processes(exe_name):
    for process in psutil.process_iter():
        try:
            if exe_name.lower() in process.name().lower():
                process.kill()
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass

def download_and_extract(url, destination):
    response = requests.get(url)
    if response.status_code == 200:
        with open("BepInEx.zip", "wb") as file:
            file.write(response.content)
        with ZipFile("BepInEx.zip", "r") as zip_ref:
            zip_ref.extractall(destination)
        os.remove("BepInEx.zip")

def search_and_create_folder(root_dir):
    found_gorilla_pc_files = False
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            if dirname == "Gorilla Tag":
                gorilla_tag_dir = os.path.join(dirpath, dirname)
                gorilla_pc_files_dir = os.path.join(gorilla_tag_dir, "GorillaPcFiles")
                kill_running_processes("GorillaTag.exe")
                os.makedirs(gorilla_pc_files_dir, exist_ok=True)
                found_gorilla_pc_files = True
                bepinex_url = "https://github.com/BepInEx/BepInEx/releases/download/v5.4.22/BepInEx_x64_5.4.22.0.zip"
                download_and_extract(bepinex_url, gorilla_tag_dir)
                caution_text = "CAUTION!! Not verified mods. Game may act unstable if used with outdated mods."
                with open(os.path.join(gorilla_pc_files_dir, "CAUTION.txt"), "w") as f:
                    f.write(caution_text)
                os.environ["GORILLA_TAG_DIRECTORY"] = gorilla_pc_files_dir
                break
        if found_gorilla_pc_files:
            break
    return found_gorilla_pc_files

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    use_saved_directory = input("Do you want to use the saved Gorilla Tag directory? (yes/no): ").lower()
    if use_saved_directory == "yes":
        saved_directory = os.environ.get("GORILLA_TAG_DIRECTORY")
        if saved_directory and os.path.exists(saved_directory):
            found_gorilla_tag = True
        else:
            found_gorilla_tag = False
    else:
        drives_to_check = ["C:/", "D:/"]
        found_gorilla_tag = False
        for drive in drives_to_check:
            if os.path.exists(drive):
                found = search_and_create_folder(drive)
                if found:
                    found_gorilla_tag = True
                    speak("Found the folder. Installing the items and mods..")
                    break
        if not found_gorilla_tag:
            speak("No Gorilla Tag folder found.")
    if found_gorilla_tag:
        subprocess.Popen(os.path.join(saved_directory, "GorillaTag.exe"))
        time.sleep(19)
        kill_running_processes("GorillaTag.exe")
