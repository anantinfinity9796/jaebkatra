# db_operations.py


from abc import ABC, abstractmethod
from typing import Any

class DbOperations(ABC):

    @abstractmethod
    def create_resource(self,) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    def insert_into_resource(self,) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    def update_resource(self,) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    def delete_resource(self,) -> Any:
        raise NotImplementedError
    