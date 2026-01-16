from pypresence import Presence
import keyboard
import time
import pystray
from PIL import Image, ImageDraw
import threading
import ctypes

# --- custom RPC ---
print("Your client id:")
client_id_from_user = input()
print("Name of your application:")
user_app_name = input()
print("Write a description of your activity (preferably short)<3:")
details_from_user = input()
print("Add state if you want:")
state_user = input()


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
def hide_console():
    """Hide console window"""
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    hwnd = kernel32.GetConsoleWindow()
    if hwnd:
        user32.ShowWindow(hwnd, 0)

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
    print("🔥 Discord RPC is starting...")
    print("Enter your details below:")
    
    # Start RPC
    current_rpc = custom_rpc()
    
    print("\n✅ RPC is active! Minimizing to tray...")
    print("Ctrl+Alt+C = Clear RPC")
    time.sleep(2)
    
    # Hide console window
    hide_console()
    
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
