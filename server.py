import flask
import flask_cors
from modules.encrypt import *
from modules.gen import generate_key
import subprocess
import socket
import io
from PIL import Image
from shutil import move
import time
import psutil
import os
import uuid


port = 4040
file_dir = "./resources/full/"
temp_dir = "./resources/temp/"
app = flask.Flask(__name__)
CORS = flask_cors.CORS(app)
key = "75e9bc89514d1b8ca251cbd922500acee7dd102922cb4e671e9dbdf63cbbdd8c" # swap this for your own password
set_key(b'sYibxVcu1QDal1uETk-G4nho___kPjHhYwFzMFSXEGo=')
login_message = ""


def get_ping():
    try:
        result = subprocess.run(['ping', '-c', '1', socket.gethostbyname(socket.gethostname())], capture_output=True, text=True, timeout=10)
        ping_time = result.stdout.split("time=")[1].split(" ")[0]
        return str(ping_time)
    except (IndexError, subprocess.TimeoutExpired):
        return None
def rename_file(filepath):
    # Ensure the file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    # Generate a unique name
    file_dir = os.path.dirname(filepath)
    file_ext = os.path.splitext(filepath)[1]
    new_name = f"{uuid.uuid4()}{file_ext}"
    new_path = os.path.join(file_dir, new_name)

    # Rename the file
    os.rename(filepath, new_path)
    print(f"File renamed to: {new_path}")

    return new_path
def remove_exif_data(filepath):
    # Ensure the file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    # Get the file extension and output path
    file_ext = os.path.splitext(filepath)[1].lower()
    output_path = os.path.splitext(filepath)[0] + file_ext

    if file_ext not in [".jpg", ".jpeg", ".png"]:
        print(f"Unsupported file type: {file_ext}")
        return ""

    try:
        with Image.open(filepath) as img:
            # Save the image without EXIF data
            img_without_exif = Image.new(img.mode, img.size)
            img_without_exif.putdata(list(img.getdata()))
            img_without_exif.save(output_path)
            print(f"Image saved without EXIF data: {output_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to process image: {e}")

    return output_path
def generate_low_quality(filepath):
    # Ensure the file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    # Get the file extension and output path
    file_ext = os.path.splitext(filepath)[1].lower()
    output_path = os.path.splitext(filepath)[0] + "_low_quality" + file_ext

    if file_ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
        # Process image files
        try:
            with Image.open(filepath) as img:
                # Resize the image to 25% of its original size
                img_resized = img.resize(
                    (img.width // 4, img.height // 4), Image.Resampling.LANCZOS
                )
                # Save with lower quality
                img_resized.save(output_path, quality=30)
                print(f"Low-quality image saved to: {output_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to process image: {e}")

    elif file_ext in [".mp4", ".avi", ".mkv", ".mov", ".wmv"]:
        # Process video files: Generate a thumbnail
        output_path = os.path.splitext(filepath)[0] + "_low_quality.jpg"
        try:
            # Use FFmpeg to extract a single frame as a thumbnail
            subprocess.run(
                [
                    "ffmpeg",
                    "-i", filepath,
                    "-ss", "00:00:01",
                    "-vframes", "1",
                    "-q:v", "2",
                    output_path
                ],
                check=True
            )
            print(f"Video thumbnail saved to: {output_path}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to generate video thumbnail: {e}")
    else:
        print(f"Unsupported file type: {file_ext}")
        return("file is incompatable for this")
    encrypt_file(output_path)
    return output_path
def cend(string,array=[]):
    for end in array:
        if string.endswith(end):
            return True
    return False
for file_name in os.listdir(temp_dir):
    rename_file(os.path.join(temp_dir, file_name))
for file_name in os.listdir(temp_dir):
    remove_exif_data(os.path.join(temp_dir, file_name))
    # rename files
for file_name in os.listdir(temp_dir):
    source_path = os.path.join(temp_dir, file_name)
    destination_path = os.path.join(file_dir, file_name)
    try:
        move(source_path, destination_path)
        print(f"Moved {file_name} to {file_dir}")
        generate_low_quality(destination_path)
        encrypt_file(destination_path)
        
    except Exception as e:
        print(f"Failed to move {file_name}: {e}")

# app routes:
@app.route("/")
def render_website():
    return flask.render_template("index.html")

@app.route(f"/{key}/")
def return_status():
    return login_message

@app.route(f"/encrypt/<text>")
def return_encrypt(text):
    return encrypt_string(text)

@app.route(f'/{key}/upload_end', methods=['POST'])
def upload_file():
    if 'files' not in flask.request.files:
        return 'No files part'
    
    files = flask.request.files.getlist('files')  # Get list of files from the form
    
    if not files:
        return 'No selected files'
    
    uploaded_files = []
    for file in files:
        if file.filename == '':
            return 'One of the files is missing a name'
        
        # Save each file to the uploads directory
        file_path = os.path.join(temp_dir, file.filename)
        file.save(file_path)
        uploaded_files.append(file.filename)

    return f"Files uploaded successfully: {', '.join(uploaded_files)}"

@app.route('/upload')
def render_upload():
    return flask.render_template("upload.html")

@app.route(f"/{key}/files_low_quality")
def return_files_low_quality():
    result=[]
    for file_name in os.listdir(file_dir):
        if((file_name.split("."))[0].endswith("_low_quality")):
            result.append(os.path.join(file_dir, file_name))
    return flask.jsonify(result)

@app.route(f"/{key}/files")
def return_files():
    result=[]
    for file_name in os.listdir(file_dir):
        if((file_name.split("."))[0].endswith("_low_quality")):
            pass
        else:
            result.append(os.path.join(file_dir, file_name))
    return flask.jsonify(result)

@app.route(f"/{key}/file_data/<path:file_name>")
def serve_file_base64(file_name):
        return str(decrypt_file_return_string_base64(file_name))

@app.route(f'/{key}/file/<path:file_name>')
def serve_file(file_name):
    img_data = base64.b64decode(str(decrypt_file_return_string_base64(file_name)))
    
    # Return the decoded binary data with the appropriate MIME type
    return flask.Response(io.BytesIO(img_data), mimetype='image/png')

@app.route(f'/{key}/file/lowres/<path:file_name>')
def serve_image_low_res(file_name):
    file_name_low_quality = os.path.basename(os.path.normpath(file_name))
    file_name_low_quality = (file_name_low_quality.split("."))[0]
    file_name_low_quality = file_name_low_quality + "_low_quality.jpg"
    file_name_low_quality = file_name.replace(os.path.basename(os.path.normpath(file_name)),"") + file_name_low_quality
    
    img_data = base64.b64decode(str(decrypt_file_return_string_base64(file_name_low_quality)))
    
    # Return the decoded binary data with the appropriate MIME type
    return flask.Response(io.BytesIO(img_data), mimetype='image/png')


# todo

if(__name__ == "__main__"):

    app.run(host="0.0.0.0",port=port)