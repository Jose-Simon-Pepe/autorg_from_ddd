import click
from config.config import Config
from autorg.domain.protocols.repository import Repository
from datetime import datetime
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
    @click.option("--datenum","-dn",is_flag=True,default=False,help="show all inputs date creation in a numeric way")
    @click.option("-d","day",help="Show inputs created on desired day",required=False, type=str)
    def ls_command(datenum,day):
        repo = CsvRepository(Config().storage("csv")["filepath"])
        app = AppInput(repo)
        inputs: list[str] = [inp for inp in app.list_inputs()]
    
        if len(inputs) == 0:
            click.echo("Not inputs found")
    
        else:

            if day:

                right_inp = list()

                for inp in inputs:
                    if datetime.strptime(str(inp.creation_date),"%Y-%m-%d %H:%M:%S.%f").strftime("%a %d %b %Y")==day:
                        right_inp.append(inp)

                for right in right_inp:
                    click.echo(datetime.strptime(str(right.creation_date),"%Y-%m-%d %H:%M:%S.%f").strftime("%a %d %b %Y")+" "+right.content) 


            elif not datenum:
                for item in inputs:
                    click.echo(item.content)

            elif datenum:
                for item in inputs:
                    click.echo(str(item.creation_date)+" "+item.content)

