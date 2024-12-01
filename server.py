import flask
import flask_cors
from modules.encrypt import encrypt_string, decrypt_file_return_string_base64, set_key
from modules.gen import generate_key
import subprocess
import socket
import time
import psutil
import os

# default website
# files call
# server status call
# password enc call
# shutdown call

port = 4040
server_password = "password123"
file_dir = "/home/_3hy/Pictures/background_lowres/.backgrounds/.weird/"
app = flask.Flask(__name__)
CORS = flask_cors.CORS(app)
key = encrypt_string(server_password)


def get_ping():
    try:
        result = subprocess.run(['ping', '-c', '1', socket.gethostbyname(socket.gethostname())], capture_output=True, text=True, timeout=10)
        ping_time = result.stdout.split("time=")[1].split(" ")[0]
        return str(ping_time)
    except (IndexError, subprocess.TimeoutExpired):
        return None



@app.route("/")
def render_website():
    return flask.render_template("index.html")

@app.route(f"/encrypt/<text>")
def return_encrypt(text):
    return encrypt_string(text)

@app.route(f"/{key}/info_packet")
def info_packet():
    return flask.jsonify({
        "uptime": str(time.time() - psutil.boot_time()),
        "cpu":str(psutil.cpu_percent()),
        "ram":str(psutil.virtual_memory().percent), 
        "hostname":socket.gethostname(),
        "ip":socket.gethostbyname(socket.gethostname()),
        "ping": get_ping()
    })

@app.route(f"/{key}/files")
def return_no_files():
    count=0
    result = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            print(str(count) + " - " + file)
            count+=1
            ext = file.split('.')
            ext = ext[len(ext)-1]
            result.append(ext)
    return result

@app.route(f"/{key}/file/<key>/<index>")
def return_files(key,index):
    key = generate_key(key) # get the raw key for decryption
    set_key(key.encode())
    count=0
    for root, dirs, files in os.walk(file_dir): 
        for file in files:
            if int(count)==int(index):
                print(count)
                return decrypt_file_return_string_base64(os.path.join(root, file))
            print(index)
            print(count)
            print("-----")
            count+=1
    return ""

@app.route(f"/{key}/")
def return_status():
    return "welcome"


if(__name__ == "__main__"):

    app.run(host="0.0.0.0",port=port)