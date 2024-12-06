import typer
from .log import setup_logger
from .commands.tune import tune_app
from .commands.files import files_app
from .commands.auth import auth_app
from .commands.model import model_app
from .commands.accelerator import accelerator_app
import logging

# Create typer app
app = typer.Typer(help="Felafax CLI")
setup_logger()

logger = logging.getLogger(__name__)


# Create sub-commands
app.add_typer(auth_app, name="auth")
app.add_typer(files_app, name="files")
app.add_typer(tune_app, name="tune")
app.add_typer(model_app, name="model")
app.add_typer(accelerator_app, name="accelerator")

if __name__ == "__main__":
    logger.info("Starting Felafax CLI")
    app()