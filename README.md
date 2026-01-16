# DiscordRPCchanger
------Custom Activity for your Discord Profile------

## Project Structure

```
DiscordRPCchanger/
├── assets/              # Image resources (included in repository)
│   ├── background.jpg   # Background image for GUI
│   ├── icon.jpg         # System tray icon
│   ├── app_icon.jpg     # Application window icon
│   └── icon.ico         # Original icon file
├── DiscordRPCAppChanger.py    # Main application
├── DiscordRPCAppChanger.spec  # PyInstaller build configuration
├── create_assets.py     # Utility to generate image assets
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Building

To build the executable:
```bash
pyinstaller DiscordRPCAppChanger.spec
```

**Important:** After building, copy the `assets` folder to the `dist/` directory:
```bash
# Windows (PowerShell)
Copy-Item -Recurse assets dist/

# Linux/Mac
cp -r assets dist/
```

The final structure should be:
```
dist/
├── DiscordRPCAppChanger.exe
└── assets/
    ├── background.jpg
    ├── icon.jpg
    └── app_icon.jpg
```

## Customizing Images

You can replace images in the `dist/assets/` folder **without rebuilding** the application!
Just replace the files and restart the app. See `assets/README.md` for details.
