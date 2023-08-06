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
from docker_tags_getter.filters.tags_filter import TagsFilter
from docker_tags_getter.api.v2.repositories_api import RepositoriesAPI
from docker_tags_getter.api.v2.tags_api import TagsAPI

console = Console()
repo = typer.Typer()

@repo.command()
def tags(
    namespace: str = typer.Option(
        None, "--namespace", "-ns",
        help="[b]The namespace[/] is a uniq identification of [b]a user or a organisation[/].",
        show_default=False
    ),
    repository: str = typer.Option(
        None, "--repository", "-r",
        help="[b]The repository[/] is a uniq identification of [b]a project[/].",
        show_default=False
    ),
    filter: bool = typer.Option(
        None, "--filter", "-f",
        help="[b]The tags[/] will be filtered.",
        show_default=False
    ),
):
    """
    [green b]All tags[/] will be returned for the [yellow b]namespace[/].
    """
    if namespace is None:
        console.print(f"[red b][ERROR] Please, give the namespace name!!![/]")
        return

    if namespace is None:
        console.print(f"[red b][ERROR] Please, give the repository name!!![/]")
        return

    headers_config = HeadersConfig()
    fetcher = ApiFetcher(headers_config)

    tags_api = TagsAPI(fetcher, namespace, repository)

    tags = tags_api.get_list()

    if filter:
        if 'latest' in tags:
            tags.remove('latest')

        tags_filter = TagsFilter()
        tags = tags_filter.filter_list(tags)

    for tag in tags:
        console.print(tag)

