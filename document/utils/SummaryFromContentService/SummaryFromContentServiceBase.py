from abc import ABC, abstractmethod

class SummaryFromContentServiceBase(ABC):
    """
    SummaryFromContentServiceBase is an abstract class that defines the method generate_summary.
    """
    
    @abstractmethod
    def generate_summary(self, content: str) -> str:
        pass