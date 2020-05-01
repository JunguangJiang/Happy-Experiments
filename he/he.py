import click
import os
from he import colors
from he.workspace import Workspace

WORKSPACE_DIR = 'he_workspace'

@click.group()
def cli():
    """HE is built for Happy Experiments"""
    pass


@cli.command()
@click.option(
    '--watch', prompt='Watched directory',
    type=click.Path(exists=True, file_okay=False),
    help='The directory to watch'
)
def init(watch):
    """Init a happy experiment workspace"""
    click.echo(colors.prompt('Watch directory ') + colors.path(watch))
    try:
        os.mkdir(WORKSPACE_DIR)
    except FileExistsError:
        click.echo(colors.warning('HE workspace already exists!'))
    workspace = Workspace(WORKSPACE_DIR)
    workspace.dump()


@cli.command()
@click.option('--exp', prompt=True, type=click.STRING, help='experiment name')
@click.option('--script_file', default=None, type=click.STRING, help='script file')
@click.argument('script', nargs=-1)
def run(exp, script, script_file):
    """Run an experiment"""
    workspace = Workspace(WORKSPACE_DIR)
    workspace.load()
    try:
        workspace.run_experiment(exp)
        if script_file is None:
            workspace.run_trial(exp, script)
        else:
            with open(script_file, 'r') as f:
                for line in f.readlines():
                    workspace.run_trial(exp, line.strip().split(' '))
        click.echo(colors.prompt('Finish experiment: ') + colors.path(exp))
    except Exception as e:
        click.echo(colors.warning(e))
    workspace.dump()


@cli.command()
@click.argument(
    'experiment',
    type=click.STRING,
)
@click.option(
    '--metric_names', '-m',  multiple=True
)
@click.option('--arg_names', '-a', multiple=True)
@click.option('--time/--no-time', default=False)
@click.option('--log/--no-log', default=False)
@click.option('--script/--no-script', default=False)
def show(experiment, metric_names, arg_names, time, log, script):
    """Display the information of a certain experiment"""
    workspace = Workspace(WORKSPACE_DIR)
    workspace.load()
    if experiment in workspace.experiments:
        workspace.experiments[experiment].display(arg_names, metric_names,  time, log, script)
    else:
        click.echo(colors.warning("Experiment {} doesn't exist".format(experiment)))
