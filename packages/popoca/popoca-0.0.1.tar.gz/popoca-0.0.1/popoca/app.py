import typer
from rich import print

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
app = typer.Typer(context_settings=CONTEXT_SETTINGS, no_args_is_help=True)


@app.command()
def init():
    """Función principal"""
    print("Función principal")
    print("Esta es la función principal")


def run():
    app()


if __name__ == "__main__":
    run()
