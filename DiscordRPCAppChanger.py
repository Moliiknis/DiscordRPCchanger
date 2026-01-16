from pypresence import Presence
import keyboard
import time
import pystray
from PIL import Image, ImageDraw
import threading
import ctypes
import tkinter as tk
from tkinter import messagebox

# Global variables for user input
client_id_from_user = ""
user_app_name = ""
details_from_user = ""
state_user = ""

def get_user_input():
    """Create a simple GUI window to get user input"""
    global client_id_from_user, user_app_name, details_from_user, state_user
    
    root = tk.Tk()
    root.title("Discord RPC Setup")
    root.geometry("400x300")
    root.resizable(False, False)
    
    # Center window
    root.eval('tk::PlaceWindow . center')
    
    tk.Label(root, text="Your client ID:").pack(pady=5)
    client_id_entry = tk.Entry(root, width=50)
    client_id_entry.pack(pady=5)
    
    tk.Label(root, text="Name of your application:").pack(pady=5)
    app_name_entry = tk.Entry(root, width=50)
    app_name_entry.pack(pady=5)
    
    tk.Label(root, text="Activity description (short):").pack(pady=5)
    details_entry = tk.Entry(root, width=50)
    details_entry.pack(pady=5)
    
    tk.Label(root, text="State (optional):").pack(pady=5)
    state_entry = tk.Entry(root, width=50)
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
        
        root.destroy()
    
    tk.Button(root, text="Start RPC", command=submit, bg="#5865F2", fg="white", width=20).pack(pady=20)
    
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
        print("[RPC] is ready to use")
        return RPC

    except Exception as e:
        print("error RPC:", e)

# --- clear RPC ---
def clear_rpc(current):
    try:
        if current:
            current.clear()
            current.close()
        print("[RPC] is clear")
    except:
        pass


# --- main  ---
def create_image():
    """Make an icon image for the system tray"""
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
    # Get user input via GUI
    get_user_input()
    
    # Start RPC
    current_rpc = custom_rpc()
    
    # RPC reference for tray icon
    rpc_ref = [current_rpc]
    
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
    
    # Run the system tray icon in main thread (blocking)
    run_tray_icon(rpc_ref)


if __name__ == "__main__":
    main()
