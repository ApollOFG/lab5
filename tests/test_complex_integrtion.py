import pytest
from src.models import  Parameters, Bill, ApartmentSettlement
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


def test_create_apartment_settlement():
    
    params = Parameters()
    manager = Manager(params)
    
   
    manager.bills = [
        Bill(amount_pln=760.0, date_due="2025-02-15", apartment="apart-polanka", 
             settlement_year=2025, settlement_month=1, type="rent"),
        Bill(amount_pln=150.0, date_due="2025-02-12", apartment="apart-polanka", 
             settlement_year=2025, settlement_month=1, type="electricity")
    ]


    settlement = manager.create_apartment_settlement("apart-polanka", 2025, 1)
    

    empty_settlement = manager.create_apartment_settlement("apart-polanka", 2025, 3)

    assert isinstance(settlement, ApartmentSettlement)          
    assert settlement.apartment == "apart-polanka"              
    assert settlement.year == 2025                              
    assert settlement.month == 1                                
    assert settlement.total_bills_pln == 910.0                  
    assert settlement.total_rent_pln == 0.0                     
    assert settlement.total_due_pln == -910.0                   
    assert empty_settlement.total_bills_pln == 0.0              
    assert empty_settlement.total_due_pln == 0.0                
    assert empty_settlement.month == 3                          
    assert settlement.total_due_pln != empty_settlement.total_due_pln 
    assert settlement.total_bills_pln > 0                       