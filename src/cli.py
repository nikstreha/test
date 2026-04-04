import structlog
import typer
from gunicorn.app.base import BaseApplication

from authorization.composition.configuration.settings import Settings
from authorization.infrastructure.logging.setup import configure_logging

configure_logging(log_level=Settings().LOG_LEVEL)  # type: ignore

logger = structlog.get_logger(__name__)

cli = typer.Typer(no_args_is_help=True)


class StandaloneApplication(BaseApplication):
    def __init__(self, app_uri, options=None):
        self.options = options or {}
        self.app_uri = app_uri
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        from gunicorn.util import import_app

        return import_app(self.app_uri)


@cli.command()
def api(
    host: str = typer.Option("0.0.0.0"),
    port: int = typer.Option(8000),
    workers: int = typer.Option(1),
    reload: bool = typer.Option(False),
) -> None:
    options = {
        "bind": f"{host}:{port}",
        "workers": workers,
        "worker_class": "uvicorn.workers.UvicornWorker",
        "reload": reload,
        "factory": True,
        "loglevel": "info",
        "accesslog": "-",
    }

    logger.info(f"Starting Gunicorn on {host}:{port} with {workers} workers")

    StandaloneApplication(
        "authorization.composition.api_app:build_api_app", options
    ).run()


if __name__ == "__main__":
    cli()
