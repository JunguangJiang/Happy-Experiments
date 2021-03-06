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
@click.argument('script', nargs=-1)
def run(exp, silence, script):
    """
    Run an experiment.

    If you have '-' or '--' in your script arguments, please use '--' before script.
    Example: he run --exp test -- ls -l
    """
    if exp is None:
        exp = get_current_time()
    workspace = Workspace()
    workspace.start_experiment(exp)
    workspace.run_trial(exp, script, silence)
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

    Explanations of `arg_names`:
        For script `python test.py -s clipart -t amazon`, arg_names are ['s', 't'],
        and the corresponding arg_values are ['clipart', 'amazon'].

    Explanations of `metric_names`:
        Parse the metric values from the log file.
        Note that we use the last matched value in the log file.
        For example, when metric is 'best_acc1', we will match
        the last line that look like
            - best_acc1 = 78.5
            - best_acc1: 43
            - best_acc1 100.
    """
    workspace = Workspace()
    workspace.display(experiment, arg_names, metric_names, exp_name, time, log, script, save)

