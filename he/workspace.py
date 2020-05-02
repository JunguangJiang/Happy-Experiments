import os
import os.path as osp

import click
from prettytable import PrettyTable
import pandas as pd

from he import colors
from he.config import *
from he.experiment import Experiment
from he.util import ExclusivePersistentObject


class Workspace:
    """HE Workspace"""
    def __init__(self):
        experiments_file = osp.join(WORKSPACE_DIR, "workspace.json")
        self.experiments_on_disk = ExclusivePersistentObject(experiments_file)

    def check(self):
        experiments_file = osp.join(WORKSPACE_DIR, "workspace.json")
        if not osp.exists(experiments_file):
            click.echo(colors.warning("Cannot find HE workspace!"))
            exit(0)

    def init(self):
        """
        Init the Workspace:
            1. make a root directory
            2. check whether IGNORE_FILE exists
            3. create a disk file to store experiments
        """
        try:
            click.echo(colors.prompt('Creating directory ') + colors.path(WORKSPACE_DIR))
            os.mkdir(WORKSPACE_DIR)
            if not os.path.exists(IGNORE_FILE):
                click.echo(colors.warning('Please provide .heignore!'))
            self.experiments_on_disk.create({})
        except FileExistsError:
            click.echo(colors.warning('HE workspace already exists!'))

    def start_experiment(self, experiment_name):
        """
        Create Experiment of name `experiment_name` only when it doesn't exist.
        """
        self.check()
        experiments = self.experiments_on_disk.load()
        if experiment_name in experiments:  # old experiment
            click.echo(colors.prompt('Using old experiment: ') + colors.path(experiment_name) + os.linesep)
        else:
            click.echo(colors.prompt('Create new experiment: ') + colors.path(experiment_name) + os.linesep)
            root = osp.join(WORKSPACE_DIR, experiment_name)
            experiments[experiment_name] = Experiment(root=root, name=experiment_name)
        self.experiments_on_disk.dump(experiments)

    def delete_experiment(self, experiment_name):
        self.check()
        experiments = self.experiments_on_disk.load()
        if experiment_name in experiments:  # old experiment
            if click.prompt(colors.prompt("Delete experiment {}? (yes/no)".format(experiment_name))) == 'yes':
                experiment = experiments[experiment_name]
                import shutil
                shutil.rmtree(experiment.root)
                experiments.pop(experiment_name)
        else:
            click.echo(colors.warning("Cannot find experiment {}".format(experiment_name)))
        self.experiments_on_disk.dump(experiments)

    def run_trial(self, experiment_name, script, silence):
        """
        :param experiment_name: (str)
        :param script: (list(str))
        :param silence: (bool) whether print results on the screen
        """
        self.check()
        # store the script information into the experiment
        # get the Trial of this script
        experiments = self.experiments_on_disk.load()
        assert experiment_name in experiments
        experiment = experiments[experiment_name]
        new_trial = experiment.add_trial(script)
        self.experiments_on_disk.dump(experiments)

        # running the new Trial
        new_trial.run(experiment.code, silence)

    def display(self, display_exp_names, arg_names, metric_names,
                has_exp_name, time, log, script, csv_file=None):
        """
        :param display_exp_names: (list(str)) the names of all the experiments to be displayed
        :param arg_names: (list(str)) the names of all the hyper-parameters to be displayed
        :param metric_names: (list(str)) the names of all the metric to be displayed
        :param has_exp_name: (bool) whether show exp_name
        :param time: (bool) whether show time
        :param log: (bool) whether show log file_name
        :param script: (bool) whether show script string
        :param csv_file: (str) output csv filename. Defualt: None
        """
        self.check()
        experiments = self.experiments_on_disk.load()

        if len(display_exp_names) == 0:
            display_exp_names = experiments.keys()
        else:
            # check whether the display experiments exists
            for exp_name in display_exp_names:
                if exp_name not in experiments:
                    click.echo(colors.warning("Experiment {} doesn't exist".format(exp_name)))
                    return

        # get the table head
        table_head = []
        if len(display_exp_names) > 1:
            has_exp_name = True
        if has_exp_name:
            table_head.append("exp_name")
        table_head.extend(list(arg_names) + list(metric_names))
        if time:
            table_head.append('time')
        if log:
            table_head.append('log')
        if script:
            table_head.append('script')
        table = PrettyTable(table_head)

        # get all the table rows
        table_rows = []
        for exp_name in display_exp_names:
            table_rows.extend(experiments[exp_name].get_table_rows(
                has_exp_name, arg_names, metric_names, time, log, script))

        for table_row in table_rows:
            table.add_row(table_row)

        self.experiments_on_disk.dump(experiments)

        print(table)
        if csv_file is not None:
            csv = pd.DataFrame(columns=table_head, data=table_rows)
            csv.to_csv(csv_file)

