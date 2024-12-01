import subprocess
def run_command(command):
    try:
        # Run the command and capture the output
        result = subprocess.run(
            command, shell=True, text=True, capture_output=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        # Handle errors during command execution
        return f"Error: {e.stderr}"
    




def generate_key(text):
    output = run_command(f"./gen/gen_new_method --password {text}")
    return output