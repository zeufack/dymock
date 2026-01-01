import click
import uvicorn

from src.service.server import MockServer


@click.group()
def cli():
    """Dymock: A tool to generate mock APIs from OpenAPI specifications."""
    pass


@cli.command()
@click.option(
    "--spec",
    "-s",
    type=click.Path(exists=True),
    required=True,
    help="Path to the OpenAPI specification file.",
)
@click.option("--host", "-h", default="127.0.0.1", help="Host to run the server on.")
@click.option("--port", "-p", default=8000, type=int, help="Port to run the server on.")
def run(spec, host, port):
    """Run the mock API server."""
    try:
        click.echo(f"Loading OpenAPI specification from: {spec}")
        server = MockServer(spec_path=spec)
        app = server.create_app()
        click.echo(f"Starting mock server on http://{host}:{port}")
        click.echo("Press Ctrl+C to stop the server")
        uvicorn.run(app, host=host, port=port)
    except FileNotFoundError as e:
        click.echo(f"Error: Specification file not found: {e}", err=True)
        raise click.Abort()
    except PermissionError as e:
        click.echo(f"Error: Cannot read specification file: {e}", err=True)
        raise click.Abort()
    except ValueError as e:
        click.echo(f"Error: Invalid OpenAPI specification: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Unexpected error starting server: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    cli()
