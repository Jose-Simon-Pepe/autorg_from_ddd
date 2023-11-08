import click
from config.config import Config
from autorg.domain.protocols.repository import Repository
import datetime
import sys
from autorg.application.dtos.input_dto import InputDto 

from autorg.application.input import AppInput
from autorg.infrastructure.adapters.csvrepository import CsvRepository


class Cli:
    

    def __init__(self,config=Config()):
        """En caso de no proveer una configuracion nueva, se usara por defecto la del proyecto"""
        self._config = config
        self.read_config()


    def read_config(self):
        try:
            if self._config.storage("csv")["filepath"]:
                self._repo = CsvRepository(self._config.storage("csv")["filepath"])

        except Exception as e:
            raise e

    def repo(self) -> Repository:
        return self._repo

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
            repo = CsvRepository(Config().storage("csv")["filepath"])
            app = AppInput(repo)
            app.add_input(input_)
            click.echo("The input was saved correctly", color=True)
        except Exception as err:
            click.echo(click.style(f"Failed adding input, {err}", fg="red"), file=sys.stderr)
    
    @inbox.command(name="ls", help="show all inputs in the inbox")
    @click.option("--date","-d",is_flag=True,default=False,help="show all inputs date creation")
    def ls_command(date):
        repo = CsvRepository(Config().storage("csv")["filepath"])
        app = AppInput(repo)
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
