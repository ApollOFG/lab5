from src.models import Apartment, Bill, Parameters, Tenant, Transfer, ApartmentSettlement, TenantSettlement
from typing import List

class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True
    
    def get_apartment_costs(self, apartment_key: str, year: int = None, month: int = None) -> float:
        total_cost = 0.0
        for bill in self.bills:
            if bill.apartment == apartment_key:
                if (year is None or bill.settlement_year == year) and (month is None or bill.settlement_month == month):
                    total_cost += bill.amount_pln
                
        return total_cost
    
    def create_apartment_settlement(self, apartment_key: str, year: int, month: int) -> ApartmentSettlement:
        total_bills = self.get_apartment_costs(apartment_key, year, month)
        total_rent = 0.0
        total_transfers = 0.0
        balance = total_transfers - total_bills
        return ApartmentSettlement(
            apartment=apartment_key,
            month=month,
            year=year,
            total_rent_pln=total_rent,
            total_bills_pln=total_bills,
            total_due_pln=balance
        )
    def create_tenant_settlements(self, apartment_settlement: ApartmentSettlement) -> List[TenantSettlement]:
        active_tenants = [
            t for t in self.tenants.values() 
            if t.apartment == apartment_settlement.apartment
        ]
        if not active_tenants:
            return []
        tenant_count = len(active_tenants)
        share_of_bills = apartment_settlement.total_bills_pln / tenant_count

        settlements = []
        for tenant in active_tenants:
            rent = tenant.rent_pln
            total_due = rent + share_of_bills
            balance = 0.0 - total_due

            settlements.append(TenantSettlement(
                tenant=tenant.name,
                apartment_settlement=apartment_settlement.apartment,
                month=apartment_settlement.month,
                year=apartment_settlement.year,
                rent_pln=rent,
                bills_pln=share_of_bills,
                total_due_pln=total_due,
                balance_pln=balance
            ))

        return settlements