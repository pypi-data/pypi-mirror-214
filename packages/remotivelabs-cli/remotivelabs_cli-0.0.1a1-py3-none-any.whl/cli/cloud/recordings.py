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

    #print(project)
    #raise typer.Exit()
    #try:
        #project_names()
    #except SystemExit as e:
    #    raise sys.exit(e)

    if project == "_":
        print("Something went wrong")
        raise typer.Exit()
    #else:
    #    print(project)

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
         recording_file: str = typer.Option("", help="Recording file"),
         ensure_broker_started: bool = typer.Option(default=False, help="Ensure broker exists, start otherwise"),
         broker: str = typer.Option(..., help="Broker name to play on"),
         project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
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
                print("Broker not running, use --ensure-broker-started true to start the broker")
                exit(0)
        progress.add_task(
            description=f"Uploading recording {recording_session} to {broker} and setting play mode to pause...",
            total=None)
        if recording_file == "":
            rest.handle_get(f"/api/project/{project}/files/recording/{recording_session}/upload",
                            params={'brokerName': broker})
        else:
            rest.handle_get(f"/api/project/{project}/files/recording/{recording_session}/{recording_file}/upload",
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
        get_signed_url_resp = requests.get(
            f'{rest.base_url}/api/project/{project}/files/recording/{recording_session}/recording-file/{recording_file}',
            headers=rest.headers(), allow_redirects=True)
        if get_signed_url_resp.status_code == 200:

            # Next download the actual file
            download_resp = requests.get(url=get_signed_url_resp.json()["downloadUrl"], stream=True)
            if download_resp.status_code == 200:
                with open(recording_file, 'wb') as out_file:
                    shutil.copyfileobj(download_resp.raw, out_file)
                print(f"{recording_file} downloaded")
            else:
                sys.stderr.write(f"Got unexpected status {download_resp.status_code}\n")
        else:
            sys.stderr.write(f"Got unexpected status {get_signed_url_resp.status_code}\n")

# @app.command()
# def upload(file: str, project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
# files = {'upload_file': open(file, 'rb')}
# values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}
# rest.headers["content-type"] = "application/octet-stream"
# r = requests.get(f"{rest.base_url}/api/project/{project}/files/recording/upload/{file}", headers=rest.headers)
# print(r.status_code)
# print(r.text)

# curl -X PUT -H 'Content-Type: application/octet-stream' --upload-file docker-compose.yml 'https://storage.googleapis.com/beamylabs-fileuploads-dev/projects/beamyhack/recording/myrecording?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=recordings-upload-account%40beamycloud-dev.iam.gserviceaccount.com%2F20220729%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20220729T134012Z&X-Goog-Expires=3000&X-Goog-SignedHeaders=content-type%3Bhost&X-Goog-Signature=d1fa7639349d6453aebfce8814d6e5685af03952d07aa4e3cb0d44dba7cf5e572f684c8120dba17cbc7ea6a0ef5450542a3c745c65e04272b34265d0ddcf1b67e6f2b5bfa446264a62d77bd7faabf45ad6bd2aec5225f57004b0a31cfe0480cba063a3807d86346b1da99ecbae3f3e6da8f44f06396dfc1fdc6f89e475abdf969142cef6f369f03aff41000c8abb28aa82185246746fd6c16b6b381baa2d586382a3d3067b6376ddba2b55b2b6f9d942913a1cbfbc61491ba6a615d7d5a0d9a476c357431143e9cea1411dfad9f01b1e1176dc8c056cbf08cccfd401a55d63c19d038f3ab42b712abc48d759047ac07862c4fae937c341e19b568bb60a4e4086'
