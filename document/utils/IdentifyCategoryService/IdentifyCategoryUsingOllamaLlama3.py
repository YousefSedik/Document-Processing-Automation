from .IdentifyCategoryServiceBase import IdentifyCategoryServiceBase
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


class IdentifyCategoryUsingLLM(IdentifyCategoryServiceBase):

    def identify_category(self, content):
        template = """
            I will provide the extracted text from an image using TesseractOCR, along with a list of predefined categories. Your task is to analyze the text and determine which categories are relevant to the content.

            Input Format:
            Extracted Text:
            {content}

            Categories:
            {categories}

            Output Format:
            Return relevant categories, if many split with a coma.
            Ensure that the selected categories accurately reflect the main topics or themes found in the extracted text. If no categories match, return an empty string.
            only respond with the categories.
            """
        try:
            model = OllamaLLM(model="llama3:latest")
            prompt = ChatPromptTemplate.from_template(template)

            chain = prompt | model

            result = chain.invoke({"content": content, "categories": self.categories})
            result = result.split(',')
            return result
        except Exception as e:
            print(f"Failed to identify category: {e}")
            return ""
