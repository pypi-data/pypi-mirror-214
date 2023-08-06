import logging
import os

import typer

app = typer.Typer()

from kaxi import Runner, log

logger = logging.getLogger("kaxi")


@app.command()
def run(filename: str):
    runner = Runner.from_yaml(filename)

    log.init(runner.settings.get("verbose", False))

    runner.execute()
