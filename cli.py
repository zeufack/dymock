import click


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
    print(spec, host, port)


if __name__ == "__main__":
    cli()
