from rich.console import Console
import typer
from docker_tags_getter.cli.repos import repos
from docker_tags_getter.cli.repo import repo

console = Console()
cli_app = typer.Typer(rich_markup_mode="rich")
cli_app.add_typer(repos, name="repos", help="Manage repos information")
cli_app.add_typer(repo, name="repo", help="Manage repo information")

