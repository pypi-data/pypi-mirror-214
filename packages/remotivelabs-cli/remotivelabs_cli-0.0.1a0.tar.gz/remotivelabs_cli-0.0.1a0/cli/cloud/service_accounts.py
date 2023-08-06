import typer
# from typing_extensions import Annotated
from typing import List, Optional

import json
from rich.progress import Progress, SpinnerColumn, TextColumn
import sys
from . import rest_helper as rest
from . import service_account_keys

app = typer.Typer()


@app.command(name="list", help="List service-accounts")
def list(project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    rest.handle_get(f"/api/project/{project}/admin/accounts")


@app.command(name="create", help="Create service account")
def create(
        name: str,
        role: List[str] = typer.Option(..., help="Roles to apply"),
        project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    data = {
        'name': name,
        'roles': role
    }
    rest.handle_post(url=f"/api/project/{project}/admin/accounts", body=json.dumps(data))


@app.command(name="delete", help="Create service account")
def delete(
        name: str,
        project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    rest.handle_delete(url=f"/api/project/{project}/admin/accounts/{name}")


app.add_typer(service_account_keys.app, name="keys", help="Manage project service account keys")
