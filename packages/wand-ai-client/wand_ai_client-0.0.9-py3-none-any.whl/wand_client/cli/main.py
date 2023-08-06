import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import click
import rich
from click import Context
from prompt_toolkit import PromptSession
from rich.progress import Progress

from wand_client import __version__
from wand_client.cli.config import CONFIG_PATH, WandCliSettings
from wand_client.cli.formatters import (
    ModelFormatter,
    ModelsFormatter,
    RichRetrainProgressListener,
    SettingsFormatter,
    SourceFormatter,
    TrainingFormatter,
    TrainingsFormatter,
)
from wand_client.sdk.core import Model, TrainingListener, WandClient


class Root:
    def __init__(self, option_settings: Dict[str, Any]) -> None:
        self._option_settings = option_settings

    def get_settings(self) -> WandCliSettings:
        return WandCliSettings(**self._option_settings)

    def get_client(self) -> WandClient:
        settings = self.get_settings()
        settings.check_complete()
        return WandClient(
            base_url=settings.WAND_API_URL,  # type: ignore
            token=settings.WAND_TOKEN,  # type: ignore
        )


@click.group()
@click.version_option(__version__)
@click.option("--api_url", type=str, default=None)
@click.option("--token", type=str, default=None)
@click.pass_context
def cli(ctx: Context, api_url: Optional[str], token: Optional[str]) -> None:
    option_settings = {
        "WAND_API_URL": api_url,
        "WAND_TOKEN": token,
    }
    option_settings = {
        key: value for key, value in option_settings.items() if value is not None
    }
    ctx.obj = Root(option_settings)


@cli.group()
def config() -> None:
    """
    Client setup commands
    """


@config.command()
@click.option("--api_url", type=str, required=True)
@click.option("--token", type=str, required=True)
def setup(api_url: str, token: str) -> None:
    """
    Initialize cli client
    """
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps(
            {
                "WAND_API_URL": api_url,
                "WAND_TOKEN": token,
            }
        )
    )
    print(f"Wrote config to: {CONFIG_PATH.absolute()}")


@config.command()
@click.pass_context
def show(ctx: Context) -> None:
    """
    Show current settings
    """
    settings: WandCliSettings = ctx.obj.get_settings()
    rich.print(SettingsFormatter()(settings))


@cli.group()
def source() -> None:
    """
    Operations with data sources
    """


@source.command()
@click.argument("filename", type=click.Path(exists=True))
@click.pass_context
def upload_file(ctx: Context, filename: Path) -> None:
    """Upload a file as a source"""
    client: WandClient = ctx.obj.get_client()
    source = client.source.create_from_filepath(filename)
    rich.print(SourceFormatter()(source))


@source.command()
@click.option("--max-pages", type=int, default=1000)
@click.argument("url", type=click.STRING, nargs=-1)
@click.pass_context
def web(ctx: Context, url: List[str], max_pages: int = 1000) -> None:
    """Create a web scrapper source"""
    client: WandClient = ctx.obj.get_client()
    source = client.source.create_web(url, max_pages)
    rich.print(SourceFormatter()(source))


@cli.group()
def model() -> None:
    """
    Operations with ml models
    """


@model.command()
@click.argument("source_id", type=click.STRING, nargs=-1)
@click.pass_context
def train(ctx: Context, source_id: List[str]) -> None:
    """Upload a file as a source"""
    client: WandClient = ctx.obj.get_client()

    with Progress() as progress:
        task = progress.add_task("Training model")

        class _Listener(TrainingListener):
            def on_progress(self, model: Model) -> None:
                progress.update(
                    task,
                    completed=model.status.progress,
                    description=f"Training model {model.id}",
                )
                progress.refresh()

        model = client.models.train(source_ids=source_id, listener=_Listener())
        rich.print(model.id)


@model.command()
@click.argument("model_id", type=click.STRING)
@click.pass_context
def get(ctx: Context, model_id: str) -> None:
    """Get info about model by ID"""
    client: WandClient = ctx.obj.get_client()
    model = client.models.get(model_id=model_id)
    rich.print(ModelFormatter()(model))


@model.command()
@click.argument("model_id", type=click.STRING)
@click.pass_context
def delete(ctx: Context, model_id: str) -> None:
    """Get info about model by ID"""
    client: WandClient = ctx.obj.get_client()
    client.models.delete(model_id=model_id)
    rich.print("Model deleted")


@model.command()
@click.argument("model_id", type=click.STRING)
@click.pass_context
def retrain(ctx: Context, model_id: str) -> None:
    """Upload a file as a source"""
    client: WandClient = ctx.obj.get_client()

    with Progress() as progress:
        training = client.models.retrain(
            model_id, listener=RichRetrainProgressListener(progress)
        )
        rich.print(
            f"Training of model {training.model_id} with "
            f"training id {training.id} finished"
        )


@model.command(name="list")
@click.pass_context
def list_(ctx: Context) -> None:
    """List all models"""
    client: WandClient = ctx.obj.get_client()
    models = client.models.list_all()
    rich.print(ModelsFormatter()(models))


@model.command()
@click.argument("model_id", type=click.STRING)
@click.pass_context
def chat(ctx: Context, model_id: str) -> None:
    """Talk with LLM model"""
    client: WandClient = ctx.obj.get_client()
    chat = client.models.start_chat(model_id)

    print(f"You are talking to model with id {model_id}. Type 'exit' to close.")

    session: PromptSession[str] = PromptSession()
    console = rich.console.Console()
    while True:
        prompt_text = session.prompt("> ")
        if prompt_text == "exit":
            return
        with console.status("Generating answer...", spinner="bouncingBall"):
            resp = chat.ask(prompt_text)
        console.print(resp, style="bold")


@cli.group()
def training() -> None:
    """
    Operations with ml trainings
    """


@training.command(name="get")
@click.argument("training_id", type=click.STRING)
@click.pass_context
def get_training(ctx: Context, training_id: str) -> None:
    """Get info about training by ID"""
    client: WandClient = ctx.obj.get_client()
    training = client.trainings.get(training_id=training_id)
    rich.print(TrainingFormatter()(training))


@training.command(name="list")
@click.pass_context
def list_training(ctx: Context) -> None:
    """List all training"""
    client: WandClient = ctx.obj.get_client()
    models = client.trainings.list_all()
    rich.print(TrainingsFormatter()(models))


if __name__ == "__main__":
    cli()
