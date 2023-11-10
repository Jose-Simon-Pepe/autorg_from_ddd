import os
from config.config import Config
import pytest
import datetime
from click.testing import CliRunner
from autorg.infrastructure.adapters.cli import Cli 
from autorg.infrastructure.adapters.csvrepository import CsvRepository

# TEST: debo verificar que el input ingresado haya quedado persistido
# TEST: verificar que los inputs puedan filtrarse por hora/fecha
# TEST: el comando inbox debe contener todo lo relativo a la bandeja de entrada (listar, agregar etc)
#TODO: Deberia mejorarse la logica de las opciones flag como d, el codigo queda poco claro si no

# TODO: APP adapter should recieve a instance of desired repo, no just use csv repo!

@pytest.fixture(autouse=True)
def run_around_tests():
    """This foreach is being used because of the mdfaking garbage collector being doom"""
    if len(Config._instances.values()) >0:
        Config._instances.clear()
    yield
    Config._instances.clear()


class TestCli:


    def setup_method(self):
        runner = CliRunner()
        self.runner = runner
        self.cli = Cli()
        self.now = self.get_now()

    def teardown_method(self):
        if os.path.exists("data.csv"):
            os.remove("data.csv")
        if os.path.exists("testsdata.csv"):
            os.remove("testsdata.csv")


    def get_date(self,date:str):
        return datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%a %d %b %Y")

    def get_now(self):
        return datetime.datetime.now().strftime('%a %d %b %Y')

    @pytest.mark.integration
    def test_input_command_should_persist_data(self):
        sut = self.runner.invoke(self.cli.add_command, ["random input"])
        assert sut.output == "The input was saved correctly\n"

        # ¿How verify that the input was stored?
        assert sut.exit_code == 0

    @pytest.mark.skip
    #FIX: Deberiamos replantear la forma de la prueba para que sea mas legible
    def test_list_inputs_should_show_a_list_of_all_inboxed_inputs(self):
        sut = self.runner.invoke(self.cli.add_command, ["random input"])
        sut = self.runner.invoke(self.cli.add_command, ["random input 2"])
        sut = self.runner.invoke(ls_command)
        actual =  [+1 for inp in ["random input","random input 2"] if inp in sut.output ]
        assert len(actual) == 2
        assert sut.exit_code == 0
    
    @pytest.mark.integration
    def test_list_inputs_should_show_a_msg_when_there_is_none_inboxed(self):
        sut = self.runner.invoke(self.cli.ls_command)
        assert sut.output == "Not inputs found\n"
        assert sut.exit_code == 0

    @pytest.mark.integration
    def test_dont_should_accept_duplicate_inputs(self):
        self.runner.invoke(self.cli.add_command, ["input"])
        self.runner.invoke(self.cli.add_command, ["input"])
        sut = self.runner.invoke(self.cli.ls_command)
        assert sut.output == "input\n"

    @pytest.mark.integration
    def test_list_inputs_with_d_argument_should_show_each_input_creation_date(self):
        self.runner.invoke(self.cli.add_command, ["input"])
        sut = self.runner.invoke(self.cli.ls_command,"-dn")
        now = str(datetime.datetime.now())[0:9]
        assert sut.output.startswith(now)


    def test_cli_should_be_created_with_a_config_module(self):
        assert Cli(Config()) is not None

        #TODO: Hacer que tambien se verifique, segun config, que tipo de persistencia usar
    def test_cli_should_use_config_module_for_configure_repo_storage_path(self):
        sut= Cli(Config("tests/helpers/config.toml")) 
        assert type(sut.repo()) is CsvRepository
        assert sut.repo()._repo_path == "testsdata.csv"

 #TODO: Unificar el formato de date en el proyecto sin hora y con nombre de dia
#TODO: Escribir el testdata en el csv y hacer el assertion
#    TODO: Desacoplarlo del Csv repo
    #    TODO: Mejorar el codigo feo
    def test_list_inputs_with_d_should_show_a_filtered_by_day_input_list_with_selected_day(self):
        cli = Cli(Config("tests/helpers/config.toml"))
        self.runner.invoke(cli.add_command, ["Just created input"])
        hypothetical_date = self.get_date("2023-01-20")

        with open("testsdata.csv",'a') as td:
            td.write(r"1,"+"2023-01-20"+" 18:26:04.118271,Stub input \n")

        sut = self.runner.invoke(cli.ls_command,"-d '"+hypothetical_date+"'")
        out = sut.output
        assert not out.startswith(self.now) and not out.endswith("Just created input")
        assert out.startswith(hypothetical_date)








    
