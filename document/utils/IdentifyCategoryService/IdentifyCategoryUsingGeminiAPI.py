from .IdentifyCategoryServiceBase import IdentifyCategoryServiceBase
from django.conf import settings
from google import genai


class IdentifyCategoryUsingGeminiAPI(IdentifyCategoryServiceBase):
    def identify_category(self, content):
        
        template = f"""
            I will provide the extracted text from an image using TesseractOCR, along with a list of predefined categories. Your task is to analyze the text and determine which categories are relevant to the content.

            Input Format:
            Extracted Text:
            {content}

            Categories:
            {self.categories}

            Output Format:
            Return relevant categories, if many split with a coma.
            Ensure that the selected categories accurately reflect the main topics or themes found in the extracted text. If no categories match, return an empty string.
            only respond with the categories.
            """

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", contents=template
        )
        return [category.strip() for category in response.text.split(",")]
