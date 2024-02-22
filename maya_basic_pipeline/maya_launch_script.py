import subprocess

# Correctly format the path to the batch file for Windows
batch_file_path = 'E:\\launch_maya.bat'

# Use subprocess to call the batch file with the corrected path
subprocess.call(['cmd.exe', '/C', batch_file_path])