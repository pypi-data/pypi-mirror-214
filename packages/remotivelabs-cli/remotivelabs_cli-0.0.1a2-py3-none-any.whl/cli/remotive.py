import typer
from .brokers import app as broker_app
from .cloud.cloud_cli import app as cloud_app

# from cloud import cloud_cli

app = typer.Typer()


# def run_cli():

app.add_typer(broker_app, name="broker", help="Manage a single broker - local or cloud")
app.add_typer(cloud_app, name="cloud", help="Manage resources in RemotiveCloud", )
