# BeamNG-CareerMoneyEditor

This tool was made because in BeamNG.drive career mode, you often end up accidentally hitting curbs or scraping the ground all the time. This causes minor damage, and you can’t do anything in the garage without repairing it first. That costs alot of money over time.

I got tired of it and thought: "Why not make a tool that just adds that $1500 back into BeamNG?" 

This is a simple solution that modifies your save files directly. It would be even cooler to build something that edits BeamNG’s memory in real-time, but I’m not there yet. For now, this gets the job done.

## How it works!

This tool modifies your BeamNG.drive career save files to change your in-game money. Here’s the basic flow:

1. **Find BeamNG Installation**  
   It automatically searches your `LOCALAPPDATA` directory to detect which version of BeamNG.drive you're using.

2. **List Available Saves**  
   It locates your career saves by scanning BeamNG’s `settings/cloud/saves` directory.

3. **Let You Pick a Save**  
   The tool lists all your available saves and asks you to pick which one you want to modify.

4. **Find The Latest Autosave**  
   Inside the selected save, it looks for the latest autosave folder by checking which one has the most recently modified `playerAttributes.json` file.

5. **Edit Your Money**  
   Once the file is found, you’re given 3 options:
   - Press **Enter** to simply add $1500 (default option)
   - Choose **1** to add or subtract a custom amount
   - Choose **2** to directly set your money to a specific value

6. **Save Changes**  
   The modified money value is written back to your save file. It double-checks that the file was updated correctly and reports success or failure.

⚠ **Note:** BeamNG.drive must be closed while you run the tool, or the save file may be locked and changes won’t apply.
