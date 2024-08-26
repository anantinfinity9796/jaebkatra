# api_operations.py

from abc import ABC, abstractmethod



class Repository(ABC):

    @abstractmethod
    def get_all(self,):
        raise NotImplementedError
    
    @abstractmethod
    def get_one(self,):
        raise NotImplementedError

    @abstractmethod
    def create(self,):
        raise NotImplementedError
    
    @abstractmethod
    def update(self,):
        pass

    @abstractmethod
    def update_part(self,):
        pass
    
    @abstractmethod
    def delete(self,):
        pass
