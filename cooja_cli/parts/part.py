from abc import ABC, abstractmethod

class Part(ABC):
    @abstractmethod
    def to_xml(self):
        pass
    @abstractmethod
    def to_dict(self):
        pass
    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        """Create an instance of the class from a dict."""
        pass