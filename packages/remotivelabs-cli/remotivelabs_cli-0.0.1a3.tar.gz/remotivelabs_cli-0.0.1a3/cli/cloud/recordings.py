import sys
import signal
from multiprocessing import Process
import typer
import requests
import os
import json
import shutil
from rich.progress import Progress, SpinnerColumn, TextColumn
from . import rest_helper as rest

app = typer.Typer()

def uid(p):
    print(p)
    return p['uid']

def project_names():
    r = requests.get(f'{rest.base_url}/api/bu/{rest.org}/project', headers=rest.headers)
    #sys.stderr.write(r.text)
    if r.status_code == 200:
        projects = r.json()
        names = map(lambda p: p['uid'], projects)
        return (list(names))
    else:
        sys.stderr.write(f"Could not list projects due to {r.status_code}\n")
        #os.kill(signal.SIGSTOP)
        raise typer.Exit(0)
        #return []

        #return map(list(r.json()), lambda e: e.uid)
#    return ["beamyhack"]


@app.command("list", help="Lists recordings in project")
def listRecordings(type: str = typer.Argument(default="all", help="all, processing, recent"),
         project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT',
                                     autocompletion=project_names)):


    if project == "_":
        print("Something went wrong")
        raise typer.Exit()

    if type == "all":
        rest.handle_get(f"/api/project/{project}/files/recording")
    elif type == "recent":
        rest.handle_get(f"/api/project/{project}/files/recording/recent")
    elif type == "processing":
        rest.handle_get(f"/api/project/{project}/files/recording/processing")
    else:
        print("Unknown type: " + type)


@app.command(help="Shows details about a specific recording in project")
def describe(name: str, project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    rest.handle_get(f"/api/project/{project}/files/recording/{name}")


def doStart(name: str, project: str, api_key: str, return_response: bool = False):
    if api_key == "":
        body = {"size": "S"}
    else:
        body = {"size": "S", 'apiKey': api_key}
    return rest.handle_post(f"/api/project/{project}/brokers/{name}", body=json.dumps(body),
                            return_response=return_response)





@app.command(help="Plays all recording files or a single recording")
def play(recording_session: str = typer.Option(..., help="Recording session id"),
         ensure_broker_started: bool = typer.Option(default=False, help="Ensure broker exists, start otherwise"),
         broker: str = typer.Option(..., help="Broker name to play on"),
         project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
        rest.ensure_auth_token()
        v = progress.add_task(description=f"Verifying broker {broker} exists...", total=100)
        r = requests.get(f'{rest.base_url}/api/project/{project}/brokers/{broker}', headers=rest.headers)
        progress.update(v, advance=100.0)
        if r.status_code == 404:
            if ensure_broker_started:
                progress.add_task(description=f"Starting broker {broker}...", total=1)
                r = doStart(broker, project, '', return_response=True)
                if r.status_code != 200:
                    print(r.text)
                    exit(0)
            else:
                print("Broker not running, use --ensure-broker-started to start the broker")
                exit(0)
        elif r.status_code != 200:
            sys.stderr.write(f"Got http status code {r.status_code}")
            typer.Exit(0)

        progress.add_task(
            description=f"Uploading recording {recording_session} to {broker} and setting play mode to pause...",
            total=None)
        #if recording_file == "":
        #    rest.handle_get(f"/api/project/{project}/files/recording/{recording_session}/upload",
        #                    params={'brokerName': broker})
        #else:
        rest.handle_get(f"/api/project/{project}/files/recording/{recording_session}/upload",
                            params={'brokerName': broker})


@app.command(help="Downloads the specified recording file")
def download(recording_session: str = typer.Option(..., help="Recording session id"),
             recording_file: str = typer.Option("", help="Recording file"),
             project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
        progress.add_task(description=f"Downloading {recording_file}", total=None)

        # First request the download url from cloud. This is a public signed url that is valid
        # for a short period of time
        rest.ensure_auth_token()
        get_signed_url_resp = requests.get(
            f'{rest.base_url}/api/project/{project}/files/recording/{recording_session}/recording-file/{recording_file}',
            headers=rest.headers, allow_redirects=True)
        if get_signed_url_resp.status_code == 200:

            # Next download the actual file
            download_resp = requests.get(url=get_signed_url_resp.json()["downloadUrl"], stream=True)
            if download_resp.status_code == 200:
                with open(recording_file, 'wb') as out_file:
                    shutil.copyfileobj(download_resp.raw, out_file)
                print(f"{recording_file} downloaded")
            else:
                sys.stderr.write(download_resp.text)
                sys.stderr.write(f"Got http status {download_resp.status_code}\n")
        else:
            sys.stderr.write(get_signed_url_resp.text)
            sys.stderr.write(f"Got http dd status {get_signed_url_resp.status_code}\n")


@app.command()
def upload(file: str, project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):

    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
        progress.add_task(description=f"Uploading {file}", total=None)

        filename = os.path.basename(file)
        rest.ensure_auth_token()
        rest.headers["content-type"] = "application/octet-stream"
        r = requests.post(f"{rest.base_url}/api/project/{project}/files/recording/{filename}", headers=rest.headers)
        if r.status_code == 200:
            headers = {}
            headers["content-type"] = "application/x-www-form-urlencoded"
            r = requests.put(r.text, open(file, 'rb'), headers = headers)
            print("File successfully uploaded, please run 'remotive cloud recordings list' to verify that the recording was successfully processed")
        else:
            print(r.text)
