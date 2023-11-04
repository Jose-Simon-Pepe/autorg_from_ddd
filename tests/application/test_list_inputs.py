import os
import pytest
from autorg.application.input import AppInput
from autorg.application.dtos.input_dto import InputDto
from tests.helpers.repository import InMemoryRepository


class TestListInputs:


    @pytest.mark.integration
    def test_list_inputs_should_return_a_list_of_input_dtos(self):
        repo = InMemoryRepository()
        app = AppInput(repo)
        app.add_input("hola")
        assert type(app.list_inputs()) is list
        assert type(app.list_inputs()[0]) is InputDto

    

