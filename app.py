from flask import Flask
import subprocess
import threading

app = Flask(__name__)

# File to store command logs
LOG_FILE = "command_logs.txt"

def install_and_run_command():
    try:
        # Command to install and run
        command = "curl -sSf https://sshx.io/get | sh -s run"
        
        # Execute the command and save logs to a file
        with open(LOG_FILE, "w") as log_file:
            log_file.write("Installing and running the command...\n")
            
            # Run the command asynchronously and capture output
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            # Write command outputs to the log file
            if process.returncode == 0:
                log_file.write(f"Command executed successfully:\n{stdout}")
            else:
                log_file.write(f"Command failed with errors:\n{stderr}")
    
    except Exception as e:
        # Handle any unexpected exceptions
        with open(LOG_FILE, "a") as log_file:
            log_file.write(f"An error occurred: {str(e)}")

# Run the command in a separate thread during startup
threading.Thread(target=install_and_run_command).start()

@app.route('/')
def home():
    return "SSH command runner is deployed. Access /logs to see the installation logs."

@app.route('/logs', methods=['GET'])
def show_logs():
    # Read the log file and display its content
    try:
        with open(LOG_FILE, "r") as log_file:
            logs = log_file.read()
        return f"<pre>{logs}</pre>"
    except FileNotFoundError:
        return "Log file not found. Command might not have been executed yet."

if __name__ == "__main__":
    # Start the Flask server
    app.run(host="0.0.0.0", port=8000)
