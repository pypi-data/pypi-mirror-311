try:
    import typer
except ImportError as import_error:
    raise ImportError(
        "You don't have Typer installed, "
        "install this package with the [cli] extra:\n"
        "pip install mind-the-gap[cli]"
    ) from import_error

from tfl.cli import cycles

app = typer.Typer()
app.add_typer(cycles.app, name="cycles")

if __name__ == "__main__":
    app()
