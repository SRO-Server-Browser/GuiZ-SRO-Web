# GuiZ-SRO-Web

A lightweight web-based GUI overlay for Silkroad Online, toggled with the `Z` key. Displays a web interface (`https://www.example.com`) on top of the game while keeping game focus. Launched via a DLL injected into `sro_client.exe`.

## Features
- Toggle web GUI with `Z` key.
- GUI stays on top without stealing game focus.
- Closing the window (`X`) hides the GUI instead of exiting.
- DLL automatically starts/stops the GUI with `sro_client.exe`.

## Repository Structure
- **Dll/**: Contains `DllMain.cpp` (source) and `GuiZ.dll` (compiled DLL).
- **GuiZ/**: Contains `GuiZ.py` (Python source), a precompiled `GuiZ.exe` (via PyInstaller), and a zipped `GuiZ.zip` with the executable.

## Requirements
- Windows 10/11
- Python 3.10+ (for compiling `GuiZ.py`)
- Visual Studio (for compiling `DllMain.cpp`)
- Silkroad Online client (`sro_client.exe`)

## Installation
1. **Extract Files**:
   - Place `GuiZ.dll` and `GuiZ.exe` in `C:\Test\`.

2. **Configure Game Window Title**:
   - Update `GuiZ.py`’s `FindWindowW(None, "client")` with `sro_client.exe`’s window title (e.g., "Silkroad Online").
   - Recompile `GuiZ.py` if needed:
     ```bash
     pip install PyQt5 PyQtWebEngine pyinstaller
     pyinstaller --onefile GuiZ.py
     ```

3. **Run**:
   - Inject `GuiZ.dll` using StudPE or another injector.
   - Put same folder `GuiZ.dll` & `GuiZ.exe` & `sro_client.exe`
   - Run `sro_client.exe`.
   - Press `Z` to toggle the GUI.

## Notes
- Run `silkroad.exe` as administrator if `Z` key detection fails.
- Ensure internet access for the web GUI.
- Logs are written to the system temp directory (`guiZ_log.txt`).

## License
MIT License
