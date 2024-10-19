import subprocess
import os

root_dir = os.getcwd()

f = open(root_dir + '/worker_tracker.txt', 'r+')
f.truncate(0)

# Define the two scripts
download_script = root_dir + "/download.py"
process_script = root_dir + "/train.py"

# Start both scripts in parallel using subprocess
download_process = subprocess.Popen(['python3', download_script])
process_process = subprocess.Popen(['python3', process_script])

# Wait for both to complete
download_process.wait()
process_process.wait()