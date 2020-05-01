import os
import click
from he import colors
from he.workspace import Workspace

WORKSPACE_DIR = 'he_workspace'


@click.group()
def cli():
    """HE is built for Happy Experiments"""
    pass


@cli.command()
def init():
    """Init a happy experiment workspace"""
    try:
        os.mkdir(WORKSPACE_DIR)
        workspace = Workspace(WORKSPACE_DIR)
        workspace.init()
        if not os.path.exists('.heignore'):
            click.echo(colors.warning('Please provide .heignore!'))
    except FileExistsError:
        click.echo(colors.warning('HE workspace already exists!'))



@cli.command()
@click.option('--exp', prompt=True, type=click.STRING, help='experiment name')
@click.option('--script_file', default=None, type=click.STRING, help='script file')
@click.argument('script', nargs=-1)
def run(exp, script, script_file):
    """Run an experiment"""
    workspace = Workspace(WORKSPACE_DIR)
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


@cli.command()
@click.argument('experiment', type=click.STRING, nargs=-1)
@click.option('--metric_names', '-m',  multiple=True)
@click.option('--arg_names', '-a', multiple=True)
@click.option('--time/--no-time', default=False)
@click.option('--log/--no-log', default=False)
@click.option('--script/--no-script', default=False)
def show(experiment, metric_names, arg_names, time, log, script):
    """Display the information of a certain experiment"""
    workspace = Workspace(WORKSPACE_DIR)
    workspace.display(experiment, metric_names, arg_names, time, log, script)

