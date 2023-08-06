import json
import os
import sys
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread
import typer
from . import rest_helper as rest

app = typer.Typer()

config_dir_name = str(Path.home()) + "/.config/.remotive/"
token_file_name = str(Path.home()) + "/.config/.remotive/cloud.secret.token"


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        #self.send_response(301)
        #self.send_header('Location', 'https://cloud.remotivelabs.com')
        #self.end_headers()
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def log_message(self, format, *args):
        return

    def do_GET(self):
        self._set_response()
        self.wfile.write("Successfully setup CLI, return to your terminal to continue".encode('utf-8'))
        path = self.path
        time.sleep(1)
        httpd.server_close()

        killerthread = Thread(target=httpd.shutdown)
        killerthread.start()

        if not os.path.exists(config_dir_name):
            os.makedirs(config_dir_name)
        write_token(path[1:])
        print("Successfully logged on, you are ready to go with cli")


def start_local_webserver(server_class=HTTPServer, handler_class=S, port=8089):
    server_address = ('', port)
    global httpd
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


@app.command(help="Login to the cloud")
def login():
    webbrowser.open(f'{rest.base_url}/login?redirectUrl=http://localhost:8089', new=1, autoraise=True)
    start_local_webserver()


@app.command(help="Print access token")
def print_access_token():
    print(read_token())

@app.command(help="List available auth tokens")
def list():
    for file in os.listdir(config_dir_name):
        print(file)

@app.command(help="Show token file")
def describe(
        file: str = typer.Option(..., help="File name")):
    print(read_file(file))


@app.command(help="Activate the account file")
def activate(
        file: str = typer.Option(..., help="File name")):

    # Best effort to read file
    if os.path.exists(file):
        token_file = json.loads(read_file_with_path(file))
        write_token(token_file['token'])
    elif os.path.exists(str(Path.home()) + f"/.config/.remotive/{file}"):
        token_file = json.loads(read_file(file))
        write_token(token_file['token'])
    else:
        sys.stderr.write("File could not be found \n")


@app.command(help="Clear access token")
def logout():
    write_token("")
    print("Access token removed")


@app.command(help="Test authentication")
def test():
    if rest.has_access('/api/whoami'):
        print("Access granted, good to go!")
    else:
        print("Access failed (401), please login again")


def read_token():
    f = open(token_file_name, "r")
    token = f.read()
    f.close()
    return token

def read_file_with_path(file):
    f = open(file, "r")
    token = f.read()
    f.close()
    return token

def read_file(file):
    f = open(str(Path.home()) + f"/.config/.remotive/{file}", "r")
    token = f.read()
    f.close()
    return token

def write_token(token):
    f = open(token_file_name, "w")
    f.write(token)
    f.close()

# Key stuff
# f = open(str(Path.home())+ "/.remotivelabs/privatekey.json", "r")
# j = json.loads(f.read())
# print(j['privateKey'])
# key = load_pem_private_key(bytes(j['privateKey'],'UTF-8'), None)
# print(key.key_size)
#
# "exp": datetime.now(tz=timezone.utc)
# encoded = jwt.encode({"some": "payload"}, j['privateKey'] , algorithm="RS256", headers={"kid":  j["keyId"]})
# print(encoded)
