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

The `assets` folder will be automatically included in the build.
