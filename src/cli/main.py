import typer
from src.cli.repl import run_repl
from src.log.logging_config import clean_log

clean_log()

app = typer.Typer()

@app.command()
def chat():
    run_repl()


if __name__ == "__main__":
    app()