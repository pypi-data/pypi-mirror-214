# SPDX-FileCopyrightText: 2023-present Wytamma Wirth <wytamma.wirth@me.com>
#
# SPDX-License-Identifier: MIT
import click

from litchat.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="LitChat")
def litchat():
    click.echo("Hello world!")
