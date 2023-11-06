import click
import datetime
import sys
from autorg.application.dtos.input_dto import InputDto 

from autorg.application.input import AppInput
from autorg.infrastructure.adapters.csvrepository import CsvRepository


class Cli:

    @click.group
    def autorg():
        pass


    @autorg.group
    def inbox():
        pass

    @inbox.command(name="add", help="add a input to inbox")
    @click.argument("input_")
    def add_command(input_: str):
        try:
            app = AppInput(CsvRepository())
            app.add_input(input_)
            click.echo("The input was saved correctly", color=True)
        except Exception as err:
            click.echo(click.style(f"Failed adding input, {err}", fg="red"), file=sys.stderr)
    
    @inbox.command(name="ls", help="show all inputs in the inbox")
    @click.option("--date","-d",is_flag=True,default=False,help="show all inputs date creation")
    def ls_command(date):
        app = AppInput(CsvRepository())
        inputs: list[str] = [inp for inp in app.list_inputs()]
    
        if len(inputs) == 0:
            click.echo("Not inputs found")
    
        else:
    
            if not date:
                for item in inputs:
                    click.echo(item.content)
            if date:
                for item in inputs:
                    click.echo(str(item.creation_date)+" "+item.content)
