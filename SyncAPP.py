import os
import subprocess
from ftplib import FTP
import tkinter as tk
from tkinter import ttk,filedialog
import configparser
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"tkinter designs\build\assets\frame0")




def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# Load or create a configuration file
config = configparser.ConfigParser()
config_file_path = "config.ini"

if os.path.exists(config_file_path):
    config.read(config_file_path)

def sync_local():
    ftp_host = entry_ftp_host.get()
    ftp_username = entry_ftp_username.get()
    ftp_password = entry_ftp_password.get()
    local_folder_path = entry_local_folder_path.get()
    remote_folder_path = entry_remote_folder_path.get()

    sync_winscp_folders(ftp_host, ftp_username, ftp_password, local_folder_path, remote_folder_path, sync_mode="local")

def sync_remote():
    ftp_host = entry_ftp_host.get()
    ftp_username = entry_ftp_username.get()
    ftp_password = entry_ftp_password.get()
    local_folder_path = entry_local_folder_path.get()
    remote_folder_path = entry_remote_folder_path.get()

    sync_winscp_folders(ftp_host, ftp_username, ftp_password, local_folder_path, remote_folder_path, sync_mode="remote")

def sync_winscp_folders(host, username, password, local_path, remote_path, sync_mode):
    # Connect to the FTP server
    ftp = FTP(host)
    ftp.login(username, password)
    print("Connected to the FTP server.")

    # Create a temporary script file for WinSCP commands
    script_filename = "winscp_script.txt"
    with open(script_filename, "w") as script_file:
        script_file.write(f"option batch abort\n")
        script_file.write(f"option confirm off\n")
        script_file.write(f"open ftp://{username}:{password}@{host}\n")
        
        if sync_mode == "local":
            script_file.write(f"synchronize local -delete \"{local_path}\" \"{remote_path}\"\n")
        elif sync_mode == "remote":
            script_file.write(f"synchronize remote \"{local_path}\" \"{remote_path}\"\n")
        
        script_file.write(f"exit\n")

    # Execute WinSCP with the script file
    user_home = os.path.expanduser("~")
    winscp_path = os.path.join(user_home, "AppData", "Local", "Programs", "WinSCP", "WinSCP.exe")#if this doesnt work 
    #try the line down bellow 
    
    #winscp_path = r"C:\\Users\\R3i\\AppData\\Local\\Programs\\WinSCP\\WinSCP.exe"  # Replace with your WinSCP installation path
    try:
        subprocess.run([winscp_path, "/console", f"/script={os.path.abspath(script_filename)}"])
        print("Synchronization complete.")
    except Exception as e:
        print(f"Error synchronizing folders: {str(e)}")
    finally:
        # Clean up: remove the temporary script file
        os.remove(script_filename)

    # Close the FTP connection
    ftp.quit()






window = Tk()
window.title("FTP Sync")

window.geometry("774x470")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 470,
    width = 774,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    371.0,
    470.0,
    fill="#009DC0",
    outline="")


canvas.create_text(
    23.0,
    74.0,
    anchor="nw",
    text="Host name",
    fill="#FFFFFF",
    font=("Inter", 12 * -1)
)

canvas.create_text(
    231.0,
    72.0,
    anchor="nw",
    text="Port",
    fill="#FFFFFF",
    font=("Inter", 12 * -1)
)

canvas.create_text(
    183.0,
    126.0,
    anchor="nw",
    text="Password",
    fill="#FFFFFF",
    font=("Inter", 12 * -1)
)

canvas.create_text(
    24.0,
    126.0,
    anchor="nw",
    text="User Name",
    fill="#FFFFFF",
    font=("Inter", 12 * -1)
)

canvas.create_text(
    23.0,
    266.0,
    anchor="nw",
    text="Local Directory Path",
    fill="#FFFFFF",
    font=("Inter", 12 * -1)
)

canvas.create_text(
    24.0,
    328.0,
    anchor="nw",
    text="Remote Directory Path",
    fill="#FFFFFF",
    font=("Inter", 12 * -1)
)

canvas.create_text(
    132.0,
    11.0,
    anchor="nw",
    text="LogIn",
    fill="#FFFFFF",
    font=("Inter Bold", 20 * -1)
)

canvas.create_text(
    112.0,
    206.0,
    anchor="nw",
    text="Directories",
    fill="#FFFFFF",
    font=("Inter Bold", 20 * -1)
)


# Create labels and entry widgets for user input

#Hostname texbox
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    116.5,
    105.0,
    image=entry_image_1
)
entry_ftp_host = tk.Entry(bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_ftp_host.place(
    x=25.0,
    y=90.0,
    width=183.0,
    height=28.0
)
canvas.create_rectangle(
    227.0,
    90.0,
    299.0,
    120.0,
    fill="#FFFFFF",
    outline="")
#Username TextBox
entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    94.0,
    157.0,
    image=entry_image_2
)
entry_ftp_username = tk.Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_ftp_username.place(
    x=26.0,
    y=142.0,
    width=136.0,
    height=28.0
)
#password TextBox
entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    241.0,
    157.0,
    image=entry_image_3
)
entry_ftp_password = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    show="*"
)
entry_ftp_password.place(
    x=181.0,
    y=142.0,
    width=120.0,
    height=28.0
)
#local folder path TextBox
entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    132.5,
    297.0,
    image=entry_image_4
)
entry_local_folder_path = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_local_folder_path.place(
    x=26.0,
    y=282.0,
    width=213.0,
    height=28.0
)

#remote directory path textBox
entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    132.5,
    359.5,
    image=entry_image_5
)
entry_remote_folder_path = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_remote_folder_path.place(
    x=26.0,
    y=345.0,
    width=213.0,
    height=27.0
)
#function to browse the local folder we want to sync 
def browse_local_folder():
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        entry_local_folder_path.delete(0, tk.END)
        entry_local_folder_path.insert(0, selected_folder)
#Browse Button
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=browse_local_folder,
    relief="flat"
)
button_1.place(
    x=262.0,
    y=279.0,
    width=71.0,
    height=37.0
)

#function to save temporary the login and directoryes
def save_settings():
    config["Config"] = {
        "ftp_host": entry_ftp_host.get(),
        "ftp_username": entry_ftp_username.get(),
        "ftp_password": entry_ftp_password.get(),
        "local_folder_path": entry_local_folder_path.get(),
        "remote_folder_path": entry_remote_folder_path.get()
    }

    with open(config_file_path, "w") as config_file:
        config.write(config_file)

#Save Button
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=save_settings,
    relief="flat"
)
button_2.place(
    x=139.0,
    y=416.0,
    width=71.0,
    height=37.0
)
# Sync Local Button
button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=sync_local,
    relief="flat"
)
button_3.place(
    x=513.0,
    y=131.0,
    width=164.0,
    height=55.71429443359375
)
#Sync Remote Button
button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=sync_remote,
    relief="flat"
)
button_4.place(
    x=513.0,
    y=255.0,
    width=164.0,
    height=55.71429443359375
)

canvas.create_text(
    231.0,
    96.0,
    anchor="nw",
    text="21",
    fill="#A0A0A0",
    font=("Inter", 16 * -1)
)



# Run the Tkinter main loop
if "Config" in config:
    if "ftp_host" in config["Config"]:
        entry_ftp_host.insert(0, config["Config"]["ftp_host"])
    if "ftp_username" in config["Config"]:
        entry_ftp_username.insert(0, config["Config"]["ftp_username"])
    if "ftp_password" in config["Config"]:
        entry_ftp_password.insert(0, config["Config"]["ftp_password"])
    if "local_folder_path" in config["Config"]:
        entry_local_folder_path.insert(0, config["Config"]["local_folder_path"])
    if "remote_folder_path" in config["Config"]:
        entry_remote_folder_path.insert(0, config["Config"]["remote_folder_path"])


icon_path = "sync1.ico"
window.wm_iconbitmap(icon_path)


window.resizable(False, False)  # Prevent window from being resizable
# Run the Tkinter main loop
window.mainloop()