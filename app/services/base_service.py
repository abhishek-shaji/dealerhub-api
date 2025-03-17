from abc import ABC, abstractmethod
from uuid import UUID


class BaseService(ABC):
    @abstractmethod
    def get_all(self, current_user):
        pass

    @abstractmethod
    def get_one(self, id: UUID):
        pass

    @abstractmethod
    def create(self, data, current_user):
        pass

    @abstractmethod
    def update(self, id: UUID, data):
        pass

    @abstractmethod
    def delete(self, id: UUID):
        pass
