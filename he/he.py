import click
from he import colors
from he.workspace import Workspace
from he.util import get_current_time

@click.group()
def cli():
    """HE is built for Happy Experiments"""
    pass


@cli.command()
def init():
    """Init a happy experiment workspace"""
    workspace = Workspace()
    workspace.init()


@cli.command()
@click.option('--exp', type=click.STRING, help='experiment name')
@click.option('--script_file', default=None, type=click.STRING, help='script file')
@click.argument('script', nargs=-1)
def run(exp, script, script_file):
    """Run an experiment"""
    if exp is None:
        exp = get_current_time()
    workspace = Workspace()
    workspace.start_experiment(exp)
    if script_file is None:
        workspace.run_trial(exp, script)
    else:
        with open(script_file, 'r') as f:
            for line in f.readlines():
                workspace.run_trial(exp, line.strip().split(' '))
    click.echo(colors.prompt('Finish experiment: ') + colors.path(exp))


@cli.command()
@click.argument('experiment_name', type=click.STRING)
def delete(experiment_name):
    """Delete an experiment"""
    workspace = Workspace()
    workspace.delete_experiment(experiment_name)


@cli.command()
@click.argument('experiment', type=click.STRING, nargs=-1)
@click.option('--arg_names', '-a', multiple=True)
@click.option('--metric_names', '-m',  multiple=True)
@click.option('--exp-name/--no-exp-name', default=False)
@click.option('--time/--no-time', default=False)
@click.option('--log/--no-log', default=False)
@click.option('--script/--no-script', default=False)
@click.option('--save', type=click.STRING, help='output csv filename', default=None)
def show(experiment, arg_names, metric_names, exp_name, time, log, script, save):
    """
    Display the information of certain experiments
    When experiments are not provided, display all the experiments.
    """
    workspace = Workspace()
    workspace.display(experiment, arg_names, metric_names, exp_name, time, log, script, save)

