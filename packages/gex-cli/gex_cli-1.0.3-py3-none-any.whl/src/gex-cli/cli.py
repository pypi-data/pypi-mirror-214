from __future__ import annotations

import os

import click
import git
import github3
from rich.console import Console
from rich.table import Table

from . import __name__, __version__
from .logger import success, error, info, warn
from .util import rmtree


@click.group(context_settings={'help_option_names': ['-h', '--help'],})
@click.version_option(version=__version__, prog_name=__name__)
def gex() -> None:
    pass


@click.command(name="g")
@click.argument("template", 
                required=False)
@click.option("-n", "--name", "project_name",
              help="Project name.")
@click.option("-sG", "--save-git", "save_git",
              help="Saves /.git directory.", 
              default=False, 
              show_default=False, 
              is_flag=True) 
def g(template, project_name, save_git) -> None:
    """Generate a project."""
    try:
        name = str(project_name if project_name else template)
        source = f"https://github.com/gexpy/{template}"

        dist = os.getcwd() + "\\" + name

        info(f"Creating folder '{name}' ...")
        os.mkdir(dist)
        
        git.Repo.clone_from(source, dist)
        
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


def main() -> click.Group:
    gex.add_command(g)
    gex.add_command(_list)
    
    return gex()
