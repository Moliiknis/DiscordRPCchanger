from pypresence import Presence
import keyboard
import time
import pystray
from PIL import Image, ImageDraw, ImageTk
import threading
import tkinter as tk
from tkinter import messagebox
import json
import os
import sys

# Config file to save user data
CONFIG_FILE = "rpc_config.json"

# Global variables for user input
client_id_from_user = ""
user_app_name = ""
details_from_user = ""
state_user = ""

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Paths to images (using relative paths)
BACKGROUND_IMAGE = get_resource_path(os.path.join("assets", "background.jpg"))
ICON_IMAGE = get_resource_path(os.path.join("assets", "icon.jpg"))
APP_ICON = get_resource_path(os.path.join("assets", "app_icon.jpg"))

def load_config():
    """Load saved configuration"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_config(config):
    """Save configuration"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    except:
        pass

def get_user_input():
    """Create a simple GUI window to get user input"""
    global client_id_from_user, user_app_name, details_from_user, state_user
    
    # Load saved config
    config = load_config()
    
    root = tk.Tk()
    root.title("Discord RPC Setup")
    root.geometry("800x600")
    root.resizable(False, False)
    
    # Center window
    root.eval('tk::PlaceWindow . center')
    
    # Try to set window icon
    try:
        if os.path.exists(APP_ICON):
            icon_img = Image.open(APP_ICON)
            icon_img = icon_img.resize((32, 32), Image.Resampling.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_img)
            root.iconphoto(True, icon_photo)
    except:
        pass
    
    # Try to set background image
    try:
        if os.path.exists(BACKGROUND_IMAGE):
            bg_image = Image.open(BACKGROUND_IMAGE)
            bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)
            bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(root, image=bg_photo)
            bg_label.image = bg_photo
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except:
        root.configure(bg='#2C2F33')
    
    # Create main frame with transparency
    main_frame = tk.Frame(root, bg='#2C2F33')
    main_frame.place(relx=0.5, rely=0.5, anchor='center')
    
    # Title
    title_label = tk.Label(main_frame, text="Discord RPC Setup", 
                           font=("Arial", 16, "bold"), 
                           bg='#2C2F33', fg='#FFFFFF')
    title_label.pack(pady=15)
    
    # Client ID
    tk.Label(main_frame, text="Your client ID:", 
             font=("Arial", 11), bg='#2C2F33', fg='#B9BBBE').pack(pady=5)
    client_id_entry = tk.Entry(main_frame, width=35, font=("Arial", 11), 
                               bg='#40444B', fg='#FFFFFF', 
                               insertbackground='white', relief='flat', bd=5)
    client_id_entry.insert(0, config.get('client_id', ''))
    client_id_entry.pack(pady=5)
    
    # App Name
    tk.Label(main_frame, text="Name of your application:", 
             font=("Arial", 11), bg='#2C2F33', fg='#B9BBBE').pack(pady=5)
    app_name_entry = tk.Entry(main_frame, width=35, font=("Arial", 11), 
                              bg='#40444B', fg='#FFFFFF', 
                              insertbackground='white', relief='flat', bd=5)
    app_name_entry.insert(0, config.get('app_name', ''))
    app_name_entry.pack(pady=5)
    
    # Details
    tk.Label(main_frame, text="Activity description (short):", 
             font=("Arial", 11), bg='#2C2F33', fg='#B9BBBE').pack(pady=5)
    details_entry = tk.Entry(main_frame, width=35, font=("Arial", 11), 
                            bg='#40444B', fg='#FFFFFF', 
                            insertbackground='white', relief='flat', bd=5)
    details_entry.insert(0, config.get('details', ''))
    details_entry.pack(pady=5)
    
    # State
    tk.Label(main_frame, text="State (optional):", 
             font=("Arial", 11), bg='#2C2F33', fg='#B9BBBE').pack(pady=5)
    state_entry = tk.Entry(main_frame, width=35, font=("Arial", 11), 
                          bg='#40444B', fg='#FFFFFF', 
                          insertbackground='white', relief='flat', bd=5)
    state_entry.insert(0, config.get('state', ''))
    state_entry.pack(pady=5)
    
    def submit():
        global client_id_from_user, user_app_name, details_from_user, state_user
        client_id_from_user = client_id_entry.get()
        user_app_name = app_name_entry.get()
        details_from_user = details_entry.get()
        state_user = state_entry.get()
        
        if not client_id_from_user:
            messagebox.showerror("Error", "Client ID is required!")
            return
        
        # Save config
        save_config({
            'client_id': client_id_from_user,
            'app_name': user_app_name,
            'details': details_from_user,
            'state': state_user
        })
        
        root.quit()
        root.destroy()
    
    # Submit button with rounded corners effect
    submit_btn = tk.Button(main_frame, text="Start RPC", command=submit, 
                          bg="#5865F2", fg="white", width=25, height=2,
                          font=("Arial", 12, "bold"), 
                          relief='flat', bd=0,
                          activebackground="#4752C4",
                          activeforeground="white",
                          cursor="hand2")
    submit_btn.pack(pady=25)
    
    root.mainloop()


def custom_rpc():
    try:
        client_id = client_id_from_user
        RPC = Presence(client_id)
        RPC.connect()

        RPC.update(
            name= user_app_name,
            details= details_from_user,
            state= state_user
        )
        return RPC

    except Exception as e:
        messagebox.showerror("RPC Error", f"Failed to connect: {e}")
        return None

# --- clear RPC ---
def clear_rpc(current):
    try:
        if current:
            current.clear()
            current.close()
    except:
        pass


# --- main  ---
def create_image():
    """Make an icon image for the system tray"""
    try:
        # Try to load custom icon
        if os.path.exists(ICON_IMAGE):
            icon = Image.open(ICON_IMAGE)
            icon = icon.resize((64, 64), Image.Resampling.LANCZOS)
            return icon
    except:
        pass
    
    # Fallback to generated icon
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color='#5865F2')
    dc = ImageDraw.Draw(image)
    dc.rectangle([width // 4, height // 4, 3 * width // 4, 3 * height // 4], fill='white')
    return image

def on_quit(icon, item):
    """Exit the application"""
    icon.stop()
    exit()

def run_tray_icon(rpc_ref):
    """Run the system tray icon"""
    def on_clear(icon, item):
        """Clear RPC"""
        clear_rpc(rpc_ref[0])
        rpc_ref[0] = None
    
    icon = pystray.Icon(
        "Discord RPC",
        create_image(),
        "Discord RPC Manager",
        menu=pystray.Menu(
            pystray.MenuItem("Clear RPC", on_clear),
            pystray.MenuItem("Exit", on_quit)
        )
    )
    icon.run()

def main():
    # Create tray icon reference
    rpc_ref = [None]
    
    # Start tray icon in background thread FIRST
    def start_tray():
        run_tray_icon(rpc_ref)
    
    tray_thread = threading.Thread(target=start_tray, daemon=False)
    tray_thread.start()
    
    # Small delay to ensure tray starts
    time.sleep(0.5)
    
    # Get user input via GUI window
    get_user_input()
    
    # Start RPC
    current_rpc = custom_rpc()
    
    if not current_rpc:
        return
    
    # Update RPC reference
    rpc_ref[0] = current_rpc
    
    # Run keyboard listener in a separate thread
    def keyboard_listener():
        while True:
            try:
                if keyboard.is_pressed("ctrl+alt+c"):
                    clear_rpc(rpc_ref[0])
                    rpc_ref[0] = None
                    time.sleep(0.5)
                time.sleep(0.05)
            except:
                break
    
    listener_thread = threading.Thread(target=keyboard_listener, daemon=True)
    listener_thread.start()
    
    # Keep main thread alive
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
