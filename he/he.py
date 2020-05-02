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
@click.option('--exp', type=click.STRING,
              help='Experiment name. Use current time when not provided')
@click.option('--silence/--no-silence', default=False,
              help='Whether silence the script output. Default: False')
@click.option('--script_file', default=None, type=click.STRING,
              help='Script file name.')
@click.argument('script', nargs=-1)
def run(exp, silence, script_file, script):
    """
    Run an experiment.

    If you have '-' or '--' in your script arguments, please use '--' before script.
    Example: he run --exp test -- ls -l
    """
    if exp is None:
        exp = get_current_time()
    workspace = Workspace()
    workspace.start_experiment(exp)
    if script_file is None:
        workspace.run_trial(exp, script, silence)
    else:
        with open(script_file, 'r') as f:
            for line in f.readlines():
                workspace.run_trial(exp, line.strip().split(' '), silence)
    click.echo(colors.prompt('Finish experiment: ') + colors.path(exp))


@cli.command()
@click.argument('experiment_name', type=click.STRING)
def delete(experiment_name):
    """Delete an experiment"""
    workspace = Workspace()
    workspace.delete_experiment(experiment_name)


@cli.command()
@click.argument('experiment', type=click.STRING, nargs=-1)
@click.option('--arg_names', '-a', multiple=True,
              help='The names of the args that should be displayed')
@click.option('--metric_names', '-m',  multiple=True,
              help='The names of the metrics that should be displayed')
@click.option('--exp-name/--no-exp-name', default=False,
              help='Whether display the experiment names')
@click.option('--time/--no-time', default=False,
              help='Whether display the trial time')
@click.option('--log/--no-log', default=False,
              help='Whether display the log file_names')
@click.option('--script/--no-script', default=False,
              help='Whether display the script')
@click.option('--save', type=click.STRING, default=None,
              help='The name of the output csv file. Default: None')
def show(experiment, arg_names, metric_names, exp_name, time, log, script, save):
    """
    Display the information of certain experiments.

    When experiment is not provided, display all the experiments.
    """
    workspace = Workspace()
    workspace.display(experiment, arg_names, metric_names, exp_name, time, log, script, save)

