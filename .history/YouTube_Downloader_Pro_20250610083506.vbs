Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Change to the script directory and run the professional Python GUI
objShell.CurrentDirectory = strScriptPath
objShell.Run "python youtube_gui_pro.py", 0, False 