from datetime import datetime
from hashlib import sha256
from os import walk
from os.path import join
from cryptography.fernet import Fernet
import base64
import subprocess
import socket
from mimetypes import guess_type
from flask import Response
from base64 import b64decode
from io import BytesIO


global session_list
session_list = {}

class gen:
    @staticmethod
    def generate(text):
        output = util.run_command(f"./gen/gen_new_method --password {text}")
        return output
class server:
    def serve_file(fernet,file_name):
        fernet = fernet.encode()
        try:
            # Ensure the file name starts with "/"
            if not file_name.startswith("/"):
                file_name = "/" + file_name
            
            # Decode the file content
            img_data = b64decode(crypt.decrypt_file_return_string_base64_local(file_name,fernet))
            
            # Determine MIME type based on the file name
            mime_type, _ = guess_type(file_name)
            if mime_type is None:
                mime_type = "application/octet-stream"  # Fallback MIME type

            # Return the decoded binary data as a Flask response
            return Response(BytesIO(img_data), mimetype=mime_type)
        except Exception as e:
            # Handle errors gracefully
            return Response(f"Error serving file: {str(e)}", status=500)   
class crypt:
    @staticmethod
    def sha256(hash_string):
        try:
            return sha256(hash_string.encode()).hexdigest()
        except Exception as e:
            print(f"Error in encrypt.string: {e}")
            return None
        
    @staticmethod
    def encrypt_file(path,fernet):
        try:
            with open(path, 'rb') as file:
                first = file.read()
            encrypted = fernet.encrypt(first)
            with open(path, 'wb') as file:
                file.write(encrypted)
            print(f"encrypted: {path}")
        except Exception as e:
            print(f"Error encrypting file {path}: {e}")

    @staticmethod
    def decrypt_file(path,fernet):
        try:
            with open(path, 'rb') as file:
                first = file.read()
            decrypted = fernet.decrypt(first)
            with open(path, 'wb') as file:
                file.write(decrypted)
            print(f"decrypted: {path}")
        except Exception as e:
            print(f"Error decrypting file {path}: {e}")

    @staticmethod
    def encrypt_directory(path,fernet):
        for root, _, files in walk(path):
            for file in files:
                crypt.encrypt_file(join(root, file))
    
    @staticmethod
    def decrypt_directory(path,fernet):
        for root, _, files in walk(path):
            for file in files:
                crypt.decrypt_file(join(root, file))

    @staticmethod
    def decrypt_file_return_string(path,fernet):
        try:
            with open(path, 'rb') as file:
                first = file.read()
            decrypted = fernet.decrypt(first)
            print(f"decrypted: {path}")
            return decrypted
        except Exception as e:
            print(f"Error decrypting file {path}: {e}")
            return None

    @staticmethod
    def encrypt_string_return_string(string,fernet):
        try:
            return fernet.encrypt(string.encode())
        except Exception as e:
            print(f"Error encrypting string: {e}")
            return None
        
    @staticmethod
    def decrypt_string_return_string(string,fernet):
        try:
            return fernet.decrypt(string.decrypt())
        except Exception as e:
            print(f"Error decrypting string: {e}")
            return None
        
    @staticmethod
    def decrypt_file_return_string_base64(path,fernet):
        try:
            with open(path, 'rb') as file:
                first = file.read()
            decrypted = fernet.decrypt(first)
            base64_string = base64.b64encode(decrypted).decode("utf-8")
            print(f"decrypted: {path}")
            return base64_string
        except Exception as e:
            print(f"Error in decrypt_file_return_string_base64: {e}")
            return None
    
    @staticmethod
    def decrypt_file_return_string_base64_local(path,fernet):
        try:
            with open(path, 'rb') as file:
                first = file.read()
            decrypted = fernet.decrypt(first)
            base64_string = base64.b64encode(decrypted).decode("utf-8")
            print(f"decrypted: {path}")
            return base64_string
        except Exception as e:
            print(f"Error in decrypt_file_return_string_base64: {e}")
            return None
class util:

    @staticmethod
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
        

    @staticmethod
    def get_ping():
        try:
            result = subprocess.run(['ping', '-c', '1', socket.gethostbyname(socket.gethostname())], capture_output=True, text=True, timeout=10)
            ping_time = result.stdout.split("time=")[1].split(" ")[0]
            return str(ping_time)
        except (IndexError, subprocess.TimeoutExpired):
            return None
    @staticmethod
    def decode_url_friendly(encoded_phrase):
        padding = '=' * (-len(encoded_phrase) % 4)
        base64_bytes = encoded_phrase + padding
        phrase_bytes = base64.urlsafe_b64decode(base64_bytes)
        return phrase_bytes.decode('utf-8')
    @staticmethod
    def make_url_friendly(phrase):
        phrase_bytes = phrase.encode('utf-8')
        base64_bytes = base64.urlsafe_b64encode(phrase_bytes)
        return base64_bytes.decode('utf-8').rstrip("=")
class Session:
    @staticmethod
    def hasExpired(name):
        hashed_name = crypt.sha256(name)
        if hashed_name in session_list:
            stored_date = datetime.strptime(session_list[hashed_name]["date"], '%d-%m-%Y %H:%M:%S')
            difference = (datetime.now() - stored_date).total_seconds() / 60
            print(difference)
            return difference >= session_list[hashed_name]["timeout"]
        return True  # Assume expired if session doesn't exist

    @staticmethod
    def Query(name, item):
        hashed_name = crypt.sha256(name)
        if hashed_name in session_list:
            return session_list[hashed_name].get(item, False)
        return False

    @staticmethod
    def Exists(name):
        return crypt.sha256(name) in session_list

    @staticmethod
    def Print(name):
        hashed_name = crypt.sha256(name)
        if hashed_name in session_list:
            print(f"{name} found in {hashed_name}")
            print("{")
            for key, value in session_list[hashed_name].items():
                print(f"    {key}: {value},")
            print("}")
        else:
            print(f"{name} not found.")

    @staticmethod
    def New(name, fernet, reason, timeout=60):
        hashed_name = crypt.sha256(name)
        if hashed_name not in session_list:
            session_list[hashed_name] = {
                "timeout": timeout,
                "fernet": fernet,
                "reason": reason,
                "date": datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            }
            return True
        return False
    
    @staticmethod
    def Remove(name):
        session_list.pop(crypt.sha256(name))

    @staticmethod
    def PrintAll():
        print(session_list)




































import flask # I know dupe but idc
import flask_cors
import sys 
import io

# Custom stream class that writes to both the terminal and a buffer
class DualStream(io.TextIOBase):
    def __init__(self, original_stream):
        self.terminal = original_stream  # Original stdout/stderr
        self.log_buffer = io.StringIO()  # Log buffer

    def write(self, message):
        self.terminal.write(message)  # Print to terminal
        self.terminal.flush()
        self.log_buffer.write(message)  # Store in buffer

    def flush(self):
        self.terminal.flush()
        self.log_buffer.flush()

    def get_logs(self):
        return self.log_buffer.getvalue()

# Replace stdout & stderr with our dual stream
dual_stream = DualStream(sys.stdout)
sys.stdout = dual_stream
sys.stderr = dual_stream  # Capture errors too


app = flask.Flask(__name__)
flask_cors.CORS(app)

@app.route("/logs")
def get_logs():
    return Response(dual_stream.get_logs(), mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=False,threaded=True,host="0.0.0.0")
