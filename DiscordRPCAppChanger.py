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
    """Скрыть консольное окно"""
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    hwnd = kernel32.GetConsoleWindow()
    if hwnd:
        user32.ShowWindow(hwnd, 0)

def show_console():
    """Показать консольное окно"""
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    hwnd = kernel32.GetConsoleWindow()
    if hwnd:
        user32.ShowWindow(hwnd, 5)

def create_image():
    """Создать иконку для трея"""
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color='#5865F2')
    dc = ImageDraw.Draw(image)
    dc.rectangle([width // 4, height // 4, 3 * width // 4, 3 * height // 4], fill='white')
    return image

def on_quit(icon, item):
    """Выход из приложения"""
    icon.stop()
    exit()

def run_tray_icon():
    """Запустить иконку в трее"""
    icon = pystray.Icon(
        "Discord RPC",
        create_image(),
        "Discord RPC Manager",
        menu=pystray.Menu(
            pystray.MenuItem("Exit", on_quit)
        )
    )
    icon.run()

def main():
    current_rpc = None
    print("🔥 Hotkey RPC is running")
    print("Ctrl+Alt+C = Clear")
    print("Already complete, Happy Changering")
    print("\nПриложение сворачивается в трей через 3 секунды...")
    
    time.sleep(3)
    
    # Запустить RPC
    current_rpc = custom_rpc()
    
    # Скрыть консоль
    hide_console()
    
    # Запустить иконку в трее в отдельном потоке
    tray_thread = threading.Thread(target=run_tray_icon, daemon=True)
    tray_thread.start()

    while True:
        try:
            if keyboard.is_pressed("ctrl+alt+c"):
                clear_rpc(current_rpc)
                current_rpc = None
                time.sleep(0.5)

            time.sleep(0.05)

        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
