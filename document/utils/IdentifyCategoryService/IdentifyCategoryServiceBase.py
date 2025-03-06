from abc import ABC, abstractmethod
from document.models import Category


class IdentifyCategoryServiceBase(ABC):
    def __init__(self):
        categories = Category.objects.all().values("name")
        self.categories = [category["name"] for category in categories]

    @abstractmethod
    def identify_category(self, content: str) -> list[str]:
        pass
