from __future__ import annotations

import os
from typing import Tuple

import click
import git
import github3
from rich.console import Console
from rich.table import Table

from gexpy import __name__, __version__
from gexpy.config import Config
from gexpy.logger import success, error, info, warn
from gexpy.utils import rmtree


@click.group(context_settings={'help_option_names': ['-h', '--help'],})
@click.version_option(version=__version__, prog_name=__name__)
def gex() -> None:
    pass


@click.command(name="g")
@click.argument("template", required=False)
@click.option("-n", "--name", help="Project name.")
@click.option("-sG", "--save-git", 
              help="Saves /.git directory.", 
              default=False, 
              show_default=False, 
              is_flag=True) 
def g(template, name, save_git) -> None:
    """Generate a project."""
    
    try:
        _name = str(name if name else template)
        
        dist = os.getcwd() + "\\" + _name

        info(f"Creating folder '{_name}' ...")
        os.mkdir(dist)
        
        git.Repo.clone_from(Config.URL+template, dist)
        
        if not save_git:
            warn(".git will be removed.")
            info("Removing .git ...")
            rmtree(dist + "\.git")

        success("Project successfully generated.")
    except git.GitError:
        error("Template not found.")
    except FileExistsError:
        error("Folder with this name already exists.")
    except KeyError:
        error("Template not found.")


@click.command(name='list')
def _list() -> None:
    """List of all available templates."""
    
    console = Console()
    table = Table(title="All available templates")

    table.add_column("Name")
    table.add_column("URL")
    
    org = github3.GitHub().organization("gexpy")

    for repo in org.repositories():
        repo: github3.github.repo.Repository = repo
        table.add_row(repo.name, repo.git_url[:-4].replace("git://", "https://"))

    console = Console()
    console.print(table)


commands: Tuple[click.Command] = (
    g,
    _list
)