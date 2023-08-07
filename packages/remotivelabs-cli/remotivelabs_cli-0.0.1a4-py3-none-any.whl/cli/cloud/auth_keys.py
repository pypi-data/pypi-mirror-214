from pathlib import Path

import typer
from . import rest_helper as rest

app = typer.Typer()


@app.command(name="create", help="Create and download a new personal access token")
def get_personal_access_token():
    rest.ensure_auth_token()
    rest.handle_post('/api/me/keys')

    response = rest.handle_post(url='/api/me/keys',
                                return_response=True)

    if response.status_code == 200:
        name = response.json()['name']
        write_personal_token(f"personal-{name}-key.json", response.text)
    else:
        print(f'Got status code: {response.status_code}')
        print(response.text)


@app.command(name="list", help="List personal access tokens")
def list_personal_access_tokens():
    rest.ensure_auth_token()
    rest.handle_get('/api/me/keys')


@app.command(name="revoke", help="Revoke the specified key")
def revoke(
        key_name: str = typer.Option(..., help="Name of the key to revoke")
):
    rest.ensure_auth_token()
    rest.handle_delete(f'/api/me/keys/{key_name}')


def write_personal_token(file, token):
    path = str(Path.home()) + f"/.config/.remotive/{file}"
    f = open(path, "w")
    f.write(token)
    f.close()
    print(f"Personal key written to {path}")
    print("Use 'remotive cloud auth activate filename' to use this key from cli")
    print('\033[93m This file contains secrets and must never be compromised')