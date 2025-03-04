from abc import ABC, abstractmethod


class FormatContentServiceBase(ABC):
    """
    GenerateContentServiceBase is an abstract class that defines the method generate_content.
    """

    @abstractmethod
    def optimize_content(self, content: str) -> str:
        pass
