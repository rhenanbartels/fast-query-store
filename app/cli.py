import click
import uvicorn


@click.group()
def cli():
    pass


@cli.command("run", short_help="Run a uvicorn server.")
@click.option("--host", "-h", default="127.0.0.1", help="The interface to bind to.")
@click.option("--port", "-p", default=5000, help="The port to bind to.")
def run_command(host, port):
    uvicorn.run("app.main:app", host=host, port=port)


if __name__ == "__main__":
    run_command()
