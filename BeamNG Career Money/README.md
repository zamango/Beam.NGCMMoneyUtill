## Internal Overview

### Technologies & Modules Used

- **pathlib**  
  Handles all file and directory paths in a clean, OS-independent way. Makes navigating BeamNG's save structure easier.

- **re (Regex)**  
  Used to detect and parse BeamNG version folders (like `0.31.5`) from directory names.

- **json**  
  Reads and writes the `playerAttributes.json` file, where BeamNG stores your in-game money value.

- **os**  
  Gets environment variables (like `LOCALAPPDATA`) and uses `os.path.getmtime()` to fetch file modification times.

- **time**  
  Adds small delays to improve user experience and give time for warning messages.

- **sys.exit()**  
  Cleanly exits the script when critical failures happen (e.g. no BeamNG install found, no saves found, etc).

- **typing.Optional**  
  Provides type hinting for return values that may be `None` (e.g. when files or directories aren't found).

---

### Core Logic Breakdown

- **BeamNG Version Detection:**  
  The tool looks inside `LOCALAPPDATA/BeamNG.drive` for version folders. It uses regex to sort through version names and pick the latest one based on version numbers.

- **Save Discovery:**  
  After finding the active version, it scans the `settings/cloud/saves` directory to list all available saves.

- **Autosave Selection:**  
  Inside your chosen save, it looks for autosave folders. It checks which autosave has the most recently modified `playerAttributes.json` using file modification timestamps (`os.path.getmtime`).

- **Money Modification:**  
  - Loads the JSON file into a dictionary.
  - Reads the `money["value"]` key.
  - Lets the user pick how to modify the value (default add, custom add/subtract, or absolute set).
  - Updates the value and writes it back to disk.

- **Validation:**  
  After writing, it reloads the file to verify that the value was actually updated.

---

### Error Handling

- Uses `try/except` blocks throughout the code to safely handle:
  - Missing directories
  - Locked or open files
  - Permission errors
  - Invalid user input

- If something fails at any stage, the tool prints an error message and exits gracefully.

