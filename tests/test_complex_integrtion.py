import pytest
from src.models import  Parameters
from src.manager import Manager

def test_cout_costs():
    parameters = Parameters()
    manager = Manager(parameters)
    apartment_key = 'apartment-1'
    total_cost = manager.get_apartment_costs(apartment_key)
    assert isinstance(total_cost, float)
    assert total_cost >= 0.0
    assert manager.get_apartment_costs('apart-polanka', 2025, 1) == 910.0
    assert manager.get_apartment_costs('A1', 2024, 3) == 0.0