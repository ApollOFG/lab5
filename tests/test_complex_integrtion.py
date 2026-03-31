import pytest
from src.models import  Parameters, Bill, ApartmentSettlement, TenantSettlement, Tenant
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
    
def test_create_tenant_settlements_logic():
    manager = Manager(Parameters())
    manager.tenants = {
        "t1": Tenant(name="Jan Kowalski", apartment="apart-polanka", room="r1", 
                     rent_pln=1000.0, deposit_pln=1000.0, 
                     date_agreement_from="2024-01-01", date_agreement_to="2025-01-01"),
        "t2": Tenant(name="Anna Nowak", apartment="apart-polanka", room="r2", 
                     rent_pln=1200.0, deposit_pln=1200.0, 
                     date_agreement_from="2024-01-01", date_agreement_to="2025-01-01"),
        "t3": Tenant(name="Inny Lokator", apartment="other-apart", room="r1", 
                     rent_pln=500.0, deposit_pln=500.0, 
                     date_agreement_from="2024-01-01", date_agreement_to="2025-01-01")
    }
    apt_settlement = ApartmentSettlement(
        apartment="apart-polanka", month=1, year=2025, 
        total_rent_pln=0.0, total_bills_pln=600.0, total_due_pln=-600.0
    )
    tenants_2 = manager.create_tenant_settlements(apt_settlement)
    del manager.tenants["t2"]
    tenants_1 = manager.create_tenant_settlements(apt_settlement)
    del manager.tenants["t1"]
    tenants_0 = manager.create_tenant_settlements(apt_settlement)
    assert len(tenants_2) == 2                                  
    assert tenants_2[0].bills_pln == 300.0                      
    assert tenants_2[1].bills_pln == 300.0                      
    assert tenants_2[0].rent_pln == 1000.0                      
    assert tenants_2[0].total_due_pln == 1300.0                 
    assert tenants_2[0].balance_pln == -1300.0                  
    assert len(tenants_1) == 1                                  
    assert tenants_1[0].bills_pln == 600.0                      
    assert len(tenants_0) == 0                                  
    assert isinstance(tenants_0, list)                          
    assert tenants_2[0].month == 1                              
    assert tenants_2[0].year == 2025                                    