import subprocess

# Command to run
command = "curl -sSf https://sshx.io/get | sh -s run"

# Execute the command
subprocess.run(command, shell=True, check=True)