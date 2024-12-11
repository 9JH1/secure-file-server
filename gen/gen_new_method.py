import subprocess
def gen_new_method(password):
    result = subprocess.run(['./gen_new_method', '--password',f'{password}'], capture_output=True, text=True)