import typer
from .brokers import app as broker_app
from .cloud.cloud_cli import app as cloud_app

app = typer.Typer()

app.add_typer(broker_app, name="broker", help="Manage a single broker - local or cloud")
app.add_typer(cloud_app, name="cloud", help="Manage resources in RemotiveCloud", )
