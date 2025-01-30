import flask
import flask_cors
from modules.encrypt import *
from modules.gen import generate_key as gk
import subprocess
import socket
import base64
from base64 import urlsafe_b64decode
import time
import io
from PIL import Image
from shutil import move
from time import sleep
import os
import uuid
import mimetypes


loading_log = {}
key_file = '../test.key'
port = 4040
file_dir = "/home/_3hy/.enc/"
temp_dir = "./resources/"
app = flask.Flask(__name__)
CORS = flask_cors.CORS(app)
key = "75e9bc89514d1b8ca251cbd922500acee7dd102922cb4e671e9dbdf63cbbdd8c"
set_key("sYibxVcu1QDal1uETk-G4nho___kPjHhYwFzMFSXEGo= ".encode())
login_message = "welcome"
fernet = False;

def get_ping():
    try:
        result = subprocess.run(['ping', '-c', '1', socket.gethostbyname(socket.gethostname())], capture_output=True, text=True, timeout=10)
        ping_time = result.stdout.split("time=")[1].split(" ")[0]
        return str(ping_time)
    except (IndexError, subprocess.TimeoutExpired):
        return None
def decode_url_friendly(encoded_phrase):
    # Add padding if missing
    padding = '=' * (-len(encoded_phrase) % 4)
    base64_bytes = encoded_phrase + padding
    
    # Decode from Base64 URL-safe encoding
    phrase_bytes = base64.urlsafe_b64decode(base64_bytes)
    
    # Convert bytes back to string
    return phrase_bytes.decode('utf-8')
def make_url_friendly(phrase):
    phrase_bytes = phrase.encode('utf-8')

    # Use Base64 URL-safe encoding
    base64_bytes = base64.urlsafe_b64encode(phrase_bytes)
    
    # Decode back to string and strip padding
    return base64_bytes.decode('utf-8').rstrip("=")
"""
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
    try:     
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
    except:
        print("error occured in exif removal with file: " + filepath);
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
"""

# app routes:
@app.route("/")
def render_website():
    print(f"\n\033[31mvistor joined:{flask.request.remote_addr}\033[0m\n")
    return flask.render_template("index.html")

@app.route(f"/{key}/")
def return_status():
    return flask.Response(status=200)

@app.route(f"/{key}/f/<fernet>")
def set_fernet(fernet):
    set_key(fernet.encode());
    return flask.Response(status=200)

@app.route(f"/encrypt/<text>")
def return_encrypt(text):
    sleep(5)
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

@app.route(f"/{key}/files")
def print_dir_tree():
    def build_tree(path):
        node = {"name": os.path.basename(path), "is_dir": True, "children": []}
        try:
            for entry in os.scandir(path):
                if entry.is_dir():
                    node["children"].append(build_tree(entry.path))
                else:
                    node["children"].append({"name": entry.name, "is_dir": False, "children": []})  # Ensure 'children' exists for files
        except PermissionError:
            pass  # Handle any permission errors by skipping that directory
        return node

    def print_tree(node, level=0):
        indent = "  " * level
        result = f"{indent}{node['name']}/" if node["is_dir"] else f"{indent}{node['name']}"
        for child in node["children"]:
            result += "\n" + print_tree(child, level + 1)
        return result

    tree = build_tree(file_dir)
    return tree

@app.route(f"/{key}/gen_fernet/<fernet_key>")
def generate_fernet_key(fernet_key):
    return gk(decode_url_friendly(fernet_key))

@app.route(f'/{key}/file/<fernet>/<path:file_name>')
def serve_file(fernet,file_name):
    fernet = decode_url_friendly(fernet).encode()
    try:
        # Ensure the file name starts with "/"
        if not file_name.startswith("/"):
            file_name = "/" + file_name
        
        # Decode the file content
        img_data = base64.b64decode(decrypt_file_return_string_base64_local(fernet,file_name))
        
        # Determine MIME type based on the file name
        mime_type, _ = mimetypes.guess_type(file_name)
        if mime_type is None:
            mime_type = "application/octet-stream"  # Fallback MIME type

        # Return the decoded binary data as a Flask response
        return flask.Response(io.BytesIO(img_data), mimetype=mime_type)
    except Exception as e:
        # Handle errors gracefully
        return flask.Response(f"Error serving file: {str(e)}", status=500)


@app.route(f'/{key}/file_progress/<path:file_name>')
def serve_file_progress(file_name):
    try:
        if not file_name.startswith("/"):
            file_name = "/" + file_name
        file_data = base64.b64decode(decrypt_file_return_string_base64(file_name))
        mime_type, _ = mimetypes.guess_type(file_name)
        if mime_type is None:
            mime_type = "application/octet-stream"
        loading_log[file_name] = "0.00"  # Start progress at 0%
        
        # Log the MIME type for debugging
        print(f"Serving file {file_name} with MIME type {mime_type}")
        file_stream = io.BytesIO(file_data)

        def generate_file():
            chunk_size = 1024 * 1024  # 1MB per chunk
            bytes_read = 0
            total_size = len(file_data)

            while bytes_read < total_size:
                chunk = file_data[bytes_read:bytes_read + chunk_size]
                bytes_read += len(chunk)
                yield chunk  # Stream the chunk
                
                # Update progress and cap it at 100%
                progress = min((bytes_read / total_size) * 100, 100)
                loading_log[file_name] = f"{progress:.2f}"
                print(f"Progress: {progress:.2f}%")
        
        return flask.Response(generate_file(), mimetype=mime_type)

    except Exception as e:
        return flask.Response(f"Error serving file: {str(e)}", status=500)

@app.route(f'/{key}/progress/<path:file_name>')
def serve_progress(file_name):
    global loading_log
    if not file_name.startswith("/"):
        file_name = "/" + file_name
    progress = loading_log.get(file_name, "Progress not available")
    
    # Ensure progress is capped at 100%
    if isinstance(progress, str) and progress != "Progress not available":
        progress = f"{min(float(progress), 100):.2f}"
    
    return progress


@app.route(f'/{key}/file_lowres/<path:file_name>')
def serve_image_low_res(file_name):
    if not file_name.startswith("/"):
        file_name = "/" + file_name
    file_name_low_quality = os.path.basename(os.path.normpath(file_name))
    file_name_low_quality = (file_name_low_quality.split("."))[0]
    file_name_low_quality = file_name_low_quality + "_low_quality.jpg"
    file_name_low_quality = file_name.replace(os.path.basename(os.path.normpath(file_name)),"") + file_name_low_quality
    print(f"\n{file_name_low_quality} - {file_name}\n")
    img_data = base64.b64decode(str(decrypt_file_return_string_base64(file_name_low_quality)))
    
    # Return the decoded binary data with the appropriate MIME type
    return flask.Response(io.BytesIO(img_data), mimetype='image/png')

# password change
# decrypt dir? who would do that
# keep folder tree

if(__name__ == "__main__"):
    app.run(host="0.0.0.0",port=port)
