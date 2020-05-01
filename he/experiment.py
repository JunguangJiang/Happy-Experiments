import os
import os.path as osp
import re

from he.util import get_current_time
from he.config import *
from he.trial import Trial


class Experiment:
    """
    Experiment has one code version and one running environment.
    It can have multiple Trials, i.e. all the Trials are based on the same code.
    """
    def __init__(self, root, name):
        """
        1. Create the experiment directory
        2. Copy the current code snapshot to this experiment directory
        :param root: root directory to store experiment information
        :param name: experiment name
        """
        self.root = root
        self.name = name
        self.trials = []
        if not osp.exists(self.root):
            os.mkdir(self.root)
        self.code = osp.join(self.root, 'code')
        copytree(osp.curdir, self.code)

    def add_trial(self, script):
        """
        Add a new Trial without running the Trial
        :param script: (list(str))
        """
        new_id = len(self.trials)
        new_trial = Trial(script=script, time=get_current_time(), id=new_id,
                          log_file=osp.join(self.root, '{}.txt'.format(new_id)))
        self.trials.append(new_trial)
        return new_trial

    def get_table_rows(self, exp_name, arg_names, metric_names, time, log, script):
        """
        :param exp_name: (bool) whether show experiment name
        :param arg_names: (list(str)) the names of all the hyper-parameters to be displayed
        :param metric_names: (list(str)) the names of all the metric to be displayed
        :param time: (bool) whether show time
        :param log: (bool) whether show log file_name
        :param script: (bool) whether show script string
        """
        table_rows = []
        for trial in self.trials:
            table_row = []
            if exp_name:
                table_row.append(self.name)
            table_row.extend(parse_args(trial.script, arg_names))
            table_row.extend(parse_metrics(trial.log_file, metric_names))
            if time:
                table_row.append(trial.time)
            if log:
                table_row.append(trial.log_file)
            if script:
                table_row.append(" ".join(trial.script))
            table_rows.append(table_row)
        return table_rows


def parse_args(script, arg_names):
    """
    Parse the arg values from a script
    :param script: (list(str))
    :param arg_names: (list(str)) the querying arg names
    :return:
    """
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
    """
    Parse the metric values from the log file.
    Note that we use the last matched value in the log file.
    For example, when metric is 'best_acc1', we will match
    the last line that look like
        - best_acc1 = 78.5
        - best_acc1: 43
        - best_acc1 100.

    :param log_file: (str) the name of the log file
    :param metric_names: (list(str)) the querying metric names
    :return:
    """
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
    """
    Copy src directory to dst directory.
    Note that we will ignore WORKSPACE_DIR and all the files in the IGNORE_FILE.
    Besides, all the link file will be copied without copying the linked directory.
    """
    import shutil
    ignore_patterns = [WORKSPACE_DIR]
    if osp.exists(IGNORE_FILE):
        with open(IGNORE_FILE, 'r') as f:
            for line in f.readlines():
                line = line.strip().rstrip(os.linesep)
                if line == '' or line.startswith('#') or line.find('***') > -1:
                    continue
                ignore_patterns.append(line)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*ignore_patterns), symlinks=True)