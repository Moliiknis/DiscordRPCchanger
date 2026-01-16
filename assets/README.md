# Image Replacement

You can easily replace application images **without rebuilding**!

## How It Works

The application automatically loads images from the `assets` folder, which should be located next to the executable file.

## Step 1: Locate the assets Folder

After building the application, the structure should look like this:
```
dist/
├── DiscordRPCAppChanger.exe
└── assets/
    ├── background.jpg
    ├── icon.jpg
    └── app_icon.jpg
```

**Important:** Copy the `assets` folder from the project root to the `dist/` folder next to the `.exe` file!

## Step 2: Replace Images

Simply replace the files in the `assets/` folder:
- `background.jpg` - background image for GUI (recommended size: 800x600)
- `icon.jpg` - system tray icon (recommended size: 256x256)
- `app_icon.jpg` - application window icon (recommended size: 64x64)

## Step 3: Run the Application

Launch `DiscordRPCAppChanger.exe` - new images will load automatically!

**No rebuild required!** 🎉

## Note

- Use JPG format for compatibility
- Make sure file names match exactly
- The `assets` folder must be in the same directory as the `.exe` file
