import click

__all__ = ['path', 'cmd', 'prompt']


def path(path):
    return click.style(path, fg='bright_blue', bg='bright_black')


def cmd(cmd):
    return click.style(cmd, fg='green', bg='bright_black')


def prompt(prompt):
    return click.style(prompt, fg='bright_yellow', bg='bright_black')


def warning(warning):
    return click.style(warning, fg='bright_red', bg='bright_black')