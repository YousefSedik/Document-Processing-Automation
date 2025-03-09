from abc import ABC, abstractmethod


class ContentToJSONServiceBase(ABC):
    """
    Abstract class for ContentToJSONService
    """

    @abstractmethod
    def content_to_json(self, content):
        pass
