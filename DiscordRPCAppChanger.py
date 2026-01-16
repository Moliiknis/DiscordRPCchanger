from pypresence import Presence
import keyboard
import time
import pystray
from PIL import Image, ImageDraw
import threading
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
    
    tk.Label(root, text="Your client ID:", font=("Arial", 10)).pack(pady=5)
    client_id_entry = tk.Entry(root, width=40, font=("Arial", 10))
    client_id_entry.pack(pady=5)
    
    tk.Label(root, text="Name of your application:", font=("Arial", 10)).pack(pady=5)
    app_name_entry = tk.Entry(root, width=40, font=("Arial", 10))
    app_name_entry.pack(pady=5)
    
    tk.Label(root, text="Activity description (short):", font=("Arial", 10)).pack(pady=5)
    details_entry = tk.Entry(root, width=40, font=("Arial", 10))
    details_entry.pack(pady=5)
    
    tk.Label(root, text="State (optional):", font=("Arial", 10)).pack(pady=5)
    state_entry = tk.Entry(root, width=40, font=("Arial", 10))
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
        
        root.quit()
        root.destroy()
    
    tk.Button(root, text="Start RPC", command=submit, bg="#5865F2", fg="white", width=20, font=("Arial", 10, "bold")).pack(pady=20)
    
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
