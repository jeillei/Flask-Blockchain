from abc import ABC, abstractmethod
from typing import Dict, Any, List
import json
from hashlib import sha256
import time


class SmartContract(ABC):
    def __init__(self):
        self.state: Dict[str, Any] = {}
        self.owner: str = None
        self.address: str = None

    @abstractmethod
    def execute(self, method: str, params: Dict[str, Any]) -> Any:
        pass

    def get_state(self) -> Dict[str, Any]:
        return self.state

    def set_state(self, key: str, value: Any):
        self.state[key] = value


class TokenContract(SmartContract):
    def __init__(self, initial_supply: int):
        super().__init__()
        self.state['balances'] = {}
        self.state['total_supply'] = initial_supply

    def execute(self, method: str, params: Dict[str, Any]) -> Any:
        if method == "transfer":
            return self._transfer(params['from'], params['to'], params['amount'])
        elif method == "balance_of":
            return self._balance_of(params['address'])
        raise Exception(f"Unknown method: {method}")

    def _transfer(self, from_addr: str, to_addr: str, amount: int) -> bool:
        if from_addr not in self.state['balances']:
            self.state['balances'][from_addr] = 0
        if to_addr not in self.state['balances']:
            self.state['balances'][to_addr] = 0

        if self.state['balances'][from_addr] < amount:
            return False

        self.state['balances'][from_addr] -= amount
        self.state['balances'][to_addr] += amount
        return True

    def _balance_of(self, address: str) -> int:
        return self.state['balances'].get(address, 0)


class SmartContractManager:
    def __init__(self):
        self.contracts: Dict[str, SmartContract] = {}

    def deploy_contract(self, contract: SmartContract, owner: str) -> str:
        # Generate a unique address for the contract
        timestamp = str(time.time())
        address = sha256(f"{owner}{timestamp}".encode()).hexdigest()

        contract.owner = owner
        contract.address = address
        self.contracts[address] = contract

        return address

    def execute_contract(self, address: str, method: str, params: Dict[str, Any]) -> Any:
        if address not in self.contracts:
            raise Exception(f"Contract not found: {address}")

        contract = self.contracts[address]
        return contract.execute(method, params)

    def get_contract(self, address: str) -> SmartContract:
        return self.contracts.get(address)
