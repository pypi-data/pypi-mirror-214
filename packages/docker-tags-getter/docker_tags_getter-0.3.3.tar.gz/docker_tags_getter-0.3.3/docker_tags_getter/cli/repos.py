################################################################################
# Copyright (C) 2023 Kostiantyn Klochko <kklochko@protonmail.com>              #
#                                                                              #
# This file is part of docker_tags_getter.                                     #
#                                                                              #
# docker_tags_getter is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU Lesser General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or (at your   #
# option) any later version.                                                   #
#                                                                              #
# docker_tags_getter is distributed in the hope that it will be useful, but    #
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY   #
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public       #
# License for more details.                                                    #
#                                                                              #
# You should have received a copy of the GNU Lesser General Public License     #
#along with docker_tags_getter. If not, see <https://www.gnu.org/licenses/>.   #
################################################################################

from rich.console import Console
from rich.prompt import Prompt
from typing import List, Optional
import typer

from docker_tags_getter.config.headers_config import HeadersConfig
from docker_tags_getter.fetcher.api_fetcher import ApiFetcher
from docker_tags_getter.api.v2.repositories_api import RepositoriesAPI

console = Console()
repos = typer.Typer()

@repos.command()
def all(
    namespace: str = typer.Option(
        None, "--namespace", "-ns",
        help="[b]The namespace[/] is a uniq identification of [b]a user or a organisation[/].",
        show_default=False
    )
):
    """
    [green b]All repos[/] will be returned for the [yellow b]namespace[/].
    """
    if namespace is None:
        console.print(f"[red b][ERROR] Please, give the namespace name!!![/]")
        return

    headers_config = HeadersConfig()
    fetcher = ApiFetcher(headers_config)

    repositories_api = RepositoriesAPI(fetcher, namespace)

    names = repositories_api.get_list()

    for name in names:
        console.print(name)

