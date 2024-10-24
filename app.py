from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return "SSH command runner. Access /run to execute the command."

@app.route('/run', methods=['GET'])
def run_command():
    try:
        # Command to run
        command = "curl -sSf https://sshx.io/get | sh -s run"

        # Execute the command
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return f"Command executed successfully: {result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"Command failed: {e.stderr}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
