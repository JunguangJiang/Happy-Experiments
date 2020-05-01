import os
import os.path as osp
import click
from he import colors
from collections import namedtuple
import time
import jsonpickle
import sh
from sh import ErrorReturnCode
from prettytable import PrettyTable
import re
import threading


def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


Trial = namedtuple('Trial', ['script', 'log_file', 'time', 'id'])


def parse_args(script, arg_names):
    script = [s.strip('-') for s in script]
    arg_values = []
    for arg_name in arg_names:
        try:
            idx = script.index(arg_name)
            arg_value = script[idx+1]
        except Exception:
            arg_value = ""
        arg_values.append(arg_value)
    return arg_values


def parse_metrics(log_file, metric_names):
    values = []
    with open(log_file, "r") as f:
        for metric_name in metric_names:
            metric_pattern = re.compile(metric_name + '[ =:]*([-+]?[0-9]*\.?[0-9]+)')
            value = ""
            for line in reversed(f.readlines()):
                result = metric_pattern.search(line)
                if result:  # find the latest value
                    value = result.group(1)
                    break
            values.append(value)
    return values


def copytree(src, dst):
    import shutil
    ignore_patterns = ['he_workspace']
    if osp.exists('.heignore'):
        with open('.heignore', 'r') as f:
            for line in f.readlines():
                line = line.strip().rstrip(os.linesep)
                if line == '' or line.startswith('#') or line.find('***') > -1:
                    continue
                ignore_patterns.append(line)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*ignore_patterns), symlinks=True)


class Experiment:
    def __init__(self, root, name):
        """
        :param root: root directory to store experiment information
        :param name: experiment name
        """
        self.root = root
        self.name = name
        self.trials = []

    @property
    def code(self):
        return osp.join(self.root, 'code')

    def create(self):
        os.mkdir(self.root)

    def add(self, script):
        new_id = len(self.trials)
        new_trial = Trial(script=script, time=get_current_time(), id=new_id,
                          log_file=osp.join(self.root, '{}.txt'.format(new_id)))
        self.trials.append(new_trial)
        return new_trial

    def display(self, arg_names, metric_names, time, log, script):
        table_head = list(arg_names) + list(metric_names)
        if time:
            table_head.append('time')
        if log:
            table_head.append('log')
        if script:
            table_head.append('script')
        table = PrettyTable(table_head)
        for trial in self.trials:
            table_row = parse_args(trial.script, arg_names) +\
                          parse_metrics(trial.log_file, metric_names)
            if time:
                table_row.append(trial.time)
            if log:
                table_row.append(trial.log_file)
            if script:
                table_row.append(" ".join(trial.script))
            table.add_row(table_row)
        print(table)


class Workspace:

    def __init__(self, workspace):
        self.workspace = workspace
        self.experiments = {}
        self._lock = threading.Lock()

    def run_experiment(self, experiment):
        if experiment in self.experiments:  # old experiment
            click.echo(colors.prompt('Using old experiment: ') + colors.path(experiment) + os.linesep)
        else:
            click.echo(colors.prompt('Create new experiment: ') + colors.path(experiment) + os.linesep)
            root = osp.join(self.workspace, experiment)
            exp = Experiment(root=root, name=experiment)
            exp.create()
            self.experiments[experiment] = exp
            copytree(osp.curdir, exp.code)

    def run_trial(self, experiment, script):
        assert experiment in self.experiments
        new_trial = self.experiments[experiment].add(script)
        script_string = ' '.join(script)
        cmd = script[0]
        script = script[1:]
        click.echo(colors.prompt('Running script: ') + colors.cmd('{} '.format(cmd))
                   + colors.path(script_string))

        with open(new_trial.log_file, "w") as f:
            def _fn(data, warning=False):
                if warning:
                    click.echo(colors.warning(data))
                else:
                    print(data, end='')
                f.write(data)

            current_dir = osp.abspath(osp.curdir)
            try:
                sh.cd(self.experiments[experiment].code)
                sh.Command(cmd)(script, _out=lambda data: _fn(data, warning=False))
                click.echo()
            except ErrorReturnCode as e:
                _fn(bytes.decode(e.stderr), warning=True)
            except sh.CommandNotFound as e:
                _fn("command not found: {}\n".format(str(e)), warning=True)
            except Exception as e:
                _fn(str(e), warning=True)
            sh.cd(current_dir)

    def dump(self):
        with open(osp.join(self.workspace, "workspace.json"), "w") as f:
            f.write(jsonpickle.encode(self.experiments))

    def load(self):
        with open(osp.join(self.workspace, "workspace.json"), "r") as f:
            self.experiments = jsonpickle.decode(f.read())

