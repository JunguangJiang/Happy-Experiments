import os.path as osp

import click
import sh
from he import colors


class Trial:

    def __init__(self, script, log_file, time, id):
        """
        :param script: (list(str))
        :param log_file: (str)
        :param time: (str)
        :param id: (str)
        """
        self.script = script
        self.log_file = log_file
        self.time = time
        self.id = id

    def run(self, running_directory):
        """Run the script in the `running_directory`"""
        click.echo(colors.prompt('Running script: ') + colors.cmd(' '.join(self.script)))

        cmd = self.script[0]
        script = self.script[1:]

        with open(self.log_file, "w") as f:
            def _fn(data, warning=False):
                """print and save the Trial output"""
                if warning:
                    click.echo(colors.warning(data))
                else:
                    print(data, end='')
                f.write(data)

            current_dir = osp.abspath(osp.curdir)
            sh.cd(running_directory)
            try:
                sh.Command(cmd)(script, _out=lambda data: _fn(data, warning=False))
                click.echo()
            except sh.ErrorReturnCode as e:
                _fn(bytes.decode(e.stderr), warning=True)
            except sh.CommandNotFound as e:
                _fn("command not found: {}\n".format(str(e)), warning=True)
            except Exception as e:
                _fn(str(e), warning=True)
            sh.cd(current_dir)
